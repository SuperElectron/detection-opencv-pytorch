import torch
import cv2


class Model:
    def __init__(self, model_dir:str, model: str, classes: str):
        self.model = torch.hub.load(model_dir, model, pretrained=True)
        self.model.eval()
        self._bbox_color = (0, 255, 0)
        self._text_color = (255, 255, 255)
        self._detection_label = classes

    def detect(self, image, threshold=0.8):
        results = self.model([image])
        df = results.pandas().xyxy[0]

        num_detections = 0

        for _, row in df.iterrows():
            if row["name"] == self._detection_label and row["confidence"] >= threshold:
                num_detections += 1
                x1, y1, x2, y2 = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])
                confidence = row["confidence"]

                # Draw bounding box
                image = cv2.rectangle(image, (x1, y1), (x2, y2), self._bbox_color, 2)

                # Put confidence text above the bounding box
                text = f"Confidence: {confidence:.2f}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

                text_x = max(x1, 0)
                text_y = max(y1 - 5, text_size[1])

                image = cv2.putText(image, text, (text_x, text_y), font, font_scale, self._text_color, font_thickness)

                logger.info(f"Detected {row['name']}")

        return num_detections, image
