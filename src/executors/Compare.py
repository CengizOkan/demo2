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

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # SDK resmi bulamazsa diye zorunlu JSON kazıma aracı (Fallback)
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

        # Önce standart SDK fonksiyonunu dene
        self.input_image = self.request.get_param("inputImage")

        # SDK bulamazsa JSON içinden manuel olarak çıkart
        if not self.input_image:
            self.input_image = extract_value(self.request.data, "inputImage")

        # Elde edilen resmi çıktıya ver
        self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()