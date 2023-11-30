from camera.camera import Camera
from model.model import Model
from config.config import logger, Settings
import time
from datetime import datetime
from publish.kafkaPub import KafkaPub


class AppManager:
    def __init__(self):
        self.settings = Settings(_env_file="/application/src/config/.env", _env_file_encoding="utf-8")

        self.model = Model(self.settings.TORCH_MODEL_DIR, self.settings.TORCH_MODEL, self.settings.CLASSES)
        self.camera = Camera(self.settings.CAM_WIDTH, self.settings.CAM_HEIGHT)
        self.publisher = KafkaPub(self.settings.KAFKA_CONFIGS)

    def start(self):
        logger.info("Init completed.")
        self.publisher.start()

        # start by recording the time so that we can guarantee capture on the interval
        last_capture_time = time.time()

        try:
            while True:
                current_time = time.time()

                if current_time - last_capture_time >= self.settings.CAPTURE_DELAY:
                    frame = self.camera.capture()
                    count, frame = self.model.detect(frame, self.settings.THRESHOLD)
                    event_log = {
                        "event": "yes" if count > 0 else "no",
                        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                        "alert_count": int(count),
                    }
                    self.publisher.add(event_log)
                    self.camera.save_frame(frame)
                    last_capture_time = current_time

                # Adjust sleep time to maintain the desired FPS
                elapsed_time = time.time() - current_time
                wait_time = self.settings.CAPTURE_DELAY - elapsed_time
                if wait_time < 0:
                    logger.warning(f"Process speed latency detected. "
                                   f"Processing [{abs(wait_time)} s] "
                                   f" | interval [{self.settings.CAPTURE_DELAY} s]"
                                   f" | elapsed  [{elapsed_time} s]")
                sleep_time = max(0, wait_time)
                time.sleep(sleep_time)

        except Exception as ERR:
            logger.warning(f"Shutting down due to a program error that was caught | {ERR}")
        finally:
            self.stop()

    def stop(self):
        logger.info("Closing connections.")
        self.camera.stop()
        self.publisher.stop()
