import os
import glob

def cleanup_directory(directory):
    # Gather all JPG images in the directory
    image_files = glob.glob(os.path.join(directory, '*.jpg'))
    # Gather all XML files in the directory
    xml_files = glob.glob(os.path.join(directory, '*.xml'))
    
    # Create sets of base names without extensions for comparison
    image_base_names = {os.path.splitext(os.path.basename(image))[0] for image in image_files}
    xml_base_names = {os.path.splitext(os.path.basename(xml))[0] for xml in xml_files}
    
    # Find unmatched image files (images without corresponding XML)
    unmatched_images = image_base_names - xml_base_names
    # Find unmatched XML files (XMLs without corresponding images)
    unmatched_xmls = xml_base_names - image_base_names
    
    # Delete unmatched image files
    for image_base in unmatched_images:
        image_path = os.path.join(directory, image_base + '.jpg')
        os.remove(image_path)
        print(f"Deleted unmatched image file: {image_path}")

    # Delete unmatched XML files
    for xml_base in unmatched_xmls:
        xml_path = os.path.join(directory, xml_base + '.xml')
        os.remove(xml_path)
        print(f"Deleted unmatched XML file: {xml_path}")

# Example usage:
directory = ''
cleanup_directory(directory)
