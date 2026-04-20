from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Config, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Image
)


# ===========================================================================
# INPUTS
# ===========================================================================

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Image"


# ===========================================================================
# OUTPUTS
# ===========================================================================

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Processed Image"


class OutputScore(Output):
    name: Literal["outputScore"] = "outputScore"
    value: float
    type: Literal["number"] = "number"

    class Config:
        title = "Similarity Score"


class OutputLabel(Output):
    name: Literal["outputLabel"] = "outputLabel"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Result Label"


# ===========================================================================
# EXECUTOR 1 — FILTER
# 1 input (image), 1 output (processed image)
# dependentDropdown: Blur veya Sharpen
# Her seçenek → textInput + dropdownlist (2 farklı field tipi)
# ===========================================================================

# --- Blur seçeneğinin sub-config'leri ---

class BlurRadius(Config):
    """
    Bulanıklaştırma yarıçapı. Tek sayı (1, 3, 5...) olmalıdır.
    Büyük değer daha fazla bulanıklık üretir.
    """
    name: Literal["BlurRadius"] = "BlurRadius"
    value: int = Field(default=5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["1, 3, 5, 7..."] = "1, 3, 5, 7..."

    class Config:
        title = "Radius"
        json_schema_extra = {"shortDescription": "Blur Radius"}


class OptionGaussian(Config):
    name: Literal["gaussian"] = "gaussian"
    value: Literal["Gaussian"] = "Gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian"


class OptionMedian(Config):
    name: Literal["median"] = "median"
    value: Literal["Median"] = "Median"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Median"


class BlurMode(Config):
    """
    Bulanıklaştırma algoritması.
    Gaussian: gürültü azaltmada etkili.
    Median: tuz-biber gürültüsüne karşı dayanıklı.
    """
    name: Literal["BlurMode"] = "BlurMode"
    value: Union[OptionGaussian, OptionMedian]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Blur Mode"
        json_schema_extra = {"shortDescription": "Algorithm"}


class Blur(Config):
    blurRadius: BlurRadius
    blurMode: BlurMode
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Blur"


# --- Sharpen seçeneğinin sub-config'leri ---

class SharpenIntensity(Config):
    """
    Keskinleştirme yoğunluğu.
    1.0 varsayılan değerdir; yüksek değerler daha güçlü keskinleştirme sağlar.
    """
    name: Literal["SharpenIntensity"] = "SharpenIntensity"
    value: float = Field(default=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["0.5 - 3.0"] = "0.5 - 3.0"

    class Config:
        title = "Intensity"
        json_schema_extra = {"shortDescription": "Sharpness Level"}


class OptionKernelSmall(Config):
    name: Literal["small"] = "small"
    value: Literal["Small"] = "Small"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Small (3x3)"


class OptionKernelLarge(Config):
    name: Literal["large"] = "large"
    value: Literal["Large"] = "Large"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Large (5x5)"


class SharpenKernel(Config):
    """
    Keskinleştirme çekirdeği boyutu.
    Küçük çekirdek ince detayları, büyük çekirdek genel kenarları vurgular.
    """
    name: Literal["SharpenKernel"] = "SharpenKernel"
    value: Union[OptionKernelSmall, OptionKernelLarge]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Kernel Size"
        json_schema_extra = {"shortDescription": "Kernel"}


class Sharpen(Config):
    sharpenIntensity: SharpenIntensity
    sharpenKernel: SharpenKernel
    name: Literal["Sharpen"] = "Sharpen"
    value: Literal["Sharpen"] = "Sharpen"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Sharpen"


# --- Filter dependentDropdown ---

class ConfigFilterType(Config):
    """
    Uygulanacak filtre türünü seçin.
    Blur görüntüyü yumuşatırken Sharpen kenarları belirginleştirir.
    """
    name: Literal["ConfigFilterType"] = "ConfigFilterType"
    value: Union[Blur, Sharpen]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Type"
        json_schema_extra = {"shortDescription": "Filter"}


# --- Filter Executor tanımı ---

class FilterInputs(Inputs):
    inputImageOne: InputImageOne


class FilterOutputs(Outputs):
    outputImage: OutputImage


class FilterConfigs(Configs):
    configFilterType: ConfigFilterType


class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FilterResponse(Response):
    outputs: FilterOutputs


class Filter(Config):
    """Tek bir görüntüye filtre uygular ve işlenmiş görüntüyü döndürür."""
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Filter"
        json_schema_extra = {"target": {"value": 0}}


# ===========================================================================
# EXECUTOR 2 — COMPARE
# 2 input (2 görüntü), 2 output (skor + etiket)
# dependentDropdown: Histogram veya FeatureBased
# Her seçenek → textInput + dropdownlist (2 farklı field tipi)
# ===========================================================================

# --- Histogram seçeneğinin sub-config'leri ---

class HistogramBins(Config):
    """
    Histogram hesaplamasında kullanılacak bin sayısı.
    Yüksek değer daha hassas karşılaştırma sağlar ancak daha yavaş çalışır.
    """
    name: Literal["HistogramBins"] = "HistogramBins"
    value: int = Field(default=256)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["32 - 256"] = "32 - 256"

    class Config:
        title = "Bins"
        json_schema_extra = {"shortDescription": "Bin Count"}


class OptionChannelRGB(Config):
    name: Literal["rgb"] = "rgb"
    value: Literal["RGB"] = "RGB"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "RGB"


class OptionChannelGrayscale(Config):
    name: Literal["grayscale"] = "grayscale"
    value: Literal["Grayscale"] = "Grayscale"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Grayscale"


class HistogramChannel(Config):
    """
    Histogram karşılaştırması için kullanılacak renk kanalı.
    RGB renk bilgisini, Grayscale yalnızca parlaklığı dikkate alır.
    """
    name: Literal["HistogramChannel"] = "HistogramChannel"
    value: Union[OptionChannelRGB, OptionChannelGrayscale]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Channel"
        json_schema_extra = {"shortDescription": "Color Channel"}


class Histogram(Config):
    histogramBins: HistogramBins
    histogramChannel: HistogramChannel
    name: Literal["Histogram"] = "Histogram"
    value: Literal["Histogram"] = "Histogram"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Histogram"


# --- FeatureBased seçeneğinin sub-config'leri ---

class FeatureMaxKeypoints(Config):
    """
    Özellik noktası eşleştirmesinde kullanılacak maksimum anahtar nokta sayısı.
    Daha fazla nokta daha doğru sonuç verir ancak işlem süresini artırır.
    """
    name: Literal["FeatureMaxKeypoints"] = "FeatureMaxKeypoints"
    value: int = Field(default=500)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["100 - 1000"] = "100 - 1000"

    class Config:
        title = "Max Keypoints"
        json_schema_extra = {"shortDescription": "Keypoint Limit"}


class OptionDetectorORB(Config):
    name: Literal["orb"] = "orb"
    value: Literal["ORB"] = "ORB"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "ORB"


class OptionDetectorSIFT(Config):
    name: Literal["sift"] = "sift"
    value: Literal["SIFT"] = "SIFT"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "SIFT"


class FeatureDetector(Config):
    """
    Özellik noktası çıkarma algoritması.
    ORB hızlı ve hafiftir; SIFT daha doğru ancak daha yavaştır.
    """
    name: Literal["FeatureDetector"] = "FeatureDetector"
    value: Union[OptionDetectorORB, OptionDetectorSIFT]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Detector"
        json_schema_extra = {"shortDescription": "Feature Detector"}


class FeatureBased(Config):
    featureMaxKeypoints: FeatureMaxKeypoints
    featureDetector: FeatureDetector
    name: Literal["FeatureBased"] = "FeatureBased"
    value: Literal["FeatureBased"] = "FeatureBased"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Feature Based"


# --- Compare dependentDropdown ---

class ConfigCompareMethod(Config):
    """
    İki görüntüyü karşılaştırmak için kullanılacak yöntemi seçin.
    Histogram piksel dağılımını, FeatureBased anahtar noktaları karşılaştırır.
    """
    name: Literal["ConfigCompareMethod"] = "ConfigCompareMethod"
    value: Union[Histogram, FeatureBased]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Compare Method"
        json_schema_extra = {"shortDescription": "Method"}


# --- Compare Executor tanımı ---

class CompareInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo


class CompareOutputs(Outputs):
    outputScore: OutputScore
    outputLabel: OutputLabel


class CompareConfigs(Configs):
    configCompareMethod: ConfigCompareMethod


class CompareRequest(Request):
    inputs: Optional[CompareInputs]
    configs: CompareConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class CompareResponse(Response):
    outputs: CompareOutputs


class Compare(Config):
    """İki görüntüyü karşılaştırır; benzerlik skoru ve sonuç etiketi döndürür."""
    name: Literal["Compare"] = "Compare"
    value: Union[CompareRequest, CompareResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Compare"
        json_schema_extra = {"target": {"value": 0}}


# ===========================================================================
# PACKAGE MODEL
# ===========================================================================

class ConfigExecutor(Config):
    """
    Çalıştırılacak işlem türünü seçin.
    Filter tek görüntüye filtre uygular, Compare iki görüntüyü karşılaştırır.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Filter, Compare]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {"shortDescription": "Select Task"}


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["ImageProcessor"] = "ImageProcessor"
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"