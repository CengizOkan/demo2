from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response,
    Request, Output, Input, Config, Param, Executor
)

# --- 1. SEVİYE: INPUTS & OUTPUTS ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Image
    type: Literal["object"] = "object"

class OutputScore(Output):
    name: Literal["outputScore"] = "outputScore"
    value: float
    type: Literal["number"] = "number"

class OutputLabel(Output):
    name: Literal["outputLabel"] = "outputLabel"
    value: str
    type: Literal["string"] = "string"

# --- 2. SEVİYE: DEPENDENT DROPDOWN ALANLARI (Checklist: 2 Farklı Tip) ---
class BlurStrength(Config):
    name: Literal["BlurStrength"] = "BlurStrength"
    value: int = Field(default=15, ge=1, le=51)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Güç"

class FilterNote(Config):
    name: Literal["FilterNote"] = "FilterNote"
    value: str = "Demo"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "İşlem Notu"

# --- 3. SEVİYE: DROPDOWN SEÇENEKLERİ ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    blurStrength: BlurStrength # Tetiklenen 1. alan
    filterNote: FilterNote   # Tetiklenen 2. alan
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    blurStrength: BlurStrength # Tetiklenen 1. alan
    filterNote: FilterNote   # Tetiklenen 2. alan
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Filtre Modu"

# --- 4. SEVİYE: REQUEST / RESPONSE (Örnek Kod 27'deki gibi Liste Değil Tekil) ---
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    outputImage: OutputImage

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class CompareOutputs(Outputs):
    outputScore: OutputScore
    outputLabel: OutputLabel

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

# --- 5. SEVİYE: EXECUTOR VE ÜST YAPI ---
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtre"
        json_schema_extra = {"target": {"value": 0}}

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Kıyasla"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Görev Seçin"
        json_schema_extra = {"target": "value"} # Tek executor referansı için şartnamede belirtilen target

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"