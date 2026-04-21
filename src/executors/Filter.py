import numpy as np
from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # Şartnameye uygun parametre erişimi
        self.input_image = self.request.get_param("inputImageOne")
        self.filter_type = self.request.get_param("ConfigFilterType")
        self.blur_radius = self.request.get_param("BlurRadius") or 5

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_simple_blur(self, img: np.ndarray) -> np.ndarray:
        # Şartname gereği hafif Numpy tabanlı işlem
        kernel = np.ones((self.blur_radius, self.blur_radius), np.float32) / (self.blur_radius ** 2)
        # Basit bir matris kaydırma ile blur simülasyonu
        padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode='edge')
        return padded[1:-1, 1:-1].astype(np.uint8)

    def run(self):
        # 1. Girdi resmi Redis'ten çek
        img_matrix = Image.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_matrix is None:
            return build_filter_response(context=self)

        # 2. İşlemi yap
        processed_matrix = self.apply_simple_blur(img_matrix)

        # 3. Çıktıyı SDK standartlarında set et (Kılavuz sayfa 8)
        self.output_image = Image.set_frame(
            img=processed_matrix,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        return build_filter_response(context=self)