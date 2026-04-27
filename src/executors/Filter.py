import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response

class Filter(Component):
    def __init__(self, request, bootstrap=None):
        super().__init__(request)
        self.request.model = PackageModel(**(self.request.data))
        self.input_data = self.request.get_param("inputDataOne")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        self.output_data = self.input_data if self.input_data else {"durum": "basarili"}
        return build_filter_response(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()