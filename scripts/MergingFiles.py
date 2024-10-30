import shutil
import os

def merge_directories(source1, source2, destination):
    os.makedirs(destination, exist_ok=True)  # Ensure the destination directory exists

    # Function to copy all files from source to destination
    def copy_files(source):
        for root, dirs, files in os.walk(source):
            # Path within the new directory
            relative_path = os.path.relpath(root, source)
            dest_path = os.path.join(destination, relative_path)
            os.makedirs(dest_path, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)
                if not os.path.exists(dest_file):  # Check if file does not exist before copying
                    if os.path.exists(src_file):  # Additional check if the source file exists
                        shutil.copy(src_file, dest_file)
                    else:
                        print(f"Warning: {src_file} does not exist and will not be copied.")

    copy_files(source1)
    copy_files(source2)
    print(f"Files from {source1} and {source2} have been merged into {destination}")

# Replace 'source1', 'source2', and 'destination' with the paths to your directories
merge_directories('C:/Users/abdir/Documents/Udemy - English Grammar  Master Course  All Levels  All Topics/[FreeCourseSite.com] Udemy - English Grammar  Master Course  All Levels  All Topics', 'C:/Users/abdir/Desktop/[FreeCourseSite.com] Udemy - English Grammar  Master Course  All Levels  All Topics', 'C:/Users/abdir/Documents/EnglishCourse')
