import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.utils.response import build_filter_response
from components.DemoPackage.src.models.PackageModel import PackageModel

class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Trello şartı: 2 girdi alınır, 2 çıktı olarak verilir.
        self.output_image = self.input_image
        self.output_detections = self.input_detections
        return build_filter_response(self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()