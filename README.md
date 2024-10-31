# Interface for Competition
This repository has been developed to establish a connection to the Teknofest Artificial Intelligence in Transportation Competition evaluation server (TUYZDS). 
 

# Setup

- Create a virtual environment for the system (Assuming Anaconda is installed).
- We gonna use python=3.8
```shell
$ conda create -n yarisma python=3.8
$ conda activate yarisma
```
- Install the required packages.
```shell
$ pip install -r requirements.txt
```
- Update the contents of the .env file with the team username and passwords provided by Teknofest and save it. (Note: The final path of the file should be ./config/.env).
````text
TEAM_NAME=team_name
PASSWORD=password
EVALUATION_SERVER_URL="SERVER INFORMATION WILL BE SHARED WITH COMPETITORS WHEN THE SERVER IS OPENED"
SESSION_NAME=session_name
````
- Make necessary adjustments and developments in the code, paying attention to the comments.

- To run the system, execute the following command.
````shell
python main.py
````
# Sections you can modify
You can only make changes within the ```object_detection_model.py``` file, without modifying the provided server communication interface code. 
Details about integrating the developed models into the ``ObjectDetectionModel`` class are specified in the code comments. 

## Reviewing Logs
The system logs its operations under the _logs folder during runtime. System errors can be tracked through these log files. 
During the competition, the content of the log file will be considered for any objections.
