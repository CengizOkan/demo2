from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection, BoundingBox,
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

    class Config:
        title = "Input Image"


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

    class Config:
        title = "Output Image"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Output Detections"


# --- 2. DEPENDENT DROPDOWN KONFİGÜRASYONU ---

# Option 1 Alanları (textInput ve dropdownlist)
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


class FeatureToggle(Config):
    name: Literal["FeatureToggle"] = "FeatureToggle"
    value: Union[OptionEnable, OptionDisable]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Feature Toggle"


# Option 2 Alanları (textInput ve selectBox)
class SensitivityValue(Config):
    name: Literal["SensitivityValue"] = "SensitivityValue"
    value: float = Field(default=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Sensitivity"


class OptionRed(Config):
    name: Literal["optionRed"] = "optionRed"
    value: Literal["Red"] = "Red"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Red"


class OptionBlue(Config):
    name: Literal["optionBlue"] = "optionBlue"
    value: Literal["Blue"] = "Blue"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Blue"


class ColorSelection(Config):
    name: Literal["ColorSelection"] = "ColorSelection"
    value: List[Union[OptionRed, OptionBlue]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"

    class Config: title = "Color Selection"


# Ana Seçenekler
class OptionBasic(Config):
    name: Literal["optionBasic"] = "optionBasic"
    thresholdValue: ThresholdValue
    featureToggle: FeatureToggle
    value: Literal["Basic"] = "Basic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Basic Mode"


class OptionAdvanced(Config):
    name: Literal["optionAdvanced"] = "optionAdvanced"
    sensitivityValue: SensitivityValue
    colorSelection: ColorSelection
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Advanced Mode"


class ConfigMode(Config):
    name: Literal["ConfigMode"] = "ConfigMode"
    value: Union[OptionBasic, OptionAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Working Mode"


# --- 3. EXECUTOR 1: Compare ---
class CompareInputs(Inputs):
    inputImage: InputImage


class CompareConfigs(Configs):
    configMode: ConfigMode


class CompareOutputs(Outputs):
    outputImage: OutputImage


class CompareRequest(Request):
    inputs: Optional[CompareInputs] = None  # ZORUNLU: Pydantic çökmesini engeller
    configs: CompareConfigs

    class Config:
        json_schema_extra = {"target": "configs"}
        schema_extra = {"target": "configs"}  # Platformun Pydantic versiyonuna karşı çift güvenlik


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare Task"
        json_schema_extra = {"target": {"value": 0}}
        schema_extra = {"target": {"value": 0}}


# --- 4. EXECUTOR 2: Filter ---
class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections


class FilterConfigs(Configs):
    configMode: ConfigMode


class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: OutputDetections


class FilterRequest(Request):
    inputs: Optional[FilterInputs] = None  # ZORUNLU: Pydantic çökmesini engeller
    configs: FilterConfigs

    class Config:
        json_schema_extra = {"target": "configs"}
        schema_extra = {"target": "configs"}


class FilterResponse(Response):
    outputs: FilterOutputs


class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filter Task"
        json_schema_extra = {"target": {"value": 0}}
        schema_extra = {"target": {"value": 0}}


# --- 5. PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        # Birden fazla executor olduğunda target KESİNLİKLE yazılmaz (Markdown kuralı)


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"