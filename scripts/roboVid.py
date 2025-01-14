from inference import InferencePipeline
from inference.core.interfaces.camera.entities import VideoFrame
import cv2
import supervision as sv

# Define a bounding box annotator to draw bounding boxes on the video frame
annotator = sv.BoundingBoxAnnotator()

# Define a label map to adjust class names
label_map = {
    "aVehicle": "Vehic",
    "bHuman" : "Human"
}

def my_custom_sink(predictions: dict, video_frame: VideoFrame):
    # get the text labels for each prediction
    labels = [label_map.get(p["class"], p["class"]) for p in predictions["predictions"]]
    # load our predictions into the Supervision Detections api
    detections = sv.Detections.from_inference(predictions)
    # Adjust the class names in detections
    if "class_name" in detections.data:
        detections.data["class_name"] = [label_map.get(name, name) for name in detections.data["class_name"]]
    # annotate the frame using our supervision annotator, the video_frame, the predictions (as supervision Detections), and the prediction labels
    image = annotator.annotate(
        scene=video_frame.image.copy(), detections=detections, labels=labels
    )
    # display the annotated image
    cv2.imshow("Predictions", image)
    cv2.waitKey(1)

pipeline = InferencePipeline.init(
    model_id="tkno/3",
    video_reference="C:/Users/abdir/Downloads/2023 Örnek Video.mp4",
    on_prediction=my_custom_sink,
)

pipeline.start()
pipeline.join()
