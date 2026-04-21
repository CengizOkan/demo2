import cv2
import numpy as np

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image = self.request.get_param("inputImageOne")
        self.filter_type = self.request.get_param("ConfigFilterType")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_blur(self, img: np.ndarray) -> np.ndarray:
        radius = self.request.get_param("BlurRadius") or 5
        ksize = int(radius) if int(radius) % 2 == 1 else int(radius) + 1
        return cv2.GaussianBlur(img, (ksize, ksize), 0)

    def apply_sharpen(self, img: np.ndarray) -> np.ndarray:
        intensity = self.request.get_param("SharpenIntensity") or 1.0
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)
        center = (kernel.shape[0] // 2, kernel.shape[1] // 2)
        kernel[center] = kernel[center] * float(intensity)

        sharpened = cv2.filter2D(img, -1, kernel)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    def run(self):
        # 1. Görüntüyü numpy matrisi olarak al
        img_matrix = Image.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_matrix is None:
            return  # Eğer giriş resmi yoksa patlamaması için

        # 2. Seçilen filtreyi uygula
        if self.filter_type == "Blur":
            processed_matrix = self.apply_blur(img_matrix)
        else:
            processed_matrix = self.apply_sharpen(img_matrix)

        # 3. ÇIKTI DÖNÜŞÜMÜ (KRİTİK NOKTA)
        # İşlenmiş matrisi NovaVision'ın anladığı Image nesnesine paketliyoruz
        output_img = Image()
        output_img.set_frame(frame=processed_matrix, redis_db=self.redis_db)

        # 4. response.py dosyasının beklediği değişkene ata
        self.output_image = output_img