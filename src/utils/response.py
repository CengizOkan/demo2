from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    # Filter
    Filter, FilterResponse, FilterOutputs, OutputImage,
    # Compare
    Compare, CompareResponse, CompareOutputs,
    OutputScore, OutputLabel,
)


def build_filter_response(context):
    output_image = OutputImage(value=context.output_image)
    outputs = FilterOutputs(outputImage=output_image)
    response = FilterResponse(outputs=outputs)
    executor = Filter(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )
    return package.build_model(context)


def build_compare_response(context):
    output_score = OutputScore(value=context.output_score)
    output_label = OutputLabel(value=context.output_label)
    outputs = CompareOutputs(outputScore=output_score, outputLabel=output_label)
    response = CompareResponse(outputs=outputs)
    executor = Compare(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )
    return package.build_model(context)