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

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        self.input_image = self.request.get_param("inputImage")
        self.input_detections = self.request.get_param("inputDetections")

        if self.input_image:
            cv_img = SDKImage.decode64(self.input_image)
            # Basit bir filtreleme (Grayscale örneği)
            processed = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

            mime = self.input_image.get("mime_type", "image/jpeg") if isinstance(self.input_image, dict) else getattr(
                self.input_image, "mime_type", "image/jpeg")
            self.output_image = SDKImage.encode64(processed, mime)
        else:
            self.output_image = self.input_image

        self.output_detections = self.input_detections

        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()