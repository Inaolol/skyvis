import os
import argparse

def check_label_existence(images_dir, labels_dir, extension):
    missing_labels = []

    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.endswith(extension):
                image_file = os.path.join(root, file)
                label_file = os.path.join(labels_dir, os.path.relpath(image_file, images_dir)[:-len(extension)] + 'txt')

                if not os.path.exists(label_file):
                    missing_labels.append(image_file)

    if missing_labels:
        print("Images without corresponding label files:")
        for image in missing_labels:
            print(image)
    else:
        print("All images have their corresponding label files.")

parser = argparse.ArgumentParser(
    prog='check_label_existence.py',
    description='Check if all images have their corresponding label files.'
)

parser.add_argument('-i', '--images', help='Images directory.', dest='images_dir', required=True)
parser.add_argument('-l', '--labels', help='Labels directory.', dest='labels_dir', required=True)
parser.add_argument('-e', '--ext', required=False, dest='extension', help='Image extension.', default='jpg')

args = parser.parse_args()

check_label_existence(args.images_dir, args.labels_dir, args.extension)