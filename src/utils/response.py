from components.DemoPackage.src.models.PackageModel import FilterResponse, OutputImage

def build_filter_response(context):
    response_model = FilterResponse(
        outputs=[
            OutputImage(value=context.output_image)
        ]
    )
    return response_model