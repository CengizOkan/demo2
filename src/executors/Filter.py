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
        try:
            self.request.model = PackageModel(**(self.request.data))
        except:
            pass

    def run(self):
        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections")

        img_np = SDKImage.get_frame(img=self.input_image, redis_db=self.redis_db)

        if img_np is not None:
            # Örnek bir filtre: Grayscale
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.output_image = SDKImage.set_frame(img=processed, package_uID=self.uID, redis_db=self.redis_db)
        else:
            self.output_image = self.input_image

        self.output_detections = self.input_detections
        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()