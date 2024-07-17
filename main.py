import logging
from datetime import datetime
from pathlib import Path
from decouple import config
from tqdm import tqdm
from src.connection_handler import ConnectionHandler
from src.frame_predictions import FramePredictions
from src.object_detection_model import ObjectDetectionModel


def configure_logger(team_name):
    log_folder = "./_logs/"
    Path(log_folder).mkdir(parents=True, exist_ok=True)
    log_filename = datetime.now().strftime(log_folder + team_name + '_%Y_%m_%d__%H_%M_%S_%f.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def run():
    print("Started...")
    # Fetch the necessary configuration information from the .env file
    config.search_path = "./config/"
    team_name = config('TEAM_NAME')
    password = config('PASSWORD')
    evaluation_server_url = config("EVALUATION_SERVER_URL")

    # Assign the appropriate configuration to the logger
    configure_logger(team_name)

    # Teams can implement their code within the ObjectDetectionModel class. (OPTIONAL)
    detection_model = ObjectDetectionModel(evaluation_server_url)

    # Connect to the server
    server = ConnectionHandler(evaluation_server_url, username=team_name, password=password)

    # Fetch all frames from the currently active session
    frames_json = server.get_frames()

    # Fetch all translation data from the currently active session
    translations_json = server.get_translations()

    # Retrieve the paths of the folder and files
    images_files, images_folder = server.get_listdir()

    # Run the object detection model frame by frame
    for frame, translation in tqdm(zip(frames_json, translations_json), total=len(frames_json)):
        # Create a prediction object to hold frame and translation information
        predictions = FramePredictions(frame['url'], frame['image_url'], frame['video_name'],
                                       translation['translation_x'], translation['translation_y'])
        # Health status control indicates when the system should activate in the second task
        health_status = translation['health_status']
        # Run the detection model
        predictions = detection_model.process(predictions, evaluation_server_url, health_status, images_folder, images_files)
        # Send the model's prediction values for that frame to the server
        result = server.send_prediction(predictions)


if __name__ == '__main__':
    run()
