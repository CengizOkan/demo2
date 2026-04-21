import sys
import os
import cv2
import numpy as np

# Path ekleme line importlardan sonraya alındı
sys.path.append(os.getcwd())

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_filter_response


class Filter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image_raw = self.request.get_param("inputImageOne")
        # DependentDropdown altındaki veriye erişim yolu
        conf = self.request.model.configs.executor.value.configs.ConfigFilterType.value
        self.filter_type = conf.value
        self.strength = conf.kernelSize.value

    def run(self):
        img_matrix = Image.get_frame(img=self.input_image_raw, redis_db=self.redis_db)
        if img_matrix is None:
            return build_filter_response(context=self)

        if self.filter_type == "Blur":
            k = self.strength if self.strength % 2 != 0 else self.strength + 1
            processed = cv2.GaussianBlur(img_matrix, (k, k), 0)
        else:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            processed = cv2.filter2D(img_matrix, -1, kernel)

        self.output_image = Image.set_frame(img=processed, package_uID=self.uID, redis_db=self.redis_db)
        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()