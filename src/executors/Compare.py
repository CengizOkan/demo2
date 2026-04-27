import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response


class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image_one = self.request.get_param("inputImageOne")
        self.input_image_two = self.request.get_param("inputImageTwo")

    def run(self):
        img1 = Image.get_frame(img=self.input_image_one, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.input_image_two, redis_db=self.redis_db)

        if img1 is None or img2 is None:
            self.output_score = 0.0
            self.output_label = "Görüntü Eksik"
            return build_compare_response(context=self)

        # Basit benzerlik
        score = float(np.mean(img1 == img2))
        self.output_score = score
        self.output_label = "Benzer" if score > 0.8 else "Farklı"

        return build_compare_response(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()