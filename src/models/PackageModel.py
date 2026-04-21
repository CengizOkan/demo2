from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Param, Executor

# --- 1. GİRDİ VE ÇIKTI MODELLERİ ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"

class OutputImage(Output):
    name: Literal["OutputImage"] = "OutputImage" # Baş harf büyük
    value: Image
    type: Literal["object"] = "object"

class OutputScore(Output):
    name: Literal["OutputScore"] = "OutputScore" # Baş harf büyük
    value: float
    type: Literal["number"] = "number"

class OutputLabel(Output):
    name: Literal["OutputLabel"] = "OutputLabel" # Baş harf büyük
    value: str
    type: Literal["string"] = "string"

# --- 2. BAĞLI ALANLAR (Trello: 2 Farklı Tip Alan Şartı)  ---
class KernelSize(Config):
    name: Literal["KernelSize"] = "KernelSize"
    value: int = 15
    type: Literal["number"] = "number" # Tip 1: Sayı
    field: Literal["textInput"] = "textInput"
    class Config: title = "Filtre Gücü"

class ProcessNote(Config):
    name: Literal["ProcessNote"] = "ProcessNote"
    value: str = "Demo"
    type: Literal["string"] = "string" # Tip 2: Yazı
    field: Literal["textInput"] = "textInput"
    class Config: title = "Not"

# --- 3. SEÇENEKLER VE DROPDOWN ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    kernelSize: KernelSize # Bağlı alan 1
    processNote: ProcessNote # Bağlı alan 2
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    kernelSize: KernelSize
    processNote: ProcessNote
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Uygulama Modu"

# --- 4. EXECUTOR REQUEST / RESPONSE ---
# Filter (1 In / 1 Out)
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    OutputImage: OutputImage # PascalCase

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

# Compare (2 In / 2 Out)
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

# --- 5. ANA YAPI ---
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtreleme"
        schema_extra = {"target": {"value": 0}}

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Karşılaştırma"
        schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare] # En az 2 Executor
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Görev Seçin"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID = "1331112"