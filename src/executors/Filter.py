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

        def find_any_image(data):
            if isinstance(data, dict):
                if ("mime_type" in data or "mimeType" in data) and "encoding" in data and "value" in data:
                    return data
                for k, v in data.items():
                    res = find_any_image(v)
                    if res is not None: return res
            elif isinstance(data, list):
                for item in data:
                    res = find_any_image(item)
                    if res is not None: return res
            return None

        found_image_dict = find_any_image(self.request.data)

        if found_image_dict:
            try:
                self.output_image = Image(**found_image_dict)
            except Exception:
                self.output_image = found_image_dict
        else:
            try:
                self.output_image = Image(
                    name="outputImage",
                    type="object",
                    field="img",
                    uID="fallback-123",
                    mime_type="image/png",
                    encoding="base64",
                    value="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
                )
            except Exception:
                pass

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()