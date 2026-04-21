import cv2
import numpy as np

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from novavision.DemoPackage.models.PackageModel import PackageModel
from novavision.DemoPackage.utils.response import build_filter_response


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
        mode = self.request.get_param("BlurMode") or "Gaussian"

        ksize = int(radius) if int(radius) % 2 == 1 else int(radius) + 1
        ksize = max(1, ksize)

        if mode == "Gaussian":
            return cv2.GaussianBlur(img, (ksize, ksize), 0)
        else:
            return cv2.medianBlur(img, ksize)

    def apply_sharpen(self, img: np.ndarray) -> np.ndarray:
        intensity = self.request.get_param("SharpenIntensity") or 1.0
        kernel_size = self.request.get_param("SharpenKernel") or "Small"

        if kernel_size == "Small":
            kernel = np.array([
                [0, -1,  0],
                [-1,  5, -1],
                [0, -1,  0]
            ], dtype=np.float32)
        else:
            kernel = np.array([
                [ 0,  0, -1,  0,  0],
                [ 0, -1, -2, -1,  0],
                [-1, -2, 17, -2, -1],
                [ 0, -1, -2, -1,  0],
                [ 0,  0, -1,  0,  0]
            ], dtype=np.float32)

        center = (kernel.shape[0] // 2, kernel.shape[1] // 2)
        kernel[center] = kernel[center] * float(intensity)

        sharpened = cv2.filter2D(img, -1, kernel)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    def run(self):
        img = Image.get_frame(img=self.input_image, redis_db=self.redis_db)

        # OpenCV fonksiyonlarına sadece matris (.value) gönderilir
        if self.filter_type == "Blur":
            img.value = self.apply_blur(img.value)
        else:
            img.value = self.apply_sharpen(img.value)

        self.output_image = Image.set_frame(
            img=img,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()