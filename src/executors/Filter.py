import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from sdks.novavision.src.media.image import Image as SDKImage
from components.DemoPackage.src.utils.response import build_filter_response
from components.DemoPackage.src.models.PackageModel import PackageModel


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections") or []

    def run(self):
        # 1. Obje olarak çek
        img = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        # 2. Saf matrisi çıkar
        if img is not None and img.value is not None:
            cv_img = img.value

            # OpenCV işlemleri
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            # 3. Matrisi objeye geri yükle
            img.value = processed

            # 4. Redis'e gönder
            self.output_image = SDKImage.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        self.output_detections = self.input_detections
        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()