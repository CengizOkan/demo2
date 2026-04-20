"""
İki görüntüyü karşılaştırarak benzerlik skoru ve etiket döndürür.
Histogram veya FeatureBased yöntemi kullanılabilir.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

import cv2
import numpy as np

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackage.src.models.PackageModel import PackageModel
from components.DemoPackage.src.utils.response import build_compare_response


class Compare(Component):
    SIMILARITY_THRESHOLD = 0.6

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.input_image_one = self.request.get_param("inputImageOne")
        self.input_image_two = self.request.get_param("inputImageTwo")
        self.compare_method = self.request.get_param("ConfigCompareMethod")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def compare_histogram(self, img1: np.ndarray, img2: np.ndarray) -> float:
        bins = int(self.request.get_param("HistogramBins") or 256)
        channel = self.request.get_param("HistogramChannel") or "RGB"

        if channel == "Grayscale":
            g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            h1 = cv2.calcHist([g1], [0], None, [bins], [0, 256])
            h2 = cv2.calcHist([g2], [0], None, [bins], [0, 256])
            cv2.normalize(h1, h1)
            cv2.normalize(h2, h2)
            score = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
        else:
            scores = []
            for ch in range(3):
                h1 = cv2.calcHist([img1], [ch], None, [bins], [0, 256])
                h2 = cv2.calcHist([img2], [ch], None, [bins], [0, 256])
                cv2.normalize(h1, h1)
                cv2.normalize(h2, h2)
                scores.append(cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL))
            score = float(np.mean(scores))

        return max(0.0, min(1.0, (score + 1.0) / 2.0))

    def compare_features(self, img1: np.ndarray, img2: np.ndarray) -> float:
        max_kp = int(self.request.get_param("FeatureMaxKeypoints") or 500)
        detector_type = self.request.get_param("FeatureDetector") or "ORB"

        if detector_type == "SIFT":
            detector = cv2.SIFT_create(nfeatures=max_kp)
            norm = cv2.NORM_L2
        else:
            detector = cv2.ORB_create(nfeatures=max_kp)
            norm = cv2.NORM_HAMMING

        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)

        if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
            return 0.0

        matcher = cv2.BFMatcher(norm, crossCheck=True)
        matches = matcher.match(des1, des2)

        if len(matches) == 0:
            return 0.0

        good = [m for m in matches if m.distance < 50]
        score = len(good) / max(len(kp1), len(kp2))
        return max(0.0, min(1.0, score))

    def run(self):
        img1 = Image.get_frame(img=self.input_image_one, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.input_image_two, redis_db=self.redis_db)

        # Karşılaştırma fonksiyonlarına img nesnesinin matrisi (.value) gider
        if self.compare_method == "Histogram":
            score = self.compare_histogram(img1.value, img2.value)
        else:
            score = self.compare_features(img1.value, img2.value)

        self.output_score = float(round(score, 4))
        self.output_label = "Similar" if score >= self.SIMILARITY_THRESHOLD else "Different"

        return build_compare_response(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()