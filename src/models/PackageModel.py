from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Configs, Response, Request, Output, Input, Config, Executor
)

# --- 1. INPUTS & OUTPUTS ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Image
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class OutputScore(Output):
    name: Literal["outputScore"] = "outputScore"
    value: float
    type: Literal["number"] = "number"
    field: Literal["output"] = "output"

class OutputLabel(Output):
    name: Literal["outputLabel"] = "outputLabel"
    value: str
    type: Literal["string"] = "string"
    field: Literal["output"] = "output"

# --- 2. BAĞLI ALANLAR (Trello Şartı: 2 Farklı Tip) ---
class ConfigNumber(Config):
    name: Literal["configNumber"] = "configNumber"
    value: int = 15
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Filtre Gücü"

class ConfigText(Config):
    name: Literal["configText"] = "configText"
    value: str = "Aktif"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "İşlem Durumu"

# --- 3. SEÇENEKLER ---
class OptionBlur(Config):
    name: Literal["optionBlur"] = "optionBlur"
    value: Literal["optionBlur"] = "optionBlur"
    configNumber: ConfigNumber
    configText: ConfigText
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Bulanıklaştırma"

class OptionSharpen(Config):
    name: Literal["optionSharpen"] = "optionSharpen"
    value: Literal["optionSharpen"] = "optionSharpen"
    configNumber: ConfigNumber
    configText: ConfigText
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Uygulama Modu"

# --- 4. REQUEST & RESPONSE (Senin Orijinal Yapın - Kilit Nokta Burası) ---
class FilterRequest(Request):
    inputs: Optional[List[InputImageOne]]
    configs: List[ConfigFilterType]
    class Config: schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: List[OutputImage]

class CompareRequest(Request):
    inputs: Optional[List[Union[InputImageOne, InputImageTwo]]]
    configs: List[ConfigFilterType]
    class Config: schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: List[Union[OutputScore, OutputLabel]]

# --- 5. EXECUTORS VE ANA YAPI ---
class Filter(Executor):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtreleme"
        schema_extra = {"target": {"value": 0}}

class Compare(Executor):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Karşılaştırma"
        schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # Trello: En az 2 executor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçin"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"