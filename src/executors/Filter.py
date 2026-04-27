import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

# DİKKAT: DemoPackage kısmını kendi klasör adınla değiştir.
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response

class Filter(Component):
    def __init__(self, request, bootstrap):
        # Kılavuz kuralı: Component sadece request alır.
        super().__init__(request)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(*args, **kwargs) -> dict:
        return {}

    def run(self):
        # Çökmeleri önlemek için pass-through
        self.output_image = self.input_image
        return build_filter_response(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()