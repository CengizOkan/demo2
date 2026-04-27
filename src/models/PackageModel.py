from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)


# --- 1. GİRİŞ/ÇIKIŞ TANIMLARI (Tamamen camelCase) ---
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


# --- 2. TRELLO ŞARTI: DEPENDENT DROPDOWN ---

# Option 1 İçin Form Ögeleri (Tip 1: textInput, Tip 2: dropdownlist)
class ThresholdValue(Config):
    name: Literal["ThresholdValue"] = "ThresholdValue"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Eşik (Threshold)"


class OptionEnable(Config):
    name: Literal["optionEnable"] = "optionEnable"  # Option'lar camelCase
    value: Literal["Enable"] = "Enable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Aktif"


class OptionDisable(Config):
    name: Literal["optionDisable"] = "optionDisable"
    value: Literal["Disable"] = "Disable"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Pasif"


class FeatureToggle(Config):
    name: Literal["FeatureToggle"] = "FeatureToggle"
    value: Union[OptionEnable, OptionDisable]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Özellik Durumu"


# Option 2 İçin Form Ögeleri (Tip 1: textInput, Tip 2: selectBox)
class SensitivityValue(Config):
    name: Literal["SensitivityValue"] = "SensitivityValue"
    value: float = Field(default=10.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Hassasiyet"


class OptionRed(Config):
    name: Literal["optionRed"] = "optionRed"
    value: Literal["Red"] = "Red"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Kırmızı"


class OptionBlue(Config):
    name: Literal["optionBlue"] = "optionBlue"
    value: Literal["Blue"] = "Blue"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Mavi"


class ColorSelectBox(Config):
    name: Literal["ColorSelectBox"] = "ColorSelectBox"
    value: List[Union[OptionRed, OptionBlue]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"

    class Config: title = "Renk Seçimi"


# Ana Seçenekler (Dependent'ın opsiyonları)
class OptionBasic(Config):
    name: Literal["optionBasic"] = "optionBasic"
    thresholdValue: ThresholdValue  # Field 1
    featureToggle: FeatureToggle  # Field 2
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Temel Mod"


class OptionAdvanced(Config):
    name: Literal["optionAdvanced"] = "optionAdvanced"
    sensitivityValue: SensitivityValue  # Field 1
    colorSelectBox: ColorSelectBox  # Field 2
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


# --- 4. EXECUTOR 2: Filter (2 Inputs, 2 Outputs) ---
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


# --- 5. PAKET KÖK TANIMI ---
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