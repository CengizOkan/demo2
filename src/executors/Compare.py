import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.media.image import Image as SDKImage
from components.DemoPackage.src.utils.response import build_compare_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        try:
            self.request.model = PackageModel(**(self.request.data))
        except:
            pass

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # 1. Görüntüyü Yakala (İsimden bağımsız)
        def find_img(d):
            if isinstance(d, dict):
                if "encoding" in d and "value" in d: return d
                for k, v in d.items():
                    res = find_img(v)
                    if res: return res
            elif isinstance(d, list):
                for i in d:
                    res = find_img(i)
                    if res: return res
            return None

        img_dict = find_img(self.request.data)

        if img_dict:
            # 2. REDIS'I BYPASS ET: Doğrudan Base64'ten çöz
            cv_img = SDKImage.decode64(img_dict)

            # 3. Blur Şiddetini Config'den Al
            try:
                conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
                if conf.name == "ConfigMode":
                    k = int(conf.thresholdValue.value * 40) + 1
                else:
                    k = int(conf.kernel.value)
            except:
                k = 15  # Hata durumunda varsayılan

            if k % 2 == 0: k += 1

            # Filtreyi Uygula
            processed = cv2.GaussianBlur(cv_img, (k, k), 0)

            # 4. REDIS'I BYPASS ET: Doğrudan Base64 olarak paketle
            mime = img_dict.get("mime_type", "image/jpeg")
            # ImageModel formatında dict oluşturuyoruz (Redis set_frame yerine)
            self.output_image = {
                "uID": img_dict.get("uID", "demo-uid"),
                "mime_type": mime,
                "encoding": "base64",
                "value": SDKImage.encode64(processed, mime)["value"]
            }
        else:
            self.output_image = None

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()