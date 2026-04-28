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
        def find_img(d):
            if isinstance(d, dict):
                if "encoding" in d and "value" in d: return d
                for k, v in d.items():
                    res = find_img(v)
                    if res: return res
            return None

        img_dict = find_img(self.request.data)
        self.input_detections = self.request.get_param("inputDetections") or []

        if img_dict:
            cv_img = SDKImage.decode64(img_dict)
            # Siyah Beyaz Filtre Uygula
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            self.output_image = SDKImage.encode64(processed, img_dict.get("mime_type", "image/jpeg"))
        else:
            self.output_image = img_dict

        self.output_detections = self.input_detections
        return build_filter_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()