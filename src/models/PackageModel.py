from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Param, Executor

# --- 1. INPUTS & OUTPUTS ---
# Kural: Output isimleri büyük harfle başlamalıdır.
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

# --- 2. DEPENDENT DROPDOWN İÇİN BAĞLI ALANLAR ---
class KernelSize(Config):
    name: Literal["KernelSize"] = "KernelSize"
    value: int = Field(default=15, ge=1, le=51)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Filtre Gücü"

class OptionFast(Config):
    name: Literal["Fast"] = "Fast"
    value: Literal["Fast"] = "Fast"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Hızlı"

class OptionQuality(Config):
    name: Literal["Quality"] = "Quality"
    value: Literal["Quality"] = "Quality"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Kaliteli"

class ProcessMode(Config):
    name: Literal["ProcessMode"] = "ProcessMode"
    value: Union[OptionFast, OptionQuality]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "İşlem Modu"

# --- 3. DROPDOWN SEÇENEKLERİ (Her biri 2 farklı tip alan tetikler) ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    kernelSize: KernelSize # Alan 1: textInput
    processMode: ProcessMode # Alan 2: dropdownlist
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Gaussian Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    kernelSize: KernelSize
    processMode: ProcessMode
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Keskinleştirme"

class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Uygulama Tipi"

# --- 4. EXECUTOR REQUEST / RESPONSE ---
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    OutputImage: OutputImage

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
    OutputScore: OutputScore
    OutputLabel: OutputLabel

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: ConfigFilterType
    class Config: schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

# --- 5. EXECUTORS VE ÜST YAPI ---
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
    value: Union[Filter, Compare] # En az 2 Executor [cite: 588]
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