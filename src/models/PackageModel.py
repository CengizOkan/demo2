from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config, Param
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

    class Config:
        title = "Giriş Resmi"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Giriş Tespitleri"


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

    class Config:
        title = "Çıkış Resmi"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Çıkış Tespitleri"


# --- 2. DEPENDENT DROPDOWN KONFİGÜRASYONU ---
# Option 1 Alanları (textInput ve dropdownlist)
class Threshold(Config):
    name: Literal["Threshold"] = "Threshold"
    value: float = Field(default=0.5, ge=0, le=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Eşik Değeri"


class OptEnable(Config):
    name: Literal["optEnable"] = "optEnable"
    value: Literal["Enable"] = "Enable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Aktif"


class OptDisable(Config):
    name: Literal["optDisable"] = "optDisable"
    value: Literal["Disable"] = "Disable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Pasif"


class FeatureToggle(Config):
    name: Literal["FeatureToggle"] = "FeatureToggle"
    value: Union[OptEnable, OptDisable]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Özellik Durumu"


# Option 2 Alanları (textInput ve selectBox)
class Sensitivity(Config):
    name: Literal["Sensitivity"] = "Sensitivity"
    value: int = 50
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Hassasiyet"


class ColorRed(Config):
    name: Literal["colorRed"] = "colorRed"
    value: Literal["Red"] = "Red"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Kırmızı"


class ColorBlue(Config):
    name: Literal["colorBlue"] = "colorBlue"
    value: Literal["Blue"] = "Blue"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Mavi"


class ColorSelect(Config):
    name: Literal["ColorSelect"] = "ColorSelect"
    value: List[Union[ColorRed, ColorBlue]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"

    class Config: title = "Renk Seçimi"


# Ana Seçenekler
class OptionBasic(Config):
    name: Literal["optionBasic"] = "optionBasic"
    threshold: Threshold
    featureToggle: FeatureToggle
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Temel Mod"


class OptionAdvanced(Config):
    name: Literal["optionAdvanced"] = "optionAdvanced"
    sensitivity: Sensitivity
    colorSelect: ColorSelect
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


# --- 3. EXECUTOR 1: Compare (1 Input, 1 Output) ---
class CompareInputs(Inputs):
    inputImage: InputImage
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class CompareConfigs(Configs):
    configMode: ConfigMode
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class CompareOutputs(Outputs):
    OutputImage: OutputImage  # İlk harf zorunlu olarak büyük
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


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


# --- 4. EXECUTOR 2: Filter (2 Inputs, 2 Outputs) ---
class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class FilterConfigs(Configs):
    configMode: ConfigMode
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class FilterOutputs(Outputs):
    OutputImage: OutputImage  # İlk harf zorunlu olarak büyük
    OutputDetections: OutputDetections  # İlk harf zorunlu olarak büyük
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


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


# --- 5. PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Görev Seçimi"


class PackageConfigs(Configs):
    executor: ConfigExecutor
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "demo_pkg_001"