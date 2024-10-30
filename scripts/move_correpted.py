import os
import shutil

def move_files(file_list_path, dataset_folder, new_folder):
    # Read the list of files from the text file
    with open(file_list_path, 'r') as file:
        files = file.read().splitlines()

    # Create the destination folder if it doesn't exist
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Process each file in the list
    for xml_file in files:
        xml_path = os.path.join(dataset_folder, xml_file)
        jpg_file = os.path.splitext(xml_file)[0] + '.jpg'
        jpg_path = os.path.join(dataset_folder, jpg_file)

        # Move the XML file
        if os.path.exists(xml_path):
            try:
                shutil.move(xml_path, new_folder)
                print(f"Moved: {xml_path}")
            except Exception as e:
                print(f"Error moving {xml_path}: {e}")
        else:
            print(f"XML file not found: {xml_path}")

        # Move the JPG file
        if os.path.exists(jpg_path):
            try:
                shutil.move(jpg_path, new_folder)
                print(f"Moved: {jpg_path}")
            except Exception as e:
                print(f"Error moving {jpg_path}: {e}")
        else:
            print(f"JPG file not found: {jpg_path}")

if __name__ == '__main__':
    file_list_path = 'C:/Users/abdir/Desktop/badlabel.txt'  # Replace with the path to your text file
    dataset_folder = 'C:/Users/abdir/Desktop/Dataset'  # Replace with the path to your dataset folder
    new_folder = 'C:/Users/abdir/Desktop/Error/badlabel'  # Replace with the path to your new folder

    move_files(file_list_path, dataset_folder, new_folder)
