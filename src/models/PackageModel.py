from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Detection,
    Inputs, Configs, Outputs, Response, Request,
    Output, Input, Config
)


# --- GİRİŞ VE ÇIKIŞLAR ---
class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value') if isinstance(values, dict) else getattr(values, 'value', None)
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Input Image"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Input Detections"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        val = values.get('value') if isinstance(values, dict) else getattr(values, 'value', None)
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Output Image"


class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    class Config: title = "Output Detections"


# --- TRELLO ŞARTI: DEPENDENT DROPDOWN ---

# Seçenek 1'in Alt Öğeleri (Field Tipi 1: textInput, Field Tipi 2: dropdownlist)
class ThresholdConfig(Config):
    name: Literal["ThresholdConfig"] = "ThresholdConfig"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Eşik (Threshold)"


class SubOptionA(Config):
    name: Literal["subOptionA"] = "subOptionA"
    value: Literal["Aktif"] = "Aktif"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Aktif"


class SubOptionB(Config):
    name: Literal["subOptionB"] = "subOptionB"
    value: Literal["Pasif"] = "Pasif"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Pasif"


class DropdownConfig(Config):
    name: Literal["DropdownConfig"] = "DropdownConfig"
    value: Union[SubOptionA, SubOptionB]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config: title = "Durum"


# Seçenek 2'nin Alt Öğeleri (Field Tipi 1: selectBox, Field Tipi 2: textInput)
class SelectBoxConfig(Config):
    name: Literal["SelectBoxConfig"] = "SelectBoxConfig"
    value: List[Union[SubOptionA, SubOptionB]]
    type: Literal["object"] = "object"
    field: Literal["selectBox"] = "selectBox"

    class Config: title = "Çoklu Seçim"


class CustomTextConfig(Config):
    name: Literal["CustomTextConfig"] = "CustomTextConfig"
    value: str = Field(default="Default")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config: title = "Özel Metin"


# Dependent Dropdown Seçenekleri
class OptionMode1(Config):
    name: Literal["optionMode1"] = "optionMode1"
    thresholdConfig: ThresholdConfig
    dropdownConfig: DropdownConfig
    value: Literal["Mode1"] = "Mode1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Mod 1"


class OptionMode2(Config):
    name: Literal["optionMode2"] = "optionMode2"
    selectBoxConfig: SelectBoxConfig
    customTextConfig: CustomTextConfig
    value: Literal["Mode2"] = "Mode2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config: title = "Mod 2"


# Ana Config
class MainConfig(Config):
    name: Literal["MainConfig"] = "MainConfig"
    value: Union[OptionMode1, OptionMode2]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config: title = "Çalışma Modu"


# --- EXECUTOR 1: Compare (1 Input, 1 Output) ---
class CompareInputs(Inputs):
    inputImage: InputImage


class CompareConfigs(Configs):
    mainConfig: MainConfig


class CompareOutputs(Outputs):
    outputImage: OutputImage


class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- EXECUTOR 2: Filter (2 Inputs, 2 Outputs) ---
class FilterInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections


class FilterConfigs(Configs):
    mainConfig: MainConfig


class FilterOutputs(Outputs):
    outputImage: OutputImage
    outputDetections: OutputDetections


class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FilterResponse(Response):
    outputs: FilterOutputs


class Filter(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filter Executor"
        json_schema_extra = {"target": {"value": 0}}


# --- PAKET KÖK TANIMI ---
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Compare, Filter]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackage"] = "DemoPackage"