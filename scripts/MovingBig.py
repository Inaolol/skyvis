import os
import re
from collections import defaultdict
import shutil

# Define the base path for your images and annotations
base_path = "C:/Users/abdir/Downloads/Compressed/traffic_birdseye_revised/traffic_birdseye"

# Destination path where the sorted folders will be created
destination_base_path = "C:/Users/abdir/Desktop/Big_datasets"

# List all files in the base directory
files = os.listdir(base_path)

# Dictionary to store the groups
file_groups = defaultdict(list)

# Regular expression to match a more general part of the filename before it becomes too specific
pattern = re.compile(r'([a-zA-Z]+[-_a-zA-Z]*)(?:\s|\d|\(|-|\.)')

# Loop through all files
for file in files:
    match = pattern.match(file)
    if match:
        group_key = match.group(1)
        # Normalize the group key to handle case differences and trim excessive delimiters
        group_key = re.sub(r'[-_]+$', '', group_key).lower()
        file_groups[group_key].append(file)

# Create directories based on groups and move files
for group, files in file_groups.items():
    # Ensure the directory exists
    group_dir = os.path.join(destination_base_path, group)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)
    
    # Move each file into the corresponding group directory
    for file in files:
        source_file = os.path.join(base_path, file)
        destination_file = os.path.join(group_dir, file)
        shutil.copy(source_file, destination_file)  # Use shutil.copy(source_file, destination_file) to copy instead of move

    print(f"Copied {len(files)} files to {group_dir}")

