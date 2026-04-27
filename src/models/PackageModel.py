from pydantic import Field
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# --- 1. INPUTS ---
class InputDataOne(Input):
    name: Literal["inputDataOne"] = "inputDataOne"
    value: Union[dict, list]
    type: str = "object"
    class Config: title = "Input Data 1"

class InputDataTwo(Input):
    name: Literal["inputDataTwo"] = "inputDataTwo"
    value: Union[dict, list]
    type: str = "object"
    class Config: title = "Input Data 2"

# --- 2. OUTPUTS (Şartname: Outputların baş harfleri büyük yazılmalıdır) ---
class OutputDataOne(Output):
    name: Literal["OutputDataOne"] = "OutputDataOne"
    value: Union[dict, list]
    type: str = "object"
    class Config: title = "Output Data 1"

class OutputDataTwo(Output):
    name: Literal["OutputDataTwo"] = "OutputDataTwo"
    value: Union[dict, list]
    type: str = "object"
    class Config: title = "Output Data 2"

# --- 3. BAĞLI ALANLAR (Trello: 2 different types of field) ---
class ConfigNumber(Config):
    name: Literal["ConfigNumber"] = "ConfigNumber"
    value: int = 10
    type: Literal["number"] = "number" # Tip 1
    field: Literal["textInput"] = "textInput"
    class Config: title = "Sayısal Değer"

class ConfigText(Config):
    name: Literal["ConfigText"] = "ConfigText"
    value: str = "Demo"
    type: Literal["string"] = "string" # Tip 2
    field: Literal["textInput"] = "textInput"
    class Config: title = "Metin Değer"

# --- 4. SEÇENEKLER ---
class OptionA(Config):
    name: Literal["optionA"] = "optionA"
    value: Literal["optionA"] = "optionA"
    configNumber: ConfigNumber
    configText: ConfigText
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "A Seçeneği"

class OptionB(Config):
    name: Literal["optionB"] = "optionB"
    value: Literal["optionB"] = "optionB"
    configNumber: ConfigNumber
    configText: ConfigText
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "B Seçeneği"

# --- 5. DEPENDENT DROPDOWN ---
class ConfigDependent(Config):
    name: Literal["ConfigDependent"] = "ConfigDependent"
    value: Union[OptionA, OptionB]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Ayarlar"
        schema_extra = {"shortDescription": "Seçim yapınız"}

# --- 6. FIRST EXECUTOR (1-IN, 1-OUT) ---
class FilterInputs(Inputs):
    inputDataOne: InputDataOne

class FilterOutputs(Outputs):
    OutputDataOne: OutputDataOne

class FilterConfigs(Configs):
    configDependent: ConfigDependent

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
        title = "Filtreleme"
        schema_extra = {"target": {"value": 0}}

# --- 7. SECOND EXECUTOR (2-IN, 2-OUT) ---
class CompareInputs(Inputs):
    inputDataOne: InputDataOne
    inputDataTwo: InputDataTwo

class CompareOutputs(Outputs):
    OutputDataOne: OutputDataOne
    OutputDataTwo: OutputDataTwo

class CompareConfigs(Configs):
    configDependent: ConfigDependent

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
        title = "Kıyaslama"
        schema_extra = {"target": {"value": 0}}

# --- 8. PACKAGE ANA YAPI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare]
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