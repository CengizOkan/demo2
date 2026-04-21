from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs, Response,
    Request, Output, Input, Config, Param, Executor
)

# --- INPUT & OUTPUT MODELLERİ ---
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

# --- CONFIG SEÇENEKLERİ (OPTIONS) ---
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

# --- CONFIG PARAMETRELERİ ---
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

# --- REQUEST & RESPONSE ---
class FilterRequest(Request):
    inputs: Optional[List[InputImageOne]]
    configs: List[Union[ConfigFilterType, BlurRadius]]
    class Config:
        schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: List[OutputImage]

# --- EXECUTOR TANIMI ---
class Filter(Executor):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Filter Task"
        schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Task"

# --- ANA PAKET MODELİ ---
class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"
    uID: str = "1331112"