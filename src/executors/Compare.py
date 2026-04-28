import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.utils.response import build_compare_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        try:
            self.request.model = PackageModel(**(self.request.data))
        except Exception:
            pass

        # 1. Standart SDK Okuması
        self.input_image = self.request.get_param("inputImage")

        # 2. Kurşun Geçirmez Okuma (SDK bulamazsa json içinden zorla çek)
        if not self.input_image:
            try:
                executor_val = self.request.data.get("executor", {}).get("value", {})
                inputs = executor_val.get("value", {}).get("inputs",
                                                           {}) if "value" in executor_val else executor_val.get(
                    "inputs", {})
                if "inputImage" in inputs:
                    self.input_image = inputs["inputImage"].get("value")
            except Exception:
                pass

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Image Load'dan gelen veriyi doğrudan Output'a aktar
        self.output_image = self.input_image
        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()