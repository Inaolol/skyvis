import os
import multiprocessing
import time
import argparse
import shutil

def train_mover(i):
    i = i.strip()  # Using strip() to remove any extra whitespace or newlines
    shutil.move(os.path.join(image_label_path, i), os.path.join(image_label_path, "images/train"))
    shutil.move(os.path.join(image_label_path, i[:-3] + 'txt'), os.path.join(image_label_path, "labels/train"))

def val_mover(i):
    i = i.strip()  # Using strip() to remove any extra whitespace or newlines
    shutil.move(os.path.join(image_label_path, i), os.path.join(image_label_path, "images/val"))
    shutil.move(os.path.join(image_label_path, i[:-3] + 'txt'), os.path.join(image_label_path, "labels/val"))

parser = argparse.ArgumentParser(description='Move files into train and val directories.')
parser.add_argument('text_directory', type=str, help='Directory where train.txt and valid.txt are located')
parser.add_argument('image_label_path', type=str, help='Directory where the images and their txt labels are located')
args = parser.parse_args()

text_directory = args.text_directory
image_label_path = args.image_label_path

start = time.time()
if __name__ == '__main__':
    os.makedirs(os.path.join(image_label_path, 'images/train'), exist_ok=True)
    os.makedirs(os.path.join(image_label_path, 'images/val'), exist_ok=True)
    os.makedirs(os.path.join(image_label_path, 'labels/train'), exist_ok=True)
    os.makedirs(os.path.join(image_label_path, 'labels/val'), exist_ok=True)

    with open(os.path.join(text_directory, 'train.txt')) as f:
        train_lines = f.readlines()
    with open(os.path.join(text_directory, 'valid.txt')) as f:
        val_lines = f.readlines()

    # Create multiprocessing pool for moving train files
    pool = multiprocessing.Pool()
    pool.map(train_mover, train_lines)
    pool.close()
    pool.join()
    print('Moving train finished in ' + str(time.time() - start) + ' seconds.')

    # Reset start time and create another multiprocessing pool for moving validation files
    start = time.time()
    pool = multiprocessing.Pool()
    pool.map(val_mover, val_lines)
    pool.close()
    pool.join()
    print('Moving validation finished in ' + str(time.time() - start) + ' seconds.')