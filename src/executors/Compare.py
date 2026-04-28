import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.media.image import Image as SDKImage
from components.DemoPackage.src.utils.response import build_compare_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # 1. SDK ile resmi çekiyoruz (Gelen şey bir Image objesidir)
        img = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        # 2. Objenin ve içindeki saf görüntü matrisinin (value) dolu olduğundan emin ol
        if img is not None and img.value is not None:
            cv_img = img.value  # OpenCV'nin beklediği saf Numpy matrisi

            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k = 15
            if conf.name == "ConfigModeBasic":
                k = int(conf.blurThreshold.value * 30) + 1
            else:
                k = int(conf.kernel.value)

            if k % 2 == 0: k += 1

            # OpenCV işlemini saf matris (cv_img) üzerinde yap
            processed = cv2.GaussianBlur(cv_img, (k, k), 0)

            # 3. İşlenmiş matrisi tekrar Image objesinin içine koy
            img.value = processed

            # 4. Güncellenmiş objeyi Redis'e kaydet
            self.output_image = SDKImage.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()