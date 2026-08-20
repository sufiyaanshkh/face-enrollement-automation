from insightface.app import FaceAnalysis
import cv2


class FaceDetector:
    def __init__(self, det_size=(640, 640), ctx_id=-1):
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=ctx_id, det_size=det_size)

    def detect_faces(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError('Image could not be read')
        return self.app.get(image)
