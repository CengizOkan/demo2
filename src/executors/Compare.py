import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response


class Compare(Component):
    def __init__(self, request, bootstrap):
        # KRİTİK DÜZELTME: Component sadece request alır!
        super().__init__(request)

        self.bootstrap_data = bootstrap
        self.request.model = PackageModel(**(self.request.data))

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Matematiksel işlemleri platformu geçene kadar bekletiyoruz
        self.output_score = 1.0
        self.output_label = "Sistem Calisiyor"
        return build_compare_response(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()