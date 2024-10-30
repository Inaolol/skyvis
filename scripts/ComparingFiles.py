import os

def list_files(directory):
    """List all files in a directory recursively, ignoring .vatt files."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.vatt'):  # Filter out .vatt files
                file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list

def compare_directories(dir1, dir2):
    files1 = set(list_files(dir1))
    files2 = set(list_files(dir2))

    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1

    # Print files only in dir1
    if only_in_dir1:
        print(f"Files only in {os.path.basename(dir1)} ({len(only_in_dir1)}):")
        print("\n".join(sorted(only_in_dir1)))
    else:
        print(f"No unique files in {os.path.basename(dir1)}.")

    # Print files only in dir2
    if only_in_dir2:
        print(f"\nFiles only in {os.path.basename(dir2)} ({len(only_in_dir2)}):")
        print("\n".join(sorted(only_in_dir2)))
    else:
        print(f"No unique files in {os.path.basename(dir2)}.")


# Example directories to compare
dir1 = 'C:/Users/abdir/Documents/Udemy - English Grammar  Master Course  All Levels  All Topics/[FreeCourseSite.com] Udemy - English Grammar  Master Course  All Levels  All Topics'
dir2 = 'C:/Users/abdir/Documents/EnglishCourse'
compare_directories(dir1, dir2)
