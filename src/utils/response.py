from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    Filter, FilterResponse, FilterOutputs, OutputImage,
    Compare, CompareResponse, CompareOutputs, OutputScore, OutputLabel
)

def build_filter_response(context):
    output_img = OutputImage(value=context.output_image)
    # Şartname: Attribute ismi büyük harfle başlamalı[cite: 1].
    outputs = FilterOutputs(OutputImage=output_img)
    response = FilterResponse(outputs=outputs)
    executor = Filter(value=response)
    config_exec = ConfigExecutor(value=executor)
    pkg_configs = PackageConfigs(executor=config_exec)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=pkg_configs)
    return package.build_model(context)

def build_compare_response(context):
    score = OutputScore(value=context.output_score)
    label = OutputLabel(value=context.output_label)
    # CompareOutputs içindeki OutputScore ve OutputLabel attribute'ları
    outputs = CompareOutputs(OutputScore=score, OutputLabel=label)
    response = CompareResponse(outputs=outputs)
    executor = Compare(value=response)
    config_exec = ConfigExecutor(value=executor)
    pkg_configs = PackageConfigs(executor=config_exec)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=pkg_configs)
    return package.build_model(context)