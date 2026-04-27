from pydantic import Field
from typing import Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# --- 1. INPUTS (Media Service Bypass - Sadece JSON Data) ---
class InputDataOne(Input):
    name: Literal["inputDataOne"] = "inputDataOne"
    value: Union[dict, list] # Kılavuz kuralı: Any kullanılamaz, dict/list olmalı
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class InputDataTwo(Input):
    name: Literal["inputDataTwo"] = "inputDataTwo"
    value: Union[dict, list]
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

# --- 2. OUTPUTS (Şartname: Outputların baş harfleri büyük yazılmalıdır) ---
class OutputData(Output):
    name: Literal["OutputData"] = "OutputData"
    value: Union[dict, list]
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class OutputScore(Output):
    name: Literal["OutputScore"] = "OutputScore"
    value: float
    type: Literal["number"] = "number"
    field: Literal["output"] = "output"

class OutputLabel(Output):
    name: Literal["OutputLabel"] = "OutputLabel"
    value: str
    type: Literal["string"] = "string"
    field: Literal["output"] = "output"

# --- 3. BAĞLI ALANLAR (Trello: 2 different types of field) ---
class BlurValue(Config):
    name: Literal["BlurValue"] = "BlurValue"
    value: float = 1.5
    type: Literal["number"] = "number" # Tip 1: Sayısal
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Filtre Degeri"

class FilterNote(Config):
    name: Literal["FilterNote"] = "FilterNote"
    value: str = "Islem Onayi"
    type: Literal["string"] = "string" # Tip 2: Metin
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Islem Notu"

# --- 4. SEÇENEKLER ---
class OptionBlur(Config):
    name: Literal["optionBlur"] = "optionBlur"
    value: Literal["optionBlur"] = "optionBlur"
    blurValue: BlurValue
    filterNote: FilterNote
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Bulaniklik"

class OptionSharpen(Config):
    name: Literal["optionSharpen"] = "optionSharpen"
    value: Literal["optionSharpen"] = "optionSharpen"
    blurValue: BlurValue
    filterNote: FilterNote
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Keskinlik"

# --- 5. DEPENDENT DROPDOWN ---
class ConfigDependent(Config):
    name: Literal["ConfigDependent"] = "ConfigDependent"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Filtre Secimi"

# --- 6. FIRST EXECUTOR (1-IN, 1-OUT) ---
class FilterInputs(Inputs):
    inputDataOne: InputDataOne
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class FilterOutputs(Outputs):
    OutputData: OutputData
    value: str = "Outputs"
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class FilterConfigs(Configs):
    configDependent: ConfigDependent
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

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
        title = "Filtreleme Görevi"
        schema_extra = {"target": {"value": 0}}

# --- 7. SECOND EXECUTOR (2-IN, 2-OUT) ---
class CompareInputs(Inputs):
    inputDataOne: InputDataOne
    inputDataTwo: InputDataTwo
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class CompareOutputs(Outputs):
    OutputScore: OutputScore
    OutputLabel: OutputLabel
    value: str = "Outputs"
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

class CompareConfigs(Configs):
    configDependent: ConfigDependent
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

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
        title = "Kiyaslama Görevi"
        schema_extra = {"target": {"value": 0}}

# --- 8. PACKAGE ANA YAPI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # Trello Şartı: En az 2 Executor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Görev Seçin"

class PackageConfigs(Configs):
    executor: ConfigExecutor
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"