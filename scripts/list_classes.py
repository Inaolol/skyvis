import os
import argparse

def extract_class_ids_from_file(file_path, classes):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            class_id = line.strip().split(' ')[0]
            if class_id not in classes:
                print(f"New class ID found: {class_id}")
                classes.add(class_id)

def extract_class_ids_from_directory(directory, classes):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                extract_class_ids_from_file(file_path, classes)

parser = argparse.ArgumentParser(
    prog='list_classes.py',
    description='List class IDs from YOLO labels in a directory and its subfolders.'
)

parser.add_argument('-d', '--dir', help='Directory of YOLO labels', dest='dir', required=True)
args = parser.parse_args()

classes = set()

extract_class_ids_from_directory(args.dir, classes)

print("Unique class IDs:")
print(classes)
