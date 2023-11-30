# Object Detection with OpenCV and PyTorch

A quick start to object detection with openCV + Pytorch + Kafka

# Table of contents

1. [Overview](#Overview)
2. [Getting Started](#Getting-Started)
3. [Configurations](#Configurations)
4. [References](#References)

---


<a name="Overview"></a>
## Overview


This is a demo project to show how to run inference with the default model as a YoloV5 ultralytics model.
- `OpenCV` to connect with a camera (/dev/video0) and save images to .build/capture
- `Pytorch` load model and run inference on images
- `Kafka` to provide a publisher/subscriber messaging fabric for clients

---


<a name="Getting-started"></a>
## Getting Started

- first, lets' copy the env.example (view more below for how to customize it)

```bash
cp env.example .env
```

- now you are ready to spin it up

```bash

$ docker compose up
[+] Running 3/0
 ✔ Container kafka      Running                                                                                                                                                                                       0.0s 
 ✔ Container kafkacat   Running                                                                                                                                                                                       0.0s 
 ✔ Container inference  Running                                                                                                                                                                                       0.0s 
Attaching to inference, kafka, kafkacat
inference  | 11/30/2023 02:58:14 - thread:140222845712128 - publish.kafkaPub - INFO | Sending payload: {'event': 'no', 'datetime': '2023-11-30T02:58:14', 'alert_count': 0}
kafkacat   | % Reached end of topic test [0] at offset 110
inference  | 11/30/2023 02:58:17 - thread:140222845712128 - publish.kafkaPub - INFO | Sending payload: {'event': 'no', 'datetime': '2023-11-30T02:58:17', 'alert_count': 0}
kafkacat   | % Reached end of topic test [0] at offset 111
```

Notice above that kafkacat is used to receive messages.  You can open a terminal and do some checks

```bash
# check the health of the broker, and list any topics
$ docker exec -it kafkacat kafkacat -b kafka:9092 -L
# subscribe to the topics
$ docker exec -it kafkacat kafkacat -b kafka:9092 -t test -C
```

If you want to see the detections, you can view them in `.build/capture`.  The program will save images, cleaning itself up after every 100 images.


---

<a name="Configurations"></a>
## Configurations

__inference app__
- Check out `env.example` to see some variables that set up the application configs in `src/config/config.py`
- you should create an `.env` in `src/config/.env` so that the application can load it
```text
# model
THRESHOLD=0.6                               // threshold for object detection
TORCH_MODEL_DIR='ultralytics/yolov5'        // model = torch.hub.load(TORCH_MODEL_DIR, TORCH_MODEL, pretrained=True)
TORCH_MODEL='yolov5s'
CLASSES=person                              // the single class label that you want to detect from the model

# camera
CAPTURE_DELAY=1                             // capture a frame every X seconds. FPS=1/CAPTURE_DELAY  
CAM_WIDTH=640                               // resolution from /dev/video0
CAM_HEIGHT=480

# kafka producer                            // path to the json file that describes the server and topic
KAFKA_CONFIGS=/application/src/publish/config.json
```

__kafka server__

- Before doing a build, navigate to `.build` and see three files that set up the kafka server. Click the links below for examples

  - [kafka: server.properties](https://github.com/apache/kafka/blob/trunk/config/server.properties) Sets properties for the kafka server
  - [zookeeper: zookeeper.properties](https://github.com/apache/kafka/blob/trunk/config/zookeeper.properties) Sets properties for the zookeper broker within the kafka server
  - [supervisorD: supervisord.conf](https://supervisord.org/configuration.html) Runs a controlled process in the docker container.

- Notice that `src/publish/config.json` has a field to publish results to the kafka server at `kafka:9092` to a topic named `test`

You do not need to change any of the configurations above, this is just for reference.


---

<a name="References"></a>
## References

__update docker-compose__

- this is for linux machines!
```bash
# check that version is 1.29 or greater
$ docker-compose --version

# remove old version
$ sudo rm /usr/local/bin/docker-compose

# download new version (adjust to a version that you'd like)
$ export COMPOSE_VERSION=1.29.2
$ sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose

# test 
$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
```
---
