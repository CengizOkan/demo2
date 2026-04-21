import os
import sys
import numpy as np
import cv2  # Görüntü işleme için OpenCV kullanıyoruz

# Path ayarı (Package yapısı için kritik)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        # Gelen veriyi Pydantic modelimize giydiriyoruz
        self.request.model = PackageModel(**(self.request.data))

        # Parametrelere güvenli erişim
        self.input_image = self.request.get_param("inputImageOne")
        self.filter_type = self.request.get_param("ConfigFilterType")
        self.blur_radius = self.request.get_param("BlurRadius") or 5

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # 1. Girdi resmi Redis'ten çek
        img_matrix = Image.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_matrix is None:
            return build_filter_response(context=self)

        # 2. Görüntü İşleme (OpenCV)
        if self.filter_type == "Blur":
            k_size = int(self.blur_radius) if int(self.blur_radius) % 2 == 1 else int(self.blur_radius) + 1
            processed = cv2.GaussianBlur(img_matrix, (k_size, k_size), 0)
        else:
            # Sharpening kernel
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            processed = cv2.filter2D(img_matrix, -1, kernel)

        # 3. Çıktıyı SDK standartlarına göre kaydet (Burası Output panelini doldurur)
        self.output_image = Image.set_frame(
            img=processed,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()