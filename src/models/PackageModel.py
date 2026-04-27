from pydantic import Field
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# --- 1. INPUTS ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"

# --- 2. OUTPUTS ---
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

# --- 3. BAĞLI ALANLAR (TRELLO: 2 FARKLI TİP ŞARTI) ---
class ConfigNumber(Config):
    name: Literal["ConfigNumber"] = "ConfigNumber"
    value: int = 10
    type: Literal["number"] = "number" # TİP 1: NUMBER
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Sayısal Değer"

class ConfigString(Config):
    name: Literal["ConfigString"] = "ConfigString"
    value: str = "default"
    type: Literal["string"] = "string" # TİP 2: STRING
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Metin Değeri"

# --- 4. SEÇENEKLER ---
class OptionFirst(Config):
    name: Literal["optionFirst"] = "optionFirst"
    value: Literal["optionFirst"] = "optionFirst"
    configNumber: ConfigNumber
    configString: ConfigString
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Birinci Seçenek"

class OptionSecond(Config):
    name: Literal["optionSecond"] = "optionSecond"
    value: Literal["optionSecond"] = "optionSecond"
    configNumber: ConfigNumber
    configString: ConfigString
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "İkinci Seçenek"

# --- 5. DEPENDENT DROPDOWN ---
class ConfigDependent(Config):
    name: Literal["ConfigDependent"] = "ConfigDependent"
    value: Union[OptionFirst, OptionSecond]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Ayarlar"

# --- 6. FIRST EXECUTOR (1 IN, 1 OUT) ---
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    outputImage: OutputImage

class FilterConfigs(Configs):
    configDependent: ConfigDependent

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs
    class Config:
        schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtreleme"
        schema_extra = {"target": {"value": 0}}

# --- 7. SECOND EXECUTOR (2 IN, 2 OUT) ---
class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class CompareOutputs(Outputs):
    outputScore: OutputScore
    outputLabel: OutputLabel

class CompareConfigs(Configs):
    configDependent: ConfigDependent

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs
    class Config:
        schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Karşılaştırma"
        schema_extra = {"target": {"value": 0}}

# --- 8. ANA YAPI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # 2 Executor eklendi
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Görev Seçin"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID = "1331112"