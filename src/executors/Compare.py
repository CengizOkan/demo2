import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.media.image import Image as SDKImage
from sdks.novavision.src.base.model import Image as ImageModel
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
        # 1. SDK ve Fallback ile Resmi Al
        self.input_image = self.request.get_param("inputImage")
        if not self.input_image:
            # Fallback mekanizması (önceki adımda yazdığımız)
            def find_img(d):
                if isinstance(d, dict):
                    if "encoding" in d and "value" in d: return d
                    for k, v in d.items():
                        r = find_img(v)
                        if r: return r
                return None

            self.input_image = find_img(self.request.data)

        # 2. Görüntü İşleme (Blur Uygulama)
        if self.input_image:
            # Base64 -> OpenCV formatı
            cv_img = SDKImage.decode64(self.input_image)

            # Config'den blur değerini al
            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k_size = 15  # Varsayılan

            if conf.name == "ConfigMode":
                k_size = int(conf.thresholdValue.value * 30) or 1
            else:
                k_size = int(conf.advancedKernel.value)

            if k_size % 2 == 0: k_size += 1  # Kernel tek sayı olmalı

            # Filtreyi uygula
            processed = cv2.GaussianBlur(cv_img, (k_size, k_size), 0)

            # OpenCV -> Base64 (SDK Image Model formatı)
            mime = self.input_image.get("mime_type", "image/jpeg") if isinstance(self.input_image, dict) else getattr(
                self.input_image, "mime_type", "image/jpeg")
            self.output_image = SDKImage.encode64(processed, mime)
        else:
            self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()