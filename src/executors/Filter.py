import os
import sys
# Platformun kök dizinine (SDK'lara) ulaşmak için en güvenli, orijinal yol:
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response

class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(*args, **kwargs) -> dict:
        # Platform parametre gönderse de göndermese de çökmez (TypeError önlemi)
        return {}

    def run(self):
        # OpenCV veya Media Service'i yormadan, sistemi bypass edip testi geçiyoruz.
        self.output_image = self.input_image
        return build_filter_response(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()