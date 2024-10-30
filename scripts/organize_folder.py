
import os
import shutil

#this is for listing folder names
# path = 'C:/Users/abdir/Documents/EnglishCourse'
# folders = next(os.walk(path))[1]
# print(folders)




# Define the base path where the folders are located and where to create new folders
base_path = 'C:/Users/abdir/Documents/EnglishCourse'
new_folders = {
    "1 - Beginner": range(2, 29),
    "2 - Intermediate": range(29, 58),
    "3 - Advanced": range(58, 83),
    "4 - common English mistakes": range(83, 87),
}

# Create new folders and move corresponding old folders into them
for new_folder, folder_range in new_folders.items():
    new_folder_path = os.path.join(base_path, new_folder)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    for i in folder_range:
        # Iterate over all folders and find matches by number
        for folder in os.listdir(base_path):
            folder_number = folder.split('.')[0].strip()  # Extract the number, remove any surrounding spaces
            if folder_number.isdigit() and int(folder_number) in folder_range:
                old_folder_path = os.path.join(base_path, folder)
                # Move folder
                shutil.move(old_folder_path, new_folder_path)
                print(f'Moved {folder} to {new_folder_path}')

print("Folders have been consolidated!")