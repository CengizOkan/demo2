from components.DemoPackage.src.models.PackageModel import (
    FilterResponse, OutputImage, CompareResponse, OutputScore, OutputLabel
)

def build_filter_response(context):
    outputs = []
    if hasattr(context, 'output_image') and context.output_image is not None:
        outputs.append(OutputImage(value=context.output_image))

    return FilterResponse(outputs=outputs)

def build_compare_response(context):
    outputs = []
    if hasattr(context, 'output_score'):
        outputs.append(OutputScore(value=context.output_score))
    if hasattr(context, 'output_label'):
        outputs.append(OutputLabel(value=context.output_label))

    return CompareResponse(outputs=outputs)