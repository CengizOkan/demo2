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
        img = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img is not None and img.value is not None:
            cv_img = img.value

            conf = self.request.model.configs.executor.value.value.configs.mainConfig.value
            k = 15  # Varsayılan değer (Arayüz boş yollarsa sistem çökmesin diye)

            # Parametreler Optional olduğu için güvenli erişim (getattr)
            if conf.name == "ConfigMode":
                bt = getattr(conf, "blurThreshold", None)
                if bt and bt.value:
                    k = int(bt.value * 30) + 1
            elif conf.name == "ConfigAdvanced":
                ak = getattr(conf, "kernel", None)
                if ak and ak.value:
                    k = int(ak.value)

            if k % 2 == 0: k += 1

            processed = cv2.GaussianBlur(cv_img, (k, k), 0)
            img.value = processed
            self.output_image = SDKImage.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()