from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response

class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image_one = self.request.get_param("inputImageOne")
        self.input_image_two = self.request.get_param("inputImageTwo")
        self.compare_method = self.request.get_param("ConfigCompareMethod")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Karantina testi: Hiçbir şey yapma, sadece pass geç
        pass