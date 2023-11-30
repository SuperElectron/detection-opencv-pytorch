from pydantic import BaseSettings, Field
from typing import List
import logging
import logging.config

logging.config.fileConfig("/application/src/config/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("event")
seeker_logger = logging.getLogger("seeker")


class Settings(BaseSettings):
    """Class that represents environment variables"""

    THRESHOLD: float = Field(0.6, description="Threshold for the model")
    TORCH_MODEL_DIR: str = Field('ultralytics/yolov5', description="Threshold for the model")
    TORCH_MODEL: str = Field('yolov5s', description="Threshold for the model")

    CLASSES: str = Field('person', description="List of classes to detect")

    CAPTURE_DELAY: int = Field(1, description="Delay between camera capture")
    CAM_HEIGHT: int = Field(1080, description="Desired height of frame from /dev/video0")
    CAM_WIDTH: int = Field(1920, description="Desired width of frame from /dev/video0")

    KAFKA_CONFIGS: str = Field("/application/src/publish/config.json", description="Path to the kafka config file")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        def __repr__(self) -> str:
            return "<Config Environment Class>"

    def __repr__(self) -> str:
        return "<Environment Class>"
