import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.media.image import Image as SDKImage  # Redis I/O için
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
        # 1. Giriş Parametresini Al
        self.input_image = self.request.get_param("inputImage")

        # 2. Redis'ten Numpy Array olarak çek
        img_np = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_np is not None:
            # 3. Blur Şiddetini Config'den oku
            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k = 15
            if conf.name == "ConfigMode":
                k = int(conf.thresholdValue.value * 40) + 1
            elif conf.name == "ConfigAdvanced":
                k = int(conf.kernel.value)

            if k % 2 == 0: k += 1
            if k < 1: k = 1

            # OPENCV BLUR UYGULA
            processed = cv2.GaussianBlur(img_np, (k, k), 0)

            # 4. Sonucu Redis'e yaz (uID üretir)
            self.output_image = SDKImage.set_frame(img=processed, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()