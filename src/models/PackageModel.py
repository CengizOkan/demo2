from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response,
    Request, Output, Input, Config, Param, Executor
)

# --- 1. SEVİYE: YAPRAK DÜĞÜMLER (Inputs & Outputs) ---
class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Image
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Image
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"

# --- 2. SEVİYE: CONFIG SEÇENEKLERİ (Options) ---
class OptionBlur(Config):
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Blur"

class OptionSharpen(Config):
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Sharpen"

# --- 3. SEVİYE: CONFIG PARAMETRELERİ ---
class ConfigFilterType(Config):
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[OptionBlur, OptionSharpen]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Filter Type"

class BlurRadius(Config):
    name: Literal["BlurRadius"] = "BlurRadius"
    value: int = 5
    type: Literal["number"] = "number"
    field: Literal["input"] = "input"
    class Config: title = "Blur Radius"

# --- 4. SEVİYE: REQUEST & RESPONSE MODELLERİ ---
class FilterRequest(Request):
    inputs: Optional[List[InputImageOne]]
    configs: List[Union[ConfigFilterType, BlurRadius]]
    class Config:
        schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: List[OutputImage]

# --- 5. SEVİYE: EXECUTOR VE ÜST YAPILAR ---
class Filter(Executor):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filter Task"
        schema_extra = {"target": {"value": 0}} # Request'e yönlendirir

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"