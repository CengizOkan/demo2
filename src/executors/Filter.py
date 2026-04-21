import numpy as np

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
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
        # OpenCV olmadan basit ve hızlı bir Box Blur işlemi (Matris kaydırma ile)
        radius = int(self.request.get_param("BlurRadius") or 3)
        result = img.copy().astype(np.float32)

        for _ in range(radius):
            padded = np.pad(result, ((1, 1), (1, 1), (0, 0)), mode='edge')
            result = (padded[0:-2, 0:-2] + padded[0:-2, 1:-1] + padded[0:-2, 2:] +
                      padded[1:-1, 0:-2] + padded[1:-1, 1:-1] + padded[1:-1, 2:] +
                      padded[2:, 0:-2] + padded[2:, 1:-1] + padded[2:, 2:]) / 9.0

        return result.astype(np.uint8)

    def apply_sharpen(self, img: np.ndarray) -> np.ndarray:
        # OpenCV olmadan saf Numpy ile keskinleştirme (Laplacian kernel)
        intensity = self.request.get_param("SharpenIntensity") or 1.0
        padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode='edge').astype(np.float32)

        center = padded[1:-1, 1:-1] * 5.0
        top = padded[0:-2, 1:-1]
        bottom = padded[2:, 1:-1]
        left = padded[1:-1, 0:-2]
        right = padded[1:-1, 2:]

        sharpened = center - top - bottom - left - right

        # Yoğunluğa göre orijinal resimle harmanla
        original = img.astype(np.float32)
        result = original + (sharpened - original) * float(intensity)
        return np.clip(result, 0, 255).astype(np.uint8)

    def run(self):
        print("DEBUG: 1 - Filter calismaya basladi!", flush=True)

        img_matrix = Image.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_matrix is None:
            print("DEBUG: HATA! Resim bulunamadi veya Redis'ten okunamadi (img_matrix None).", flush=True)
            return

        print(f"DEBUG: 2 - Resim basariyla alindi. Boyutu: {img_matrix.shape}", flush=True)

        if self.filter_type == "Blur":
            processed_matrix = self.apply_blur(img_matrix)
        else:
            processed_matrix = self.apply_sharpen(img_matrix)

        print("DEBUG: 3 - Filtre uygulandi. Redis'e geri yaziliyor...", flush=True)

        output_img = Image()
        output_img.set_frame(frame=processed_matrix, redis_db=self.redis_db)
        self.output_image = output_img

        print("DEBUG: 4 - Islem TAMAM! Cikti basariyla hazirlandi.", flush=True)