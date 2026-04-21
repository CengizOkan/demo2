from components.DemoPackage.src.models.PackageModel import FilterResponse, OutputImage


def build_filter_response(context):
    outputs = []
    # Eğer bir çıktı üretildiyse listeye ekle
    if hasattr(context, 'output_image') and context.output_image:
        outputs.append(OutputImage(value=context.output_image))

    return FilterResponse(outputs=outputs)