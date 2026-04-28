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
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config: title = "Input Image"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Input Detections"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value')
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config: title = "Output Image"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
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
    value: Union[OptionEnable, OptionDisable]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Feature Status"


class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    thresholdValue: ThresholdValue
    dependentDrop: DependentDrop
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
    value: Union[ConfigMode, ConfigAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Çalışma Modu"


# --- 3. EXECUTOR 1: Compare ---
class CompareInputs(Inputs):
    inputImage: InputImage
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class CompareConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class CompareOutputs(Outputs):
    outputImage: OutputImage
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
    inputImage: InputImage
    inputDetections: InputDetections
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class FilterConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: OutputDetections
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