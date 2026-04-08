from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

# ==========================================
# ORTAK GİRDİ VE ÇIKTI MODELLERİ (INPUT / OUTPUT)
# ==========================================

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image): return "object"
        elif isinstance(value, list): return "list"
    class Config: title = "Image 1"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image): return "object"
        elif isinstance(value, list): return "list"
    class Config: title = "Image 2"

class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image): return "object"
        elif isinstance(value, list): return "list"
    class Config: title = "Result Image 1"

class OutputData(Output):
    name: Literal["outputData"] = "outputData"
    value: Union[list, str]
    type: str = "list"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, list): return "list"
        elif isinstance(value, str): return "string"
    class Config: title = "Data Metrics"

# ==========================================
# EXECUTOR 1: FILTER EXECUTOR (1 INPUT, 1 OUTPUT)
# Görev Şartı: 1 Input, 1 Output, DependentDropdown
# ==========================================

# Farklı Tip Alan 1: TextInput (Sayısal Girdi)
class BlurAmountTextInput(Config):
    name: Literal["blurAmount"] = "blurAmount"
    value: int = Field(default=5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput" # <-- Field Tipi 1: textInput
    class Config: title = "Blur Amount"

# Farklı Tip Alan 2: Option (Sabit Seçenek)
class BlurEnableOption(Config):
    name: Literal["blurEnable"] = "blurEnable"
    value: Literal["Yes"] = "Yes"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option" # <-- Field Tipi 2: option
    class Config: title = "Enable Fast Blur"

# Birinci Seçenek (İçinde 2 farklı field tipi barındırıyor)
class FilterOptionBlur(Config):
    blur_amount: BlurAmountTextInput
    blur_enable: BlurEnableOption
    name: Literal["FilterOptionBlur"] = "FilterOptionBlur"
    value: Literal["BlurMode"] = "BlurMode"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Blur Filter"

# Farklı Tip Alan 1: TextInput (Sayısal Girdi)
class SharpenAmountTextInput(Config):
    name: Literal["sharpenAmount"] = "sharpenAmount"
    value: int = Field(default=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Sharpen Amount"

# Farklı Tip Alan 2: Option (Sabit Seçenek)
class SharpenQualityOption(Config):
    name: Literal["sharpenQuality"] = "sharpenQuality"
    value: Literal["High"] = "High"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Quality Level"

# İkinci Seçenek (İçinde 2 farklı field tipi barındırıyor)
class FilterOptionSharpen(Config):
    sharpen_amount: SharpenAmountTextInput
    sharpen_quality: SharpenQualityOption
    name: Literal["FilterOptionSharpen"] = "FilterOptionSharpen"
    value: Literal["SharpenMode"] = "SharpenMode"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Sharpen Filter"

# Dependent Dropdown (En az 2 seçenek şartını sağlayan ortak özellik)
class ConfigFilterMode(Config):
    name: Literal["configFilterMode"] = "configFilterMode"
    value: Union[FilterOptionBlur, FilterOptionSharpen] # 2 Seçenek: Blur veya Sharpen
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Select Filter Mode"

class FilterInputs(Inputs):
    input1: InputImageOne # 1 Input Şartı

class FilterConfigs(Configs):
    filterMode: ConfigFilterMode

class FilterOutputs(Outputs):
    output1: OutputImageOne # 1 Output Şartı

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs
    class Config: json_schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

class FilterExecutor(Config):
    name: Literal["FilterExecutor"] = "FilterExecutor"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Filter Process"

# ==========================================
# EXECUTOR 2: BLEND EXECUTOR (2 INPUT, 2 OUTPUT)
# Görev Şartı: 2 Inputs, 2 Outputs, DependentDropdown
# ==========================================

class AlphaValTextInput(Config):
    name: Literal["alphaVal"] = "alphaVal"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Alpha Value"

class AlphaChannelOption(Config):
    name: Literal["alphaChannel"] = "alphaChannel"
    value: Literal["RGB"] = "RGB"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Channel"

class BlendOptionAlpha(Config):
    alpha_val: AlphaValTextInput
    alpha_channel: AlphaChannelOption
    name: Literal["BlendOptionAlpha"] = "BlendOptionAlpha"
    value: Literal["AlphaBlend"] = "AlphaBlend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Alpha Blend"

class MaskTolTextInput(Config):
    name: Literal["maskTol"] = "maskTol"
    value: int = Field(default=128)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config: title = "Mask Tolerance"

class MaskInvertOption(Config):
    name: Literal["maskInvert"] = "maskInvert"
    value: Literal["Inverted"] = "Inverted"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Invert Mask"

class BlendOptionMask(Config):
    mask_tol: MaskTolTextInput
    mask_invert: MaskInvertOption
    name: Literal["BlendOptionMask"] = "BlendOptionMask"
    value: Literal["MaskBlend"] = "MaskBlend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config: title = "Mask Blend"

class ConfigBlendMode(Config):
    name: Literal["configBlendMode"] = "configBlendMode"
    value: Union[BlendOptionAlpha, BlendOptionMask]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config: title = "Select Blend Mode"

class BlendInputs(Inputs):
    input1: InputImageOne # Input 1
    input2: InputImageTwo # Input 2 (Şart Sağlandı)

class BlendConfigs(Configs):
    blendMode: ConfigBlendMode

class BlendOutputs(Outputs):
    output1: OutputImageOne # Output 1
    output2: OutputData     # Output 2 (Şart Sağlandı)

class BlendRequest(Request):
    inputs: Optional[BlendInputs]
    configs: BlendConfigs
    class Config: json_schema_extra = {"target": "configs"}

class BlendResponse(Response):
    outputs: BlendOutputs

class BlendExecutor(Config):
    name: Literal["BlendExecutor"] = "BlendExecutor"
    value: Union[BlendRequest, BlendResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Blend Process"

# ==========================================
# PAKETİN ANA YAPISI (PACKAGE MODEL)
# ==========================================

class ConfigMainExecutor(Config):
    # Kullanıcının hangi Executor'ı çalıştıracağını seçtiği ana menü
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FilterExecutor, BlendExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task Type"
        json_schema_extra = {"target": "value"}

class DemoPackageConfigs(Configs):
    executor: ConfigMainExecutor

class PackageModel(Package):
    configs: DemoPackageConfigs
    type: Literal["component"] = "component"
    name : Literal["DemoPackage"] = "DemoPackage"
