from components.DemoPackage.src.models.PackageModel import FilterResponse, OutputImage


def build_filter_response(context):
    # Eğer output_image oluşturulmuşsa Response modeline ekle
    outputs = []
    if hasattr(context, 'output_image'):
        outputs.append(OutputImage(value=context.output_image))

    return FilterResponse(outputs=outputs)