import os

def delete_vtt_files(directory):
    # Counter to keep track of how many files have been deleted
    deleted_files_count = 0

    # Walk through all directories and files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".vtt"):
                # Construct full file path
                file_path = os.path.join(root, file)
                # Remove the file
                os.remove(file_path)
                # Increment the counter
                deleted_files_count += 1
                # Print the path of the deleted file
                print(f"Deleted: {file_path}")

    # Print total number of deleted files
    print(f"Total .vtt files deleted: {deleted_files_count}")

# Specify the path to the directory where you want to delete .vtt files
directory_path = "C:/Users/abdir/Documents/EnglishCourse"
delete_vtt_files(directory_path)







import os
import shutil

def consolidate_sections(base_dir, sections):
    # Create the target directories for each section if they don't exist
    for section_name, folder_range in sections.items():
        section_dir = os.path.join(base_dir, section_name)
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)
        
        # Move files from each specified folder in the range into the new section directory
        for folder_num in folder_range:
            folder_path = os.path.join(base_dir, f"{folder_num}. *")  # Adjust this if folder names are different
            if os.path.exists(folder_path):
                # Move all files in this folder to the section folder
                for filename in os.listdir(folder_path):
                    src_file = os.path.join(folder_path, filename)
                    dest_file = os.path.join(section_dir, filename)
                    if not os.path.exists(dest_file):  # Check if file already exists to avoid overwriting
                        shutil.move(src_file, dest_file)
                    else:
                        print(f"File {filename} already exists in {section_name} and will not be moved.")
                # Optionally remove the now empty folder
                os.rmdir(folder_path)
            else:
                print(f"Folder {folder_path} does not exist and will be skipped.")

# Define the base directory and sections
base_directory = "C:/Users/abdir/Documents/EnglishCourse"
sections_info = {
    "Section 1 - Beginner": range(2, 29),
    "Section 2 - Intermediate": range(29, 58),
    "Section 3 - Advanced": range(58, 83),
    "Section 4 - common English mistakes": range(83, 87)  # Assuming folders are inclusively numbered
}

consolidate_sections(base_directory, sections_info)