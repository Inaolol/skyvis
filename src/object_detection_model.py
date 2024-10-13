import logging
import time
import requests
import numpy as np

from .constants import classes, landing_statuses
from .detected_object import DetectedObject
from .detected_translation import DetectedTranslation
from ultralytics import YOLO
import cv2
from .position_estimator import PositionEstimator

# do_not_save = False

class ObjectDetectionModel:
    # Base class for team models

    def __init__(self, evaluation_server_url):
        logging.info('Created Object Detection Model')
        if do_not_save:
            print("Not sending predictions to server")
            
        self.evaulation_server = evaluation_server_url
        self.model = YOLO("C:/Users/abdir/Desktop/models/best.pt") 

        self.position_estimator = PositionEstimator()  # Initialize the PositionEstimator
        self.last_health_status = None
        self.last_known_position = None

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

        # Desired FPS
        desired_fps = 3.0
        frame_duration = 1.0 / desired_fps

        frame_count = 0
        start_time = time.time()

        # Load the frame
        frame = image

        if frame is not None:
            
            height, width = frame.shape[:2]
            frame = cv2.resize(frame, (width // 2, height // 2))

            results = self.model(frame, conf=0.4, imgsz=800, device=0)
            # FPS calculation
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                fps = frame_count / elapsed_time
            else:
                fps = 0
            fps_display = f"FPS: {fps:.2f}"

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
            
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            # Display FPS on the frame
            cv2.putText(annotated_frame, fps_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("images Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()

            # Calculate and adjust to the desired FPS
            frame_start_time = time.time()
            time_used = time.time() - frame_start_time
            time_to_sleep = frame_duration - time_used
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
        else:
            print(f"Failed to load image")


        # The health status bit indicates whether the aircraft's satellite communication is healthy.
        # If Health Status is 0, the system should operate; if it is 1, it should send the same incoming data.

        if health_status == '0':
            if self.last_health_status == '1' and self.last_known_position is not None:
                # Health status just changed from 1 to 0, set the initial position
                self.position_estimator.set_initial_position(self.last_known_position[0], self.last_known_position[1])
            
            # Use the PositionEstimator to get the position
            position = self.position_estimator.estimate_position(image)
            pred_translation_x, pred_translation_y = position
        else:
            pred_translation_x = prediction.gt_translation_x
            pred_translation_y = prediction.gt_translation_y
            
            # Update the last known position with ground truth
            self.last_known_position = np.array([float(pred_translation_x), float(pred_translation_y)])
            
            # Reset the position estimator when we get ground truth
            self.position_estimator.reset()

        # Fill in the calculated values for translation to send to the server.
        trans_obj = DetectedTranslation(pred_translation_x, pred_translation_y)
        prediction.add_translation_object(trans_obj)
        # Update the last health status
        self.last_health_status = health_status

        return prediction
    def reset_estimator(self):
        self.position_estimator.reset()
        self.last_known_position = None
        self.last_health_status = None
