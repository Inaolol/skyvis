from inference import get_model
import supervision as sv
import cv2


image_file = ""
image = cv2.imread(image_file)
model = get_model(model_id="tkno/10")

results = model.infer(image, confidence=0.3)[0]

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results)

# Define a label map to adjust class names
label_map = {
    "aVehicle": "Vehicle",
    "bHuman" : "Human"
}

# Adjust the labels in detections
if "class_name" in detections.data:
    detections.data["class_name"] = [label_map.get(name, name) for name in detections.data["class_name"]]

# create supervision annotators
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with roboflow inference results
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)


# display the image
sv.plot_image(annotated_image)
