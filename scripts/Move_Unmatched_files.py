import os
import glob
import shutil

def cleanup_directory(source_directory, destination_directory):
    # Ensure destination directory exists, if not, create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    # Gather all JPG images in the source directory
    image_files = glob.glob(os.path.join(source_directory, '*.jpg'))
    # Gather all XML files in the source directory
    xml_files = glob.glob(os.path.join(source_directory, '*.xml'))
    
    # Create sets of base names without extensions for comparison
    image_base_names = {os.path.splitext(os.path.basename(image))[0] for image in image_files}
    xml_base_names = {os.path.splitext(os.path.basename(xml))[0] for xml in xml_files}
    
    # Find unmatched image files (images without corresponding XML)
    unmatched_images = image_base_names - xml_base_names
    
    # Move unmatched image files
    for image_base in unmatched_images:
        image_path = os.path.join(source_directory, image_base + '.jpg')
        new_location = os.path.join(destination_directory, os.path.basename(image_path))
        shutil.move(image_path, new_location)
        print(f"Moved unmatched image file to: {new_location}")

# Example usage:
source_directory = ''
destination_directory = ''
cleanup_directory(source_directory, destination_directory)
