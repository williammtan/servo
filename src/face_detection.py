import cv2
import time

class FaceDetection:
    def __init__(self):
        # Load cascade
        face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('../data/haarcascade_eye.xml')

        self.cap = cv2.VideoCapture(1)
        self.resolution = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.img = self.get_img()

    def init_video(self, camera_index):
        cap = cv2.VideoCapture(1)
        # wait until cap is opened
        while not cap.isOpened():
            time.sleep(0.01)
        return cap
    
    def get_img(self):
        _, img = self.cap.read()
        return img
    
    def process_img():
        # Process img in video
        pass
