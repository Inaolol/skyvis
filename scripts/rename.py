import os
import multiprocessing
import uuid
import time
import glob
import sys

def convert_images(i):
    try:
        base_name = os.path.splitext(i)[0]
        xml_file = base_name + ".xml"
        if os.path.exists(xml_file):
            name = str(uuid.uuid4())
            new_jpg_name = os.path.join(os.path.dirname(i), f"{name}.jpg")
            new_xml_name = os.path.join(os.path.dirname(xml_file), f"{name}.xml")
            os.rename(i, new_jpg_name)
            os.rename(xml_file, new_xml_name)
        else:
            print(f"No corresponding XML file for {i}")
    except Exception as e:
        print(f"Error processing {i}: {e}")

def check_orphan_files(directory):
    all_files = glob.glob(os.path.join(directory, '*.*'))
    for file in all_files:
        if file.endswith('.jpg') or file.endswith('.xml'):
            base_name = os.path.splitext(file)[0]
            if not (os.path.exists(base_name + '.jpg') and os.path.exists(base_name + '.xml')):
                print(f"Orphan file: {file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python rename.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Provided path is not a directory")
        sys.exit(1)

    start = time.time()

    jpg_files = glob.glob(os.path.join(directory, '*.jpg'))
    pool = multiprocessing.Pool()
    pool.map(convert_images, jpg_files)
    pool.close()
    pool.join()

    check_orphan_files(directory)

    print('Renaming images finished in ' + str(time.time() - start) + ' seconds.')