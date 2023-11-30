# kafkaPub.py

import logging
import time
from confluent_kafka import Producer
import json
from queue import Queue
import socket
from threading import Thread

logger = logging.getLogger(__name__)


class KafkaPub:
    def __init__(self, config_path: str):
        """Kafka producer """
        # instantiate private attributes and members
        self._run = False
        self._topic = None
        self._config = None
        self._data = {}

        # set up variables
        self.load_config(config_path)
        assert self._config is not None

        # create main objects for threaded class
        self._producer = Producer(self._config)

        self._thread = Thread(target=self._main_thread, args=())
        self._queue = Queue()

    def stop(self) -> None:
        self._run = False
        self._thread.join()

    def start(self) -> None:
        self._run = True
        self._thread.start()

    def add(self, message: dict) -> None:
        self._queue.put(message)

    def _main_thread(self):
        """ Main class thread controlled by start() and stop() """

        logger.info("Starting kafka thread")
        self._run = True
        while self._run:
            if not self._queue.empty():
                pub_message = self._queue.get()
                logger.info(f"Sending payload: {pub_message}")
                self.send(pub_message)

        logger.info("Finished the kafka thread")

    def load_config(self, path) -> None:
        """ Load configuration for Producer from config.json """

        assert path is not None

        try:
            logging.info(f"Loading kafka configuration file: {path}")
            with open(path) as configurations:
                configs = json.load(configurations)
                self._config = configs["bootstrap"]
                self._config["client.id"] = socket.gethostname()
                self._topic = configs["topic"]

                # Log instantiation of configs
                logger.info(f"Producer created | config \t{self._config} | topic \t{self._topic}")

        except IOError:
            logging.error("File not found\t\t\t|  ./config.json")
        except ValueError:
            logging.error("File has invalid json\t\t|  ./config.json")

    def send(self, send_data: dict) -> None:
        """Kafka Producer send applicationData

        Parameters
        ----------
        send_data : `dict`
            Dictionary of applicationData to send

        """
        self._data = send_data
        self._producer.produce(self._topic, json.dumps(self._data), callback=self._delivery_report)
        self._producer.flush()

    def _delivery_report(self, err, msg):
        """Asynchronous callback for producer.produce() that logs results.
        Triggered by poll() or flush().

        Parameters
        ----------
        err : `string`
            Error type
        msg : `string`
            Callback message

        """
        if err is not None:
            logger.warning("Message delivery failed: {}".format(err))
        else:
            logger.debug(f"Delivered | topic=[{msg.topic()}] | partition=[{msg.partition()}] | message=[{self._data}]")
