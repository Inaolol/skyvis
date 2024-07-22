import os
import cv2
import xml.dom.minidom

# Define the path where both images and XML files are stored
data_path = "C:/Users/abdir/Desktop/Big_datasets"

# Define the output path for visualized images
output_path = "C:/Users/abdir/Desktop/Big_datasets/checked"
os.makedirs(output_path, exist_ok=True)

# List all files in the directory
files = os.listdir(data_path)

# Filter out only image files if they have a corresponding XML file
image_files = [f for f in files if f.endswith('.jpg') and os.path.splitext(f)[0] + '.xml' in files]

# Process each image file
for image_file in image_files:
    img_path = os.path.join(data_path, image_file)
    xml_path = os.path.join(data_path, os.path.splitext(image_file)[0] + '.xml')
    
    print("Processing:", img_path)
    img = cv2.imread(img_path)
    if img is None:
        continue

    # Parse the XML file
    dom = xml.dom.minidom.parse(xml_path)
    objects = dom.getElementsByTagName("object")

    # Draw rectangles around annotated objects
    for obj in objects:
        bndbox = obj.getElementsByTagName('bndbox')[0]
        xmin = int(bndbox.getElementsByTagName('xmin')[0].childNodes[0].data)
        ymin = int(bndbox.getElementsByTagName('ymin')[0].childNodes[0].data)
        xmax = int(bndbox.getElementsByTagName('xmax')[0].childNodes[0].data)
        ymax = int(bndbox.getElementsByTagName('ymax')[0].childNodes[0].data)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (55, 255, 155), 5)

    # Save the modified image
    output_filename = os.path.join(output_path, image_file)
    cv2.imwrite(output_filename, img)
    print("Saved visualized image to", output_filename)

print("All processing complete.")
