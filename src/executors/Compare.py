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
        # 1. Resim Yakalama (Ultimate Hunter)
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
            # 2. OpenCV İşleme
            cv_img = SDKImage.decode64(img_dict)

            # Parametreleri al
            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k_size = 21
            if conf.name == "ConfigMode":
                k_size = int(conf.threshold.value * 40) + 1
            else:
                k_size = int(conf.kernel.value)

            if k_size % 2 == 0: k_size += 1

            # BLUR UYGULA
            processed = cv2.GaussianBlur(cv_img, (k_size, k_size), 0)

            # 3. Geri Dönüş Hazırlığı
            mime = img_dict.get("mime_type", "image/jpeg")
            self.output_image = SDKImage.encode64(processed, mime)
        else:
            # Fallback (ImageView çökmesin diye)
            self.output_image = {"uID": "err", "mime_type": "image/png", "encoding": "base64",
                                 "value": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="}

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()