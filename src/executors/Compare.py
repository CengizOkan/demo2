import numpy as np

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response


class Compare(Component):
    SIMILARITY_THRESHOLD = 0.6

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image_one = self.request.get_param("inputImageOne")
        self.input_image_two = self.request.get_param("inputImageTwo")
        self.compare_method = self.request.get_param("ConfigCompareMethod")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def compare_mse(self, img1: np.ndarray, img2: np.ndarray) -> float:
        # OpenCV boyutlandırma yerine, kırparak MSE (Hata Kareleri Ortalaması) hesaplama
        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])

        c1 = img1[:h, :w].astype(np.float32)
        c2 = img2[:h, :w].astype(np.float32)

        mse = np.mean((c1 - c2) ** 2)
        # Maksimum MSE 65025'tir. Bunu 0-1 arası benzerlik skoruna çeviriyoruz.
        score = 1.0 - (mse / 65025.0)
        return float(max(0.0, min(1.0, score)))

    def run(self):
        img1_matrix = Image.get_frame(img=self.input_image_one, redis_db=self.redis_db)
        img2_matrix = Image.get_frame(img=self.input_image_two, redis_db=self.redis_db)

        if img1_matrix is None or img2_matrix is None:
            self.output_score = 0.0
            self.output_label = "Hata"
            return

        skor = self.compare_mse(img1_matrix, img2_matrix)

        self.output_score = float(skor)
        self.output_label = "Benzer" if skor >= self.SIMILARITY_THRESHOLD else "Farklı"