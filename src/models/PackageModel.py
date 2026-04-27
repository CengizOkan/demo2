from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config, Param
)


# --- 1. Giriş/Çıkış Tanımları (SDK Modelleri Kullanılarak) ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Giriş Resmi"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config:
        title = "Giriş Tespitleri"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Çıkış Resmi"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config:
        title = "Çıkış Tespitleri"


# --- 2. Dependent Dropdown Konfigürasyonları ---
# Trello gereksinimi: Her seçenek 2 farklı tipte alan tetiklemeli.

# Seçenek 1 İçin Alanlar
class Threshold(Config):
    name: Literal["Threshold"] = "Threshold"
    value: float = Field(default=0.5, ge=0, le=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Eşik Değeri"


class ModeName(Config):
    name: Literal["ModeName"] = "ModeName"
    value: str = "Default"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Mod Adı"


# Seçenek 2 İçin Alanlar (Dropdown + Number)
class ColorOption(Config):
    name: Literal["colorRed"] = "colorRed"
    value: Literal["Red"] = "Red"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Kırmızı"


class ColorSelection(Config):
    name: Literal["ColorSelection"] = "ColorSelection"
    value: Union[ColorOption]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Renk Seç"


class Sensitivity(Config):
    name: Literal["Sensitivity"] = "Sensitivity"
    value: int = 50
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Hassasiyet"


# Ana Seçenek Tanımları
class OptionBasic(Config):
    name: Literal["optionBasic"] = "optionBasic"
    threshold: Threshold
    modeName: ModeName
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Temel Ayarlar"


class OptionAdvanced(Config):
    name: Literal["optionAdvanced"] = "optionAdvanced"
    colorSelection: ColorSelection
    sensitivity: Sensitivity
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Gelişmiş Ayarlar"


class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    value: Union[OptionBasic, OptionAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Çalışma Modu"


# --- 3. Executor 1: Compare (1 Input, 1 Output) ---
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
        title = "Karşılaştırma (Compare)"
        schema_extra = {"target": {"value": 0}}


# --- 4. Executor 2: Filter (2 Inputs, 2 Outputs) ---
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
        title = "Filtreleme (Filter)"
        schema_extra = {"target": {"value": 0}}


# --- 5. Paket Kök Tanımı ---
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
    uID: str = "demo_pkg_001"