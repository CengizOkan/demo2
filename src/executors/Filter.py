from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response

class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image = self.request.get_param("inputImageOne")
        self.filter_type = self.request.get_param("ConfigFilterType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Karantina testi: Hiçbir şey yapma, sadece pass geç
        pass