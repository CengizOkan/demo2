from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)

# --- 1. GİRİŞ/ÇIKIŞ TANIMLARI ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, list):
            return "list"
        return "object"

    class Config: title = "Input Image"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"

    class Config: title = "Input Detections"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, list):
            return "list"
        return "object"

    class Config: title = "Output Image"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"

    class Config: title = "Output Detections"


# --- 2. DROPDOWN KONFİGÜRASYONU ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist", "option"] = "dropdownlist"

    class Config: title = "Blur"


class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist", "option"] = "dropdownlist"

    class Config: title = "Sharpen"


class OptionGrayscale(Config):
    name: Literal["Grayscale"] = "Grayscale"
    value: Literal["Grayscale"] = "Grayscale"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist", "option"] = "dropdownlist"

    class Config: title = "Grayscale"


class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen, OptionGrayscale] = Field(default_factory=OptionBlur)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Filtre Tipi"


# --- 3. EXECUTOR 1: Compare ---
class CompareInputs(Inputs):
    inputImage: Optional[InputImage] = None
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class CompareConfigs(Configs):
    configFilterType: ConfigFilterType
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class CompareOutputs(Outputs):
    outputImage: Optional[OutputImage] = None
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None
    configs: CompareConfigs

    class Config: json_schema_extra = {"target": "configs"}


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- 4. EXECUTOR 2: Filter ---
class FilterInputs(Inputs):
    inputImage: Optional[InputImage] = None
    inputDetections: Optional[InputDetections] = None
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class FilterConfigs(Configs):
    configFilterType: ConfigFilterType
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class FilterOutputs(Outputs):
    outputImage: Optional[OutputImage] = None
    outputDetections: Optional[OutputDetections] = None
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


class FilterRequest(Request):
    inputs: Optional[FilterInputs] = None
    configs: FilterConfigs

    class Config: json_schema_extra = {"target": "configs"}


class FilterResponse(Response):
    outputs: FilterOutputs


class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filter Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- 5. PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"