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
    def set_type_based_on_value(cls, value, values):
        val = values.get('value') if isinstance(values, dict) else getattr(values, 'value', None)
        return "object" if isinstance(val, Image) else "list"

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
    def set_type_based_on_value(cls, value, values):
        val = values.get('value') if isinstance(values, dict) else getattr(values, 'value', None)
        return "object" if isinstance(val, Image) else "list"

    class Config: title = "Output Image"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"

    class Config: title = "Output Detections"


# --- 2. DEPENDENT DROPDOWN KONFİGÜRASYONU ---
class ThresholdValue(Config):
    name: Literal["ThresholdValue"] = "ThresholdValue"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Threshold"


class OptionEnable(Config):
    name: Literal["optionEnable"] = "optionEnable"
    value: Literal["Enable"] = "Enable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Enable"


class OptionDisable(Config):
    name: Literal["optionDisable"] = "optionDisable"
    value: Literal["Disable"] = "Disable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Disable"


class DependentDrop(Config):
    name: Literal["DependentDrop"] = "DependentDrop"
    value: Union[OptionEnable, OptionDisable] = Field(default_factory=lambda: OptionEnable())
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Feature Status"


class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    thresholdValue: Optional[ThresholdValue] = None
    dependentDrop: Optional[DependentDrop] = None
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Temel Mod"


class ConfigAdvanced(Config):
    name: Literal["ConfigAdvanced"] = "ConfigAdvanced"
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Gelişmiş Mod"


class MainConfig(Config):
    name: Literal["MainConfig"] = "MainConfig"
    value: Union[ConfigMode, ConfigAdvanced] = Field(default_factory=lambda: ConfigMode())
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Çalışma Modu"


# --- 3. EXECUTOR 1: Compare ---
class CompareInputs(Inputs):
    inputImage: Optional[InputImage] = None


class CompareConfigs(Configs):
    mainConfig: Optional[MainConfig] = None


class CompareOutputs(Outputs):
    outputImage: Optional[OutputImage] = None


class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None
    configs: Optional[CompareConfigs] = None

    class Config: json_schema_extra = {"target": "configs"}


class CompareResponse(Response):
    outputs: Optional[CompareOutputs] = None


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse] = Field(default_factory=CompareRequest)
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- 4. EXECUTOR 2: Filter ---
class FilterInputs(Inputs):
    inputImage: Optional[InputImage] = None
    inputDetections: Optional[InputDetections] = None


class FilterConfigs(Configs):
    mainConfig: Optional[MainConfig] = None


class FilterOutputs(Outputs):
    outputImage: Optional[OutputImage] = None
    outputDetections: Optional[OutputDetections] = None


class FilterRequest(Request):
    inputs: Optional[FilterInputs] = None
    configs: Optional[FilterConfigs] = None

    class Config: json_schema_extra = {"target": "configs"}


class FilterResponse(Response):
    outputs: Optional[FilterOutputs] = None


class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse] = Field(default_factory=FilterRequest)
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filter Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- 5. PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter] = Field(default_factory=Compare)
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Task"


class PackageConfigs(Configs):
    executor: Optional[ConfigExecutor] = None


class PackageModel(Package):
    configs: Optional[PackageConfigs] = None
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"