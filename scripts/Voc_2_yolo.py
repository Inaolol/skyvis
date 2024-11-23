import glob
import os
import xml.etree.ElementTree as ET

dirs = ['C:/Users']
output_directory = "C:/Users"
classes = ['Vehicle', 'Human', 'FCP', 'FAL']

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def getImagesInDir(dir_path):
    return glob.glob(dir_path + '/*.jpg')

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

def convert_annotation(dir_path, output_path, image_path, skipped_files):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]
    xml_path = os.path.join(dir_path, f'{basename_no_ext}.xml')
    txt_path = os.path.join(output_path, f'{basename_no_ext}.txt')
    
    try:
        with open(xml_path, 'r', encoding='utf-8') as in_file:
            tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        if size is None:
            print(f"No size information found in {xml_path}. Skipping file.")
            skipped_files.append(xml_path)
            return
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            print(f"Invalid size (width or height is zero) in {xml_path}. Skipping file.")
            skipped_files.append(xml_path)
            return
        
        with open(txt_path, 'w') as out_file:
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in classes:
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(f"{cls_id} {' '.join(map(str, bb))}\n")
    except Exception as e:
        print(f"Failed to process {xml_path}: {str(e)}")
        skipped_files.append(xml_path)

skipped_files_list = []

for dir_path in dirs:
    image_paths = getImagesInDir(dir_path)
    for image_path in image_paths:
        convert_annotation(dir_path, output_directory, image_path, skipped_files_list)

print("Finished processing directories.")
if skipped_files_list:
    print("Some files were skipped due to errors:", skipped_files_list)
