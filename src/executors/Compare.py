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
        # Try-except kaldırıldı; model hatalıysa başlatma sırasında hata vermelidir.
        self.request.model = PackageModel(**(self.request.data))
        self.input_image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # Redis'ten matris olarak çek (image_shape hatasını SDK çözer)
        img_np = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_np is not None:
            # Konfigürasyonu al
            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k = 15
            if conf.name == "ConfigModeBasic":
                k = int(conf.blurThreshold.value * 30) + 1
            else:
                k = int(conf.kernel.value)

            if k % 2 == 0: k += 1

            # Görüntü işleme
            processed = cv2.GaussianBlur(img_np, (k, k), 0)

            # Redis'e geri yaz ve uID içeren objeyi al
            self.output_image = SDKImage.set_frame(img=processed, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()