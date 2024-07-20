import os
import shutil

def move_files(file_list, new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    for file in file_list:
        if os.path.exists(file):
            try:
                shutil.move(file, new_folder)
                print(f"Moved: {file}")
            except Exception as e:
                print(f"Error moving {file}: {e}")
        else:
            print(f"File not found: {file}")

def read_file_list(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    file_list = []
    for line in lines:
        if "No corresponding XML file for" in line or "Orphan file:" in line:
            # Extract the file path
            file_path = line.split(" for ")[-1].strip() if " for " in line else line.split(": ")[-1].strip()
            file_list.append(file_path)
    
    return file_list

if __name__ == '__main__':
    txt_file_path = 'C:/Users/abdir/Desktop/correpted.txt'  # Replace with the path to your text file
    destination_folder = 'C:/Users/abdir/Desktop/Error'  # Replace with the path to your new folder

    files_to_move = read_file_list(txt_file_path)
    move_files(files_to_move, destination_folder)
