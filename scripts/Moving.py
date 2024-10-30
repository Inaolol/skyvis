import os
import shutil
from collections import defaultdict

# Define the base path for your images and annotations
base_path = "C:/Users/abdir/Desktop/Annon/checked"

# Define the destination path where folders will be created
destination_base_path = "C:/Users/abdir/Desktop/Annon/sorted"

# List all files in the base directory
files = os.listdir(base_path)

# Dictionary to store the groups
file_groups = defaultdict(list)

# Loop through all files
for file in files:
    # Split the filename to extract the prefix
    split_name = file.rsplit('_', 1)[0]
    # Further refinement to remove numbers or other descriptors following the primary name
    refined_split = ''.join([i for i in split_name if not i.isdigit() and i != '(' and i != ')']).strip()
    # Add the file to the corresponding group
    file_groups[refined_split].append(file)

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
        shutil.move(source_file, destination_file)  # Use shutil.copy(source_file, destination_file) to copy instead of move

    print(f"Moved {len(files)} files to {group_dir}")

