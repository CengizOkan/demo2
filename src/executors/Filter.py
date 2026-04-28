import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.base.model import Image, Detection  # BU SATIRI EKLE
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
        def extract_value(data, key):
            if isinstance(data, dict):
                if data.get("name") == key and "value" in data:
                    return data.get("value")
                if key in data and isinstance(data[key], dict) and "value" in data[key]:
                    return data[key].get("value")
                for k, v in data.items():
                    res = extract_value(v, key)
                    if res is not None:
                        return res
            elif isinstance(data, list):
                for item in data:
                    res = extract_value(item, key)
                    if res is not None:
                        return res
            return None

        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections")

        if not self.input_image:
            self.input_image = extract_value(self.request.data, "inputImage")
        if not self.input_detections:
            self.input_detections = extract_value(self.request.data, "inputDetections")

        # Image objesi için Casting
        if isinstance(self.input_image, dict):
            self.output_image = Image(**self.input_image)
        elif isinstance(self.input_image, list):
            self.output_image = [Image(**item) if isinstance(item, dict) else item for item in self.input_image]
        else:
            self.output_image = self.input_image

        # Detection objesi için Casting
        if isinstance(self.input_detections, dict):
            self.output_detections = Detection(**self.input_detections)
        elif isinstance(self.input_detections, list):
            self.output_detections = [Detection(**item) if isinstance(item, dict) else item for item in self.input_detections]
        else:
            self.output_detections = self.input_detections

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()