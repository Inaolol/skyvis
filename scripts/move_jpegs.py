import os
import shutil

# Specify the source directory where JPG files are located
source_dir = 'C:/Users/abdir/Documents/'
# Specify the target directory where JPG files should be moved
target_dir = 'C:/Users/abdir/Documents/images'

# Ensure that the target directory exists, if not, create it
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Loop through all files in the source directory
for file in os.listdir(source_dir):
    # Check if the file is a JPG image
    if file.lower().endswith('.jpg'):
        # Construct the full path to the file
        file_path = os.path.join(source_dir, file)
        # Construct the destination path
        destination_path = os.path.join(target_dir, file)
        # Move the file to the target directory
        shutil.move(file_path, destination_path)

print("All JPG files have been moved to:", target_dir)
