from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
        val = values.get('value')
        return "object" if isinstance(val, Image) else "list"
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
    def set_type(cls, value, values):
        val = values.get('value')
        return "object" if isinstance(val, Image) else "list"
    class Config: title = "Output Image"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"
    class Config: title = "Output Detections"

# --- DEPENDENT DROPDOWN ---
class ThresholdVal(Config):
    name: Literal["ThresholdVal"] = "ThresholdVal"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Eşik"

class OptActive(Config):
    name: Literal["optActive"] = "optActive"
    value: Literal["Active"] = "Active"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Aktif"

class StatusDrop(Config):
    name: Literal["StatusDrop"] = "StatusDrop"
    value: Union[OptActive]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Durum"

class OptionBasic(Config):
    name: Literal["optionBasic"] = "optionBasic"
    thresholdVal: ThresholdVal
    statusDrop: StatusDrop
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Temel Mod"

class OptionAdvanced(Config):
    name: Literal["optionAdvanced"] = "optionAdvanced"
    thresholdVal: ThresholdVal
    statusDrop: StatusDrop
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gelişmiş Mod"

class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    value: Union[OptionBasic, OptionAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Çalışma Modu"

# --- EXECUTORS ---
class CompareInputs(Inputs):
    inputImage: InputImage

class CompareConfigs(Configs):
    configMode: ConfigMode

class CompareOutputs(Outputs):
    outputImage: OutputImage

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs
    class Config: schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Compare"
        schema_extra = {"target": {"value": 0}}

class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections

class FilterConfigs(Configs):
    configMode: ConfigMode

class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: OutputDetections

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs
    class Config: schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filter"
        schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"