from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response,
    Request, Output, Input, Config, Param, Executor
)

# --- 1. SEVİYE: GİRDİ VE ÇIKTI MODELLERİ ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"
    class Config: title = "Birinci Resim"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"
    class Config: title = "İkinci Resim"

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

# --- 2. SEVİYE: DEPENDENT DROPDOWN İÇİN PARAMETRELER (2 Farklı Tip) ---
class BlurStrength(Config):
    name: Literal["BlurStrength"] = "BlurStrength"
    value: int = Field(default=15, ge=1, le=51)
    type: Literal["number"] = "number" # Tip 1: Number
    field: Literal["textInput"] = "textInput"
    class Config: title = "Bulanıklık Gücü"

class FilterNote(Config):
    name: Literal["FilterNote"] = "FilterNote"
    value: str = "Standart İşlem"
    type: Literal["string"] = "string" # Tip 2: String
    field: Literal["textInput"] = "textInput"
    class Config: title = "İşlem Notu"

# --- 3. SEVİYE: DEPENDENT DROPDOWN SEÇENEKLERİ ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    blurStrength: BlurStrength # Bağlı alan 1
    filterNote: FilterNote   # Bağlı alan 2
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    blurStrength: BlurStrength # Bağlı alan 1
    filterNote: FilterNote   # Bağlı alan 2
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Uygulama Modu"

# --- 4. SEVİYE: EXECUTOR REQUEST / RESPONSE YAPILARI ---

# Filter Executor (1 Input, 1 Output)
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

# Compare Executor (2 Inputs, 2 Outputs)
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

# --- 5. SEVİYE: EXECUTOR VE ÜST YAPILARI ---
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtreleyici"
        json_schema_extra = {"target": {"value": 0}}

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Karşılaştırıcı"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # Trello: At least 2 Executors
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçimi"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"