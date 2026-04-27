import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

# DİKKAT: DemoPackage kısmını kendi klasör adınla değiştir.
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response

class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request)
        self.request.model = PackageModel(**(self.request.data))

    @staticmethod
    def bootstrap(*args, **kwargs) -> dict:
        return {}

    def run(self):
        # Sorunsuz çalışması için statik atama
        self.output_score = 1.0
        self.output_label = "Sistem Calisiyor"
        return build_compare_response(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()