import sys
import os
import numpy as np

sys.path.append(os.getcwd())

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response

class Compare(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.img1_raw = self.request.get_param("inputImageOne")
        self.img2_raw = self.request.get_param("inputImageTwo")

    def run(self):
        img1 = Image.get_frame(img=self.img1_raw, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.img2_raw, redis_db=self.redis_db)

        if img1 is None or img2 is None:
            self.output_score = 0.0
            self.output_label = "Eksik Girdi"
        else:
            score = float(np.mean(img1 == img2))
            self.output_score = score
            self.output_label = "Benzer" if score > 0.8 else "Farklı"

        return build_compare_response(context=self)

if "__main__" == __name__:
    Executor(sys.argv[1]).run()