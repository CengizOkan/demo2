import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.utils.response import build_compare_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # Girdiyi al
        self.input_image = self.request.get_param("inputImage")
        # Config değerine erişim (Örnek: threshold)
        # self.threshold = self.request.get_param("Threshold")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # İşlem mantığı buraya gelir
        self.output_image = self.input_image
        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()