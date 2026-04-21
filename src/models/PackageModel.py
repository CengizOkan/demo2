from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Param, Executor

# --- 1. SEVİYE: INPUTS & OUTPUTS ---
# Şartname: Output isimlerinin baş harfi büyük olmalı
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"

class OutputImage(Output):
    name: Literal["OutputImage"] = "OutputImage"
    value: Image
    type: Literal["object"] = "object"

class OutputScore(Output):
    name: Literal["OutputScore"] = "OutputScore"
    value: float
    type: Literal["number"] = "number"

class OutputLabel(Output):
    name: Literal["OutputLabel"] = "OutputLabel"
    value: str
    type: Literal["string"] = "string"

# --- 2. DEPENDENT DROPDOWN ALANLARI (2 Farklı Tip) ---
class BlurStrength(Config):
    name: Literal["BlurStrength"] = "BlurStrength"
    value: int = Field(default=15, ge=1, le=51)
    type: Literal["number"] = "number" # Tip 1: Number [cite: 639]
    field: Literal["textInput"] = "textInput"
    class Config: title = "Bulanıklık Değeri"

class FilterNote(Config):
    name: Literal["FilterNote"] = "FilterNote"
    value: str = "Hızlı"
    type: Literal["string"] = "string" # Tip 2: String [cite: 639]
    field: Literal["textInput"] = "textInput"
    class Config: title = "İşlem Notu"

# --- 3. DROPDOWN SEÇENEKLERİ ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    blurStrength: BlurStrength # Bağlı Alan 1
    filterNote: FilterNote     # Bağlı Alan 2
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    blurStrength: BlurStrength
    filterNote: FilterNote
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Filtre Modu"

# --- 4. EXECUTOR REQUEST / RESPONSE ---
# Şartname: First Executor (1 Input, 1 Output)
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    OutputImage: OutputImage

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"} [cite: 716]

class FilterResponse(Response):
    outputs: FilterOutputs

# Şartname: Second Executor (2 Input, 2 Output)
class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class CompareOutputs(Outputs):
    OutputScore: OutputScore
    OutputLabel: OutputLabel

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

# --- 5. EXECUTORS VE ANA YAPI ---
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Görüntü İşleme"
        schema_extra = {"target": {"value": 0}} [cite: 716]

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Görüntü Kıyaslama"
        schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # En az 2 Executor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçimi"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID = "1331112"