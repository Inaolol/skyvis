import cv2
import glob
import os
import multiprocessing
import time
from functools import partial
from tqdm import tqdm

# Define class names and colors
CLASSES = ['Vehicle', 'Human', 'FCP', 'FAL']
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Function to convert normalized coordinates to absolute pixel coordinates
def unconvert(width, height, x, y, w, h):
    xmax = int((x * width) + (w * width) / 2.0)
    xmin = int((x * width) - (w * width) / 2.0)
    ymax = int((y * height) + (h * height) / 2.0)
    ymin = int((y * height) - (h * height) / 2.0)
    return (xmin, ymin, xmax, ymax)

# Process each annotation file and corresponding image
def process_annotation(image_dir, output_dir, txt_file):
    img_path = os.path.join(image_dir, os.path.basename(txt_file)[:-3] + 'jpg')
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image file {img_path} not found.")
        height, width = img.shape[:2]
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            data = line.strip().split()
            xmin, ymin, xmax, ymax = unconvert(width, height, float(data[1]), float(data[2]), float(data[3]), float(data[4]))
            class_id = int(data[0])
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), COLORS[class_id], 2)
            cv2.putText(img, CLASSES[class_id], (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLORS[class_id], 2)
        cv2.imwrite(os.path.join(output_dir, os.path.basename(img_path)), img)
    except Exception as e:
        print(f"Error processing {txt_file}: {e}")


if __name__ == '__main__':
    annotation_dir = 'C:/Users/'  # Path to the directory containing annotation files
    image_dir = 'C:/Users/'            # Path to the directory containing image files
    output_dir = 'C:/Users/'           # Path to save processed images

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_time = time.time()
    txt_files = glob.glob(os.path.join(annotation_dir, '*.txt'))
    pool = multiprocessing.Pool()
    func = partial(process_annotation, image_dir, output_dir)

    # Wrap txt_files with tqdm for a progress bar
    for _ in tqdm(pool.imap_unordered(func, txt_files), total=len(txt_files)):
        pass

    pool.map(func, txt_files)
    pool.close()
    pool.join()

    print('Processing completed in {:.2f} seconds.'.format(time.time() - start_time))