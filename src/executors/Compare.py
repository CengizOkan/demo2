import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.base.model import Image
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
        self.output_image = None

        # 1. En Güvenli Yöntem: Pydantic modeli üzerinden saf Image objesine erişim
        try:
            req_data = self.request.model.configs.executor.value.value
            if req_data and req_data.inputs and req_data.inputs.inputImage:
                # Bu değer zaten platformun beklediği %100 orijinal Image objesidir
                self.output_image = req_data.inputs.inputImage.value
        except Exception:
            pass

        # 2. Alternatif Yöntem: Sadece 'value' içindeki orijinal veriyi çıkaran Fallback
        if not self.output_image:
            def get_inner_image(data):
                if isinstance(data, dict):
                    if data.get("name") == "inputImage" and "value" in data:
                        val = data["value"]
                        if isinstance(val, dict): return Image(**val)
                        if isinstance(val, list): return [Image(**v) if isinstance(v, dict) else v for v in val]
                    for k, v in data.items():
                        res = get_inner_image(v)
                        if res is not None: return res
                elif isinstance(data, list):
                    for item in data:
                        res = get_inner_image(item)
                        if res is not None: return res
                return None

            self.output_image = get_inner_image(self.request.data)

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()