import cv2 as cv
from datetime import datetime
import os
import shutil
from config.config import logger
import os


class Camera:
    def __init__(self, width: int, height: int):
        self.stream = None

        self._count = 0
        self._max_files_saved = 100
        self._cleanup_count = 0
        self._img_dir = "/tmp/capture"
        self._width = width
        self._height = height

        assert self._height is not None
        assert self._width is not None
        os.makedirs(self._img_dir, exist_ok=True)

        self.connect()
        logger.info(f"Camera setup with args (width=({width}), height={height})")

    def connect(self):
        self.stream = cv.VideoCapture("/dev/video0", cv.CAP_V4L)
        self.stream.set(cv.CAP_PROP_FRAME_WIDTH, self._width)
        self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, self._height)
        if not self.stream.isOpened():
            self.stream.release()
            logger.error("Cannot open camera stream.")
            raise Exception("Error: Cannot open camera stream.")

    def stop(self):
        self.stream.release()
        logger.info("Stream released.")

    def capture(self):
        _, frame = self.stream.read()
        self._count += 1
        self._cleanup_count += 1

        if frame is not None:
            return frame
        else:
            logger.error("Cannot open camera stream.")
            self.stop()
            raise Exception("Error: cannot grab a photo from the camera")

    def save_frame(self, frame):

        if self._cleanup_count == 100:
            self._cleanup_count = 0
            self.clean_folder()

        now = datetime.now()
        cv.imwrite(f"{self._img_dir}/" + f"_{self._count}" + ".png", frame)

    def clean_folder(self):
        for file in os.listdir(self._img_dir):
            if file.endswith(".png"):
                os.remove(file)
