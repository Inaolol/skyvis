import json
import logging
import requests
import time
import os
from decouple import config


class ConnectionHandler:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.auth_token = None
        self.classes = None
        self.frames = None
        self.translations = None
        self.frames_file = "frames.json"  # Saved frames file 
        self.translations_file = "translations.json"  # Saved translations file
        self.video_name = ''
        self.img_save_path = './_images/'
        

        # Define URLs
        self.url_login = self.base_url + "auth/"
        self.url_frames = self.base_url + "frames/"
        self.url_translations = self.base_url + "translation/"
        self.url_prediction = self.base_url + "prediction/"
        self.url_session = self.base_url + "session/"

        if username and password:
            self.login(username, password)

    def login(self, username, password):
        payload = {'username': username, 'password': password}
        files = []
        try:
            response = requests.post(self.url_login, data=payload, files=files, timeout=10)
            response_json = json.loads(response.text)
            if response.status_code == 200:
                self.auth_token = response_json['token']
                logging.info("Login Successfully Completed : {}".format(payload))
            else:
                logging.error("Login Failed : {}".format(response.text))
        except requests.exceptions.RequestException as e:
            logging.error(f"Login request failed: {e}")           


    def write_to_env(self, session_name=None):
        found = False
        change = False
        # Write session name to environment configuration file.
        with open("./config/.env", "r+") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # line check
                if line.startswith("SESSION_NAME="):
                    if session_name == line.split("=")[-1].strip():
                        found = True
                        logging.info(f"{session_name} json exists, returning..")
                        return line.split("=")[-1].strip()
                    else:
                        # exists but different
                        lines[i] = f"SESSION_NAME={session_name}\n"
                        change = True

            if change:
                f.seek(0)
                f.writelines(lines)
                f.truncate()
                logging.info(f"Changed the session to {session_name}")
                return session_name       

            if not found:
                # case1, no session_name
                lines.append(f"\nSESSION_NAME={session_name}\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()
                logging.info(f"Entered the session of {session_name}")
            
            return session_name

    def get_session_name(self):
        # Retrieve the predefined session name from the config file.
        # If the session name is not defined in the config file, it is obtained from the server by request.
        config.search_path = "../config/"
        return config("SESSION_NAME")
    def create_img_folder(self, path):
        # Create a directory for saving images.
        post_path = os.path.join(self.img_save_path, path)
        os.makedirs(post_path, exist_ok=True)        
    
    def get_listdir(self):
        # Get the list of files in the current video's image save path.
        save_path = os.path.join(self.img_save_path, self.video_name)
        return os.listdir(save_path), os.path.join(save_path)

    def save_frames_to_file(self, frames):
         # Save frames data to a JSON file.
        try:
            self.video_name = frames[0]['video_name'] + '/'
            # create the dir
            self.create_img_folder(self.video_name)
            # update the dir
            self.write_to_env(frames[0]['video_name'])
            
            frames_path = os.path.join(self.img_save_path, self.video_name, self.frames_file)
            
            with open(frames_path, 'w') as f:
                json.dump(frames, f)
            logging.info(f"Frames saved to {frames_path}")
        except IndexError as e:
            logging.error(f"{e} has occured!")
            raise 
        
    def load_frames_from_file(self, session_name):
        # Load downloaded frames directly from the directory without redownloading them.
        # Example: "_images/Test_Session" to load frames from the path.
        base_path = os.path.join(self.img_save_path, session_name, self.frames_file)
        dirs = os.listdir(self.img_save_path)
        if session_name in dirs:
            if os.path.exists(base_path):
                with open(base_path, 'r') as f:
                    frames = json.load(f)
                logging.info(f"Frames loaded from {base_path}")
                return frames
        logging.warning(f"{base_path} does not exist.")
        return None
    
    def get_frames(self, retries=3, initial_wait_time=0.1):
        """
        Note: Within a minute, a maximum of 5 get_frames requests can be made.
        This restriction is set to prevent contestants from overloading the server with unnecessary requests during the competition.
        Contestants are responsible for considering this limit while using the get_frames function.

        """
        try:
            # Check if the _images directory exists
            if os.path.exists(self.img_save_path):
                # If the _images directory does exist, get the session name
                session_name = self.get_session_name()
                # If there are previously downloaded frames, load them from the file.
                frames = self.load_frames_from_file(session_name)
                        # If the file containing the frames is not empty
                if frames:
                    self.video_name = session_name + "/"
                    logging.info("Frames file exists. Loading frames from file.")
                    return frames
        except:
            logging.info("Frames file exists, but it is corrupted.")


        payload = {}
        headers = {'Authorization': 'Token {}'.format(self.auth_token)}
        wait_time = initial_wait_time

        # Set our function to attempt three times in a row
        for attempt in range(retries):
            try:
                # Send a GET request to the server to fetch the file path of the frames.
                # Here, the timeout value is set to 60 seconds.
                response = requests.get(self.url_frames, headers=headers, data=payload, timeout=60)
                self.frames = json.loads(response.text)
                # If the GET request is successful, save the frames to the appropriate folder
                if response.status_code == 200:
                    logging.info("Successful : get_frames : {}".format(self.frames))
                    self.save_frames_to_file(self.frames)
                    return self.frames
                else:
                    # Log the failure if otherwise
                    logging.error("Failed : get_frames : {}".format(response.text))
            except requests.exceptions.RequestException as e:
                logging.error(f"Get frames request failed: {e}")

            # If we are not successful in our attempt, wait for a short while and then resend our request to the server.
            logging.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2

        logging.error("Failed to get frames after multiple retries. Loading frames from file.")
        return self.load_frames_from_file(session_name)


    def save_translations_to_file(self, translations):
        try:
            translations_path = os.path.join(self.img_save_path, self.video_name, self.translations_file)

            with open(translations_path, 'w') as f:
                json.dump(translations, f)

            logging.info(f"Translations saved to {translations_path}")
        except:
            logging.warning("An error has occurred")

    def load_translations_from_file(self, session_name):
        # e.g. "_images/2024_tuyz_xxx/"
        base_path = os.path.join(self.img_save_path, session_name, self.translations_file)
        dirs = os.listdir(self.img_save_path)
        if session_name in dirs:
            if os.path.exists(base_path):
                with open(base_path, 'r') as f:
                    translations = json.load(f)
                logging.info(f"Translations loaded from {base_path}")
                return translations
        logging.warning(f"{base_path} does not exist.")
        return None

    def get_translations(self, retries=3, initial_wait_time=0.1):
        """
        Note: A team can make a maximum of 5 get_frames requests within a minute.
        This restriction is defined to prevent unnecessary requests during the competition,
        which can overload the server. It is the responsibility of the competitors to
        consider this restriction when using the get_frames function.
        """
        try:
            # Check if the _images folder exists
            if os.path.exists(self.img_save_path):
                # If the _images folder has been created, retrieve our session name
                session_name = self.get_session_name()
                # If there are previously downloaded translations, load those frames from the file.
                translations = self.load_translations_from_file(session_name)
                # If the file containing the translations is not empty
                if translations:
                    logging.info("Translations file exists. Loading translations from file.")
                    return translations
        except:
            logging.info("Translation JSON exists, but it is corrupted.")

        payload = {}
        headers = {'Authorization': 'Token {}'.format(self.auth_token)}
        wait_time = initial_wait_time

        for attempt in range(retries):
            try:
                # Send a GET request to the server to fetch the file path of the frames.
                # Here, the timeout value is set to 60 seconds.
                response = requests.get(self.url_translations, headers=headers, data=payload, timeout=60)
                self.translations = json.loads(response.text)
                # If the GET request is successful, save the translations to the appropriate folder
                if response.status_code == 200:
                    logging.info("Successful : get_translations : {}".format(self.translations))
                    self.save_translations_to_file(self.translations)
                    return self.translations
                else:
                    # Log the failure if otherwise
                    logging.error("Failed : get_translations : {}".format(response.text))
            except requests.exceptions.RequestException as e:
                logging.error(f"Get translations request failed: {e}")

            # If we are not successful in our attempt, wait for a short while and then resend our request to the server.
            logging.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2

        logging.error("Failed to get translations after multiple retries. Loading translations from file.")
        return self.load_translations_from_file(session_name)

    def send_prediction(self, prediction, retries=3, initial_wait_time=0.1):
        """
        Note: A team can send predictions for a maximum of 80 frames within a minute.
        This restriction is defined to prevent unnecessary requests during the competition,
        which can overload the server. It is the responsibility of the competitors to
        consider this restriction when using the send_prediction function.

        Suggestion: Keep track of the number of requests sent within a minute and, if the system
        is running fast, delay (wait() etc.). If the maximum request limit is exceeded, the server
        will not save the sent prediction to the database. Therefore, submissions that exceed
        the request limit will not be evaluated. When the request limit is exceeded, the server
        returns the following response:
            {"detail":"You do not have permission to perform this action."}
        Additionally, competitors can design a mechanism to resend the unsent prediction to the server
        if they receive a response indicating a failed submission from the server.
        """


        payload = json.dumps(prediction.create_payload(self.base_url))
        files = []
        headers = {
            'Authorization': 'Token {}'.format(self.auth_token),
            'Content-Type': 'application/json',
        }
        wait_time = initial_wait_time

        for attempt in range(retries):
            try:
                response = requests.post(self.url_prediction, headers=headers, data=payload, files=files, timeout=60)
                # If we are able to send the prediction successfully for the relevant frame
                if response.status_code == 201:
                    logging.info("Prediction sent successfully. \n\t{}".format(payload))
                    return response
                # If we could not send the prediction because we have already sent it for the relevant frame, log it and
                # exit the loop. Do not attempt to send predictions for the same frame repeatedly
                elif response.status_code == 406:
                    logging.error("Prediction send failed - 406 Not Acceptable. Already sent. \n\t{}".format(response.text))
                    return response
                # Log if we cannot send the prediction for any other reason than having already sent it
                else:
                    logging.error("Prediction send failed. \n\t{}".format(response.text))
                    response_json = json.loads(response.text)
                    if "You do not have permission to perform this action." in response_json.get("detail", ""):
                        logging.info("Limit exceeded. 80frames/min \n\t{}".format(response.text))
                        return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Prediction request failed: {e}")

            # Wait for a certain period and try to send the prediction again for the relevant frame
            logging.info(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2

        logging.error("Failed to send prediction after multiple retries.")
        return None