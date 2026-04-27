from sdks.novavision.src.helper.package import PackageHelper

# DİKKAT: DemoPackage kısmını kendi klasör adınla değiştir.
from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    Filter, FilterResponse, FilterOutputs, OutputImage,
    Compare, CompareResponse, CompareOutputs, OutputScore, OutputLabel
)


def build_filter_response(context):
    out_img = OutputImage(value=context.output_image)
    outputs = FilterOutputs(OutputImage=out_img)
    response = FilterResponse(outputs=outputs)
    executor = Filter(value=response)
    config_exec = ConfigExecutor(value=executor)
    pkg_configs = PackageConfigs(executor=config_exec)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=pkg_configs
    )
    return package.build_model(context)


def build_compare_response(context):
    out_score = OutputScore(value=context.output_score)
    out_label = OutputLabel(value=context.output_label)
    outputs = CompareOutputs(OutputScore=out_score, OutputLabel=out_label)
    response = CompareResponse(outputs=outputs)
    executor = Compare(value=response)
    config_exec = ConfigExecutor(value=executor)
    pkg_configs = PackageConfigs(executor=config_exec)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=pkg_configs
    )
    return package.build_model(context)