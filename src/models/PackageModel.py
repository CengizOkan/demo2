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
        return "list" if isinstance(val, list) else "object"

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
        return "list" if isinstance(val, list) else "object"
    class Config: title = "Output Image"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Optional[Union[List[Detection], Detection]] = None
    type: str = "object"
    class Config: title = "Output Detections"

# --- 2. DEPENDENT DROPDOWN KONFİGÜRASYONU (Trello Şartı) ---
class ThresholdValue(Config):
    name: Literal["ThresholdValue"] = "ThresholdValue"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Blur Şiddeti"

class FeatureStatus(Config):
    name: Literal["optionEnable"] = "optionEnable"
    value: Literal["Enable"] = "Enable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Aktif"

class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    # Alan 1: textInput, Alan 2: option
    thresholdValue: ThresholdValue
    featureStatus: FeatureStatus
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Temel Mod"

class AdvancedKernelSize(Config):
    name: Literal["AdvancedKernelSize"] = "AdvancedKernelSize"
    value: int = Field(default=15, ge=1, le=51)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Kernel Boyutu (Tek Sayı)"

class AdvancedMethod(Config):
    name: Literal["Gaussian"] = "Gaussian"
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class ConfigAdvanced(Config):
    name: Literal["ConfigAdvanced"] = "ConfigAdvanced"
    # Alan 1: textInput, Alan 2: dropdownlist (Trello Şartı Sağlandı)
    advancedKernel: AdvancedKernelSize
    advancedMethod: Union[AdvancedMethod] = Field(default_factory=AdvancedMethod)
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gelişmiş Mod"

class MainConfig(Config):
    name: Literal["MainConfig"] = "MainConfig"
    value: Union[ConfigMode, ConfigAdvanced] = Field(default_factory=ConfigMode)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "İşlem Modu"

# --- 3. EXECUTOR TANIMLARI ---
class CompareInputs(Inputs):
    inputImage: Optional[InputImage] = None
class CompareConfigs(Configs):
    mainConfig: MainConfig
class CompareOutputs(Outputs):
    outputImage: Optional[OutputImage] = None
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
        title = "Görüntü Karşılaştırma"
        json_schema_extra = {"target": {"value": 0}}

class FilterInputs(Inputs):
    inputImage: Optional[InputImage] = None
    inputDetections: Optional[InputDetections] = None
class FilterConfigs(Configs):
    mainConfig: MainConfig
class FilterOutputs(Outputs):
    outputImage: Optional[OutputImage] = None
    outputDetections: Optional[OutputDetections] = None
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
        title = "Görüntü Filtreleme"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçimi"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"