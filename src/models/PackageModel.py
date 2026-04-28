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
    def set_type(cls, v, values):
        return "list" if isinstance(values.get('value'), list) else "object"
    class Config: title = "Giriş Resmi"

class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"
    class Config: title = "Giriş Tespitleri"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"
    @validator("type", pre=True, always=True)
    def set_type(cls, v, values):
        return "list" if isinstance(values.get('value'), list) else "object"
    class Config: title = "Çıkış Resmi"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"
    class Config: title = "Çıkış Tespitleri"

# --- 2. KONFİGÜRASYON (Trello Şartları: 2 Seçenek, Her Biri 2 Alan Tipi) ---
class ThresholdValue(Config):
    name: Literal["ThresholdValue"] = "ThresholdValue"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Bulanıklık Oranı"

class FeatureStatus(Config):
    name: Literal["optionEnable"] = "optionEnable"
    value: Literal["Enable"] = "Enable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Aktiflik"

class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    threshold: ThresholdValue # Alan 1: textInput
    status: FeatureStatus     # Alan 2: option
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Temel Mod"

class AdvancedKernel(Config):
    name: Literal["AdvancedKernel"] = "AdvancedKernel"
    value: int = Field(default=21, ge=1, le=99)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Kernel Boyutu"

class AlgoOption(Config):
    name: Literal["Gaussian"] = "Gaussian"
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian"

class AdvancedAlgo(Config):
    name: Literal["AdvancedAlgo"] = "AdvancedAlgo"
    value: Union[AlgoOption] = Field(default_factory=AlgoOption)
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Algoritma"

class ConfigAdvanced(Config):
    name: Literal["ConfigAdvanced"] = "ConfigAdvanced"
    kernel: AdvancedKernel # Alan 1: textInput
    algo: AdvancedAlgo     # Alan 2: dropdownlist
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gelişmiş Mod"

class MainConfig(Config):
    name: Literal["MainConfig"] = "MainConfig"
    value: Union[ConfigMode, ConfigAdvanced] = Field(default_factory=ConfigMode)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Çalışma Modu"

# --- 3. EXECUTOR REQUEST/RESPONSE ---
class CompareInputs(Inputs):
    inputImage: InputImage
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class CompareOutputs(Outputs):
    outputImage: OutputImage
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None
    configs: CompareConfigs
    class Config: json_schema_extra = {"target": "configs"}

class CompareConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class CompareResponse(Response):
    outputs: CompareOutputs

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Resim Karşılaştırma"
        json_schema_extra = {"target": {"value": 0}}

class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: OutputDetections
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class FilterRequest(Request):
    inputs: Optional[FilterInputs] = None
    configs: FilterConfigs
    class Config: json_schema_extra = {"target": "configs"}

class FilterConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class FilterResponse(Response):
    outputs: FilterOutputs

class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Resim Filtreleme"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev"

class PackageConfigs(Configs):
    executor: ConfigExecutor
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"