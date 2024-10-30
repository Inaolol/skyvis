import os
import shutil

def read_prefixes(file_path):
    """Reads file prefixes from a text file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def move_files(source_path, destination_path, prefixes):
    """Moves files with specific prefixes to the destination directory."""
    # Ensure the destination directory exists
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # List all files in the source directory
    files = os.listdir(source_path)
    moved_count = 0

    # Loop through each file
    for file in files:
        # Check if the file starts with any of the prefixes
        if any(file.startswith(prefix) for prefix in prefixes):
            # Supports both .jpg and .xml files
            if file.endswith('.jpg') or file.endswith('.xml'):
                # Move the file
                shutil.move(os.path.join(source_path, file), os.path.join(destination_path, file))
                moved_count += 1

    print(f"Moved {moved_count} files to {destination_path}")

# Paths configuration
source_path = "C:/Users/abdir/Downloads/Compressed/traffic_birdseye_revised/traffic_birdseye"
destination_path = "C:/Users/abdir/Desktop/Annon/tobechacked"
prefix_file = "C:/Users/abdir/Desktop/filenames.txt"

# Read prefixes from file
prefixes = read_prefixes(prefix_file)

# Move the files
move_files(source_path, destination_path, prefixes)
