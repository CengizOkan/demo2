from sdks.novavision.src.helper.package import PackageHelper

from components.DemoPackage.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    Filter, FilterResponse, FilterOutputs, OutputDataOne, OutputDataTwo,
    Compare, CompareResponse, CompareOutputs
)


def build_filter_response(context):
    out_data = OutputDataOne(value=context.output_data)
    outputs = FilterOutputs(OutputDataOne=out_data)
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
    out_one = OutputDataOne(value=context.output_one)
    out_two = OutputDataTwo(value=context.output_two)
    outputs = CompareOutputs(OutputDataOne=out_one, OutputDataTwo=out_two)
    response = CompareResponse(outputs=outputs)
    executor = Compare(value=response)
    config_exec = ConfigExecutor(value=executor)
    pkg_configs = PackageConfigs(executor=config_exec)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=pkg_configs
    )
    return package.build_model(context)