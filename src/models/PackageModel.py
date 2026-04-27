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

# --- 2. OUTPUTS (Kılavuz Şartı: Baş harfler büyük) ---
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

# --- 3. BAĞLI ALANLAR (Trello: 2 Farklı Tip) ---
class FieldNumber(Config):
    name: Literal["FieldNumber"] = "FieldNumber"
    value: float = 1.0
    type: Literal["number"] = "number" # Tip 1
    field: Literal["textInput"] = "textInput"
    class Config: title = "Sayısal Değer"

class FieldString(Config):
    name: Literal["FieldString"] = "FieldString"
    value: str = "Demo"
    type: Literal["string"] = "string" # Tip 2
    field: Literal["textInput"] = "textInput"
    class Config: title = "Metin Değeri"

# --- 4. SEÇENEKLER ---
class OptionFirst(Config):
    name: Literal["optionFirst"] = "optionFirst"
    value: Literal["optionFirst"] = "optionFirst"
    fieldNumber: FieldNumber
    fieldString: FieldString
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Birinci Seçenek"

class OptionSecond(Config):
    name: Literal["optionSecond"] = "optionSecond"
    value: Literal["optionSecond"] = "optionSecond"
    fieldNumber: FieldNumber
    fieldString: FieldString
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "İkinci Seçenek"

# --- 5. DEPENDENT DROPDOWN ---
class MyDependent(Config):
    name: Literal["MyDependent"] = "MyDependent"
    value: Union[OptionFirst, OptionSecond]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Ayarlar"

# --- 6. FILTER EXECUTOR (1-IN, 1-OUT) ---
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    OutputImage: OutputImage

class FilterConfigs(Configs):
    myDependent: MyDependent

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
        title = "Filtreleme Görevi"
        schema_extra = {"target": {"value": 0}}

# --- 7. COMPARE EXECUTOR (2-IN, 2-OUT) ---
class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class CompareOutputs(Outputs):
    OutputScore: OutputScore
    OutputLabel: OutputLabel

class CompareConfigs(Configs):
    myDependent: MyDependent

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
        title = "Kıyaslama Görevi"
        schema_extra = {"target": {"value": 0}}

# --- 8. PACKAGE ANA YAPI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "İşlem Seçimi"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"