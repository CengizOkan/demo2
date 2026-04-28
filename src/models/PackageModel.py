from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)

# --- 1. GİRİŞ VE ÇIKIŞLAR ---
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

# --- 2. KONFİGÜRASYON (Arayüz Eksik Veri Gönderirse Çökmemesi İçin Optional Yapıldı) ---
class BlurThreshold(Config):
    name: Literal["BlurThreshold"] = "BlurThreshold"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Bulanıklık Oranı"

class FeatureOption(Config):
    name: Literal["featureOption"] = "featureOption"
    value: Literal["Active"] = "Active"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Özellik Durumu"

class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    # HATANIN ÇÖZÜMÜ: Alanlar opsiyonel yapıldı
    blurThreshold: Optional[BlurThreshold] = None
    featureOption: Optional[FeatureOption] = None
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    # Arayüzün option yerine dropdownlist gönderme ihtimaline karşı tolerans
    field: Literal["option", "dropdownlist"] = "option"
    class Config: title = "Temel Mod"

class AdvancedKernel(Config):
    name: Literal["AdvancedKernel"] = "AdvancedKernel"
    value: int = Field(default=21, ge=1, le=51)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Kernel Boyutu"

class AlgoDropdown(Config):
    name: Literal["Gaussian"] = "Gaussian"
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option", "dropdownlist"] = "option"
    class Config: title = "Gaussian"

class ConfigAdvanced(Config):
    name: Literal["ConfigAdvanced"] = "ConfigAdvanced"
    # HATANIN ÇÖZÜMÜ: Alanlar opsiyonel yapıldı
    kernel: Optional[AdvancedKernel] = None
    algo: Optional[Union[AlgoDropdown]] = None
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option", "dropdownlist"] = "option"
    class Config: title = "Gelişmiş Mod"

class MainConfig(Config):
    name: Literal["MainConfig"] = "MainConfig"
    value: Union[ConfigMode, ConfigAdvanced] = Field(default_factory=ConfigMode)
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist", "dropdownlist"] = "dependentDropdownlist"
    class Config: title = "İşlem Modu"

# --- 3. EXECUTOR ŞEMALARI ---
class CompareInputs(Inputs):
    inputImage: InputImage
class CompareConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"
class CompareOutputs(Outputs):
    outputImage: OutputImage
class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None
    configs: CompareConfigs
    class Config: json_schema_extra = {"target": "configs"}
class CompareResponse(Response):
    outputs: CompareOutputs
class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse] = Field(default_factory=CompareRequest)
    type: Literal["object"] = "object"
    field: Literal["option", "dropdownlist"] = "option"
    class Config:
        title = "Compare"
        json_schema_extra = {"target": {"value": 0}}

class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: Optional[InputDetections] = None
class FilterConfigs(Configs):
    mainConfig: MainConfig
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"
class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: Optional[OutputDetections] = None
class FilterRequest(Request):
    inputs: Optional[FilterInputs] = None
    configs: FilterConfigs
    class Config: json_schema_extra = {"target": "configs"}
class FilterResponse(Response):
    outputs: FilterOutputs
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse] = Field(default_factory=FilterRequest)
    type: Literal["object"] = "object"
    field: Literal["option", "dropdownlist"] = "option"
    class Config:
        title = "Filter"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter] = Field(default_factory=Compare)
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist", "dropdownlist"] = "dependentDropdownlist"
    class Config: title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"