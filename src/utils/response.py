from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    CompareOutputs, CompareResponse, Compare,
    FilterOutputs, FilterResponse, Filter,
    OutputImage, OutputDetections
)


def build_compare_response(context):
    output_image = OutputImage(value=context.output_image)

    # PascalCase eşleşmesi
    outputs = CompareOutputs(OutputImage=output_image)

    response = CompareResponse(outputs=outputs)
    executor = Compare(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)


def build_filter_response(context):
    output_image = OutputImage(value=context.output_image)
    output_dets = OutputDetections(value=context.output_detections)

    # PascalCase eşleşmesi
    outputs = FilterOutputs(OutputImage=output_image, OutputDetections=output_dets)

    response = FilterResponse(outputs=outputs)
    executor = Filter(value=response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    return package.build_model(context)