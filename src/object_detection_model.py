import logging
import time
import random
import requests
import numpy as np

from .constants import classes, landing_statuses
from .detected_object import DetectedObject
from .detected_translation import DetectedTranslation
from ultralytics import YOLO
import cv2
#from .position_estimator import PositionEstimator

do_not_save = False

class ObjectDetectionModel:
    # Base class for team models

    def __init__(self, evaluation_server_url):
        logging.info('Created Object Detection Model')
        if do_not_save:
            print("Not sending predictions to server")
        self.evaulation_server = evaluation_server_url
        self.model = YOLO("C:/Users/abdir/Desktop/models/best.pt") # initialize your model here.
        # self.position_estimator = PositionEstimator()  # Initialize the PositionEstimator

    @staticmethod
    def download_image(img_url, images_folder, images_files, retries=3, initial_wait_time=0.1):
        t1 = time.perf_counter()
        wait_time = initial_wait_time
        # Check if the frame we want to download exists in the frames.json file
        image_name = img_url.split("/")[-1]
        # If we haven't downloaded the frame before, proceed with downloading
        if image_name not in images_files:
            for attempt in range(retries):
                    try:
                        response = requests.get(img_url, timeout=60)
                        response.raise_for_status()
                        
                        img_bytes = response.content
                        with open(images_folder + image_name, 'wb') as img_file:
                            img_file.write(img_bytes)

                        t2 = time.perf_counter()
                        logging.info(f'{img_url} - Download Finished in {t2 - t1} seconds to {images_folder + image_name}')
                        # Decode the downloaded image
                        bytes_array = np.asarray(bytearray(img_bytes), dtype="uint8")
                        image = cv2.imdecode(bytes_array, 1)
                        
                        return image

                    except requests.exceptions.RequestException as e:
                        logging.error(f"Download failed for {img_url} on attempt {attempt + 1}: {e}")
                        logging.info(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        wait_time *= 2

            logging.error(f"Failed to download image from {img_url} after {retries} attempts.")
        # If we have downloaded the frame before, we can skip downloading
        else:
            logging.info(f'{image_name} already exists in {images_folder}, skipping download.')

    def process(self, prediction, evaluation_server_url, health_status, images_folder, images_files):
        # Download image 

        image = self.download_image(evaluation_server_url + "media" + prediction.image_url, images_folder, images_files)
        if image is None:
            print(f"Failed to download image for prediction: {prediction.image_url}")
            return None  # Return None or handle appropriately when image download fails
        
        try:
            # Perform detection on the downloaded image
            frame_results = self.detect(prediction, health_status, image)
        except Exception as e:
            print(f"Error during detection: {e}")
            return None  # Return None or handle appropriately when detection fails
        
        return frame_results

    def detect(self, prediction, health_status, image):
        # RUN THE YOLO MODEL IN HERE:
        results = self.model(image, conf=0.3, imgsz=800)
        detected_boxes = results[0].boxes

        vehicles = []
        humans = []
        fcp_areas = []
        fal_areas = []

        # Categorize detected objects
        for box in detected_boxes:
            cls = int(box.cls[0])
            x0, y0, x1, y1 = map(int, box.xyxy[0])

            if cls == 0:
                vehicles.append([x0, y0, x1, y1, cls])
            elif cls == 1:
                humans.append([x0, y0, x1, y1, cls])
            elif cls == 2:
                fcp_areas.append([x0, y0, x1, y1, cls])
            elif cls == 3:
                fal_areas.append([x0, y0, x1, y1, cls])

        # Check overlaps and determine landing status
        for area in fcp_areas + fal_areas:
            x0, y0, x1, y1, cls = area
            area_suitable = True

            for obj in vehicles + humans:
                obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
                if obj_x0 < x1 and obj_x1 > x0 and obj_y0 < y1 and obj_y1 > y0:
                    area_suitable = False
                    break

            landing_status = landing_statuses["Inilebilir"] if area_suitable else landing_statuses["Inilemez"]

            # Create DetectedObject instance
            d_obj = DetectedObject(
                cls=cls,
                landing_status=landing_status,
                top_left_x=x0,
                top_left_y=y0,
                bottom_right_x=x1,
                bottom_right_y=y1
            )

            # Add DetectedObject to prediction
            prediction.add_detected_object(d_obj)

        # Create DetectedObject instances for vehicles
        for obj in vehicles:
            obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
            
            d_obj = DetectedObject(
                cls=obj_cls,
                landing_status=landing_statuses["Inis Alani Degil"],  
                top_left_x=obj_x0,
                top_left_y=obj_y0,
                bottom_right_x=obj_x1,
                bottom_right_y=obj_y1
            )
            prediction.add_detected_object(d_obj)

        # Create DetectedObject instances for humans
        for obj in humans:
            obj_x0, obj_y0, obj_x1, obj_y1, obj_cls = obj
            d_obj = DetectedObject(
                cls=obj_cls,
                landing_status=landing_statuses["Inis Alani Degil"],  
                top_left_x=obj_x0,
                top_left_y=obj_y0,
                bottom_right_x=obj_x1,
                bottom_right_y=obj_y1
            )
            prediction.add_detected_object(d_obj)

        # The health status bit indicates whether the aircraft's satellite communication is healthy.
        # If Health Status is 0, the system should operate; if it is 1, it should send the same incoming data.

        if health_status == '0':
            # Use the PositionEstimator to get the position
            position = self.position_estimator.estimate_position(image)
            pred_translation_x, pred_translation_y = position
        else:
            pred_translation_x = prediction.gt_translation_x
            pred_translation_y = prediction.gt_translation_y

        # Fill in the calculated values for translation to send to the server.
        trans_obj = DetectedTranslation(pred_translation_x, pred_translation_y)
        prediction.add_translation_object(trans_obj)

        return prediction
