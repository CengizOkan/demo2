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
        try:
            self.request.model = PackageModel(**(self.request.data))
        except Exception:
            pass

        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections")

        if not self.input_image:
            try:
                executor_val = self.request.data.get("executor", {}).get("value", {})
                inputs = executor_val.get("value", {}).get("inputs",
                                                           {}) if "value" in executor_val else executor_val.get(
                    "inputs", {})
                if "inputImage" in inputs:
                    self.input_image = inputs["inputImage"].get("value")
                if "inputDetections" in inputs:
                    self.input_detections = inputs["inputDetections"].get("value")
            except Exception:
                pass

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        self.output_image = self.input_image
        self.output_detections = self.input_detections
        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()