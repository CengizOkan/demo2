from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Param, Executor

# --- 1. INPUTS & OUTPUTS ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Image
    type: Literal["object"] = "object"

class OutputImage(Output):
    name: Literal["OutputImage"] = "OutputImage" # Büyük harf şart
    value: Image
    type: Literal["object"] = "object"

class OutputScore(Output):
    name: Literal["OutputScore"] = "OutputScore" # Büyük harf şart
    value: float
    type: Literal["number"] = "number"

class OutputLabel(Output):
    name: Literal["OutputLabel"] = "OutputLabel" # Büyük harf şart
    value: str
    type: Literal["string"] = "string"

# --- 2. PARAMETRELER VE DROPDOWN ---
class BlurStrength(Config):
    name: Literal["BlurStrength"] = "BlurStrength"
    value: int = 15
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Güç"

class FilterNote(Config):
    name: Literal["FilterNote"] = "FilterNote"
    value: str = "Demo"
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Not"

class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    blurStrength: BlurStrength
    filterNote: FilterNote
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
    class Config: title = "Mod Seçin"

# --- 3. REQUEST / RESPONSE ---
class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    OutputImage: OutputImage # Attribute ismi de büyük harfle başlamalı [cite: 509]

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: ConfigFilterType
    class Config:
        schema_extra = {"target": "configs"} # schema_extra kullanımı

class FilterResponse(Response):
    outputs: FilterOutputs

class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class CompareOutputs(Outputs):
    OutputScore: OutputScore # Büyük harf [cite: 509]
    OutputLabel: OutputLabel # Büyük harf [cite: 509]

class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: ConfigFilterType
    class Config:
        schema_extra = {"target": "configs"}

class CompareResponse(Response):
    outputs: CompareOutputs

# --- 4. EXECUTORS ---
class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filtre"
        schema_extra = {"target": {"value": 0}}

class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Kıyasla"
        schema_extra = {"target": {"value": 0}}

# --- 5. ANA YAPI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Görev Seçin"
        # Birden fazla executor olduğu için target yok [cite: 598]

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID = "1331112" # Doğrudan atama