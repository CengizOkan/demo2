import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.base.model import Image, Detection
from components.DemoPackage.src.utils.response import build_filter_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        try:
            self.request.model = PackageModel(**(self.request.data))
        except Exception:
            pass

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        self.output_image = None
        self.output_detections = None

        # 1. En Güvenli Yöntem: Pydantic üzerinden saf objelere erişim
        try:
            req_data = self.request.model.configs.executor.value.value
            if req_data and req_data.inputs:
                if req_data.inputs.inputImage:
                    self.output_image = req_data.inputs.inputImage.value
                if hasattr(req_data.inputs, 'inputDetections') and req_data.inputs.inputDetections:
                    self.output_detections = req_data.inputs.inputDetections.value
        except Exception:
            pass

        # 2. Alternatif Yöntem: Fallback
        if not self.output_image or not self.output_detections:
            def get_inner_val(data, target_name, target_class):
                if isinstance(data, dict):
                    if data.get("name") == target_name and "value" in data:
                        val = data["value"]
                        if isinstance(val, dict): return target_class(**val)
                        if isinstance(val, list): return [target_class(**v) if isinstance(v, dict) else v for v in val]
                    for k, v in data.items():
                        res = get_inner_val(v, target_name, target_class)
                        if res is not None: return res
                elif isinstance(data, list):
                    for item in data:
                        res = get_inner_val(item, target_name, target_class)
                        if res is not None: return res
                return None

            if not self.output_image:
                self.output_image = get_inner_val(self.request.data, "inputImage", Image)
            if not self.output_detections:
                self.output_detections = get_inner_val(self.request.data, "inputDetections", Detection)

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()