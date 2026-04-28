from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, value, values):
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
    def set_type(cls, value, values):
        val = values.get('value') if isinstance(values, dict) else getattr(values, 'value', None)
        return "object" if isinstance(val, Image) else "list"
    class Config: title = "Output Image"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"
    class Config: title = "Output Detections"

# --- DEPENDENT DROPDOWN ---
class ThresholdConfig(Config):
    name: Literal["ThresholdConfig"] = "ThresholdConfig"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Eşik (Threshold)"

class SubOptionA(Config):
    name: Literal["subOptionA"] = "subOptionA"
    value: Literal["Aktif"] = "Aktif"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Aktif"

class SubOptionB(Config):
    name: Literal["subOptionB"] = "subOptionB"
    value: Literal["Pasif"] = "Pasif"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Pasif"

class DropdownConfig(Config):
    name: Literal["DropdownConfig"] = "DropdownConfig"
    value: Union[SubOptionA, SubOptionB] = Field(default_factory=lambda: SubOptionA())
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Durum"

class SelectBoxConfig(Config):
    name: Literal["SelectBoxConfig"] = "SelectBoxConfig"
    value: List[Union[SubOptionA, SubOptionB]] = Field(default_factory=list)
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"
    class Config: title = "Çoklu Seçim"

class CustomTextConfig(Config):
    name: Literal["CustomTextConfig"] = "CustomTextConfig"
    value: str = Field(default="Default")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Özel Metin"

class OptionMode1(Config):
    name: Literal["optionMode1"] = "optionMode1"
    thresholdConfig: Optional[ThresholdConfig] = None
    dropdownConfig: Optional[DropdownConfig] = None
    value: Literal["Mode1"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Mod 1"

class OptionMode2(Config):
    name: Literal["optionMode2"] = "optionMode2"
    selectBoxConfig: Optional[SelectBoxConfig] = None
    customTextConfig: Optional[CustomTextConfig] = None
    value: Literal["Mode2"] = "Mode2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Mod 2"

class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    value: Union[OptionMode1, OptionMode2] = Field(default_factory=lambda: OptionMode1())
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Çalışma Modu"

# --- GİZLİ WRAPPER ALANLARI (Flow Engine İçin Kritik) ---
class CompareInputs(Inputs):
    name: Literal["Inputs"] = "Inputs"
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"
    inputImage: Optional[InputImage] = None

class CompareConfigs(Configs):
    name: Literal["Configs"] = "Configs"
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"
    mainConfig: Optional[ConfigMode] = None

class CompareOutputs(Outputs):
    name: Literal["Outputs"] = "Outputs"
    value: str = "Outputs"
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"
    outputImage: Optional[OutputImage] = None

class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None
    configs: Optional[CompareConfigs] = None
    class Config: json_schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: Optional[CompareOutputs] = None

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Compare Executor"
        json_schema_extra = {"target": {"value": 0}}

class FilterInputs(Inputs):
    name: Literal["Inputs"] = "Inputs"
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"
    inputImage: Optional[InputImage] = None
    inputDetections: Optional[InputDetections] = None

class FilterConfigs(Configs):
    name: Literal["Configs"] = "Configs"
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"
    mainConfig: Optional[ConfigMode] = None

class FilterOutputs(Outputs):
    name: Literal["Outputs"] = "Outputs"
    value: str = "Outputs"
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"
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
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filter Executor"
        json_schema_extra = {"target": {"value": 0}}

# --- PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Task"

class PackageConfigs(Configs):
    name: Literal["Configs"] = "Configs"
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"
    executor: Optional[ConfigExecutor] = None

class PackageModel(Package):
    configs: Optional[PackageConfigs] = None
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"