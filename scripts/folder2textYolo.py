import os
import argparse
import random
from collections import Counter

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument('train_pct', type=int, help="percentage of images to be used for training")
parser.add_argument('valid_pct', type=int, help="percentage of images to be used for validation")
parser.add_argument('yolodataset', type=str, help="path to directory with images and YOLO annotations")
parser.add_argument('--output_dir', type=str, help="directory to save output files", default=None)
args = parser.parse_args()

# Set output directory
if args.output_dir is None:
    args.output_dir = args.yolodataset

# Initialize counter and image list
extensions = []
images = []

# Check file extensions in the folder
for filename in os.scandir(args.yolodataset):
    _, ext = os.path.splitext(filename.name)
    if ext.lower() not in [".txt"]:  # Exclude .txt files
        extensions.append(ext.lower())

# Determine the most common image file extension
ext_dict = Counter(extensions)
extension = max(ext_dict, key=ext_dict.get)
print("Your image file extension is:", extension)

# Gather image files
for filename in os.listdir(args.yolodataset):
    _, ext = os.path.splitext(os.path.basename(filename))
    if ext.lower() == extension:
        images.append(os.path.join(args.yolodataset, filename))

# Calculate number of images for training and validation
number_of_images = len(images)
index_valid = round(number_of_images * args.valid_pct / 100)
validfiles = random.sample(images, index_valid)
trainfiles = list(set(images).difference(set(validfiles)))

# Output the split files
with open(os.path.join(args.output_dir, 'train.txt'), mode='w') as f:
    for item in trainfiles:
        f.write(item + "\n")

with open(os.path.join(args.output_dir, 'valid.txt'), mode='w') as f:
    for item in validfiles:
        f.write(item + "\n")

# Print summary
print('Number of images:', number_of_images)
print('Number of images used for training:', len(trainfiles))
print('Number of images used for validation:', len(validfiles))
