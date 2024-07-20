import xml.etree.ElementTree as ET
import os

# Path to the directory containing both XML and JPG files
base_path = "C:/Users/abdir/Desktop/Dataset"

# Mapping of old tags to new tags
tag_changes = {
    'ins': 'Human',
    'insan': 'Human',
    'car'  : 'Vehicle',
    'mot' : 'Vehicle',
    'motor' : 'Vehicle',
    'bus' : 'Vehicle',
    'kam' : 'Vehicle',
    'ismak' : 'Vehicle',
    'tasit' : 'Vehicle',
    'yuap' : 'FCP',
    'uuap' : 'FCP',
    'arac' : 'Vehicle',
    'yaam' :'FAL',
    'uyam' :'FAL',
    'bis' : 'Vehicle',
    'yaya' : 'Human',
    'human' : 'Human',
    'tren' : 'Vehicle',
    'Vichel' : 'Vehicle',
    'yaup'  : 'FCP'
}
# Process each file in the directory
for filename in os.listdir(base_path):
    if filename.endswith(".xml"):  # Process only XML files
        file_path = os.path.join(base_path, filename)
        
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Find all 'object' elements and modify the 'name' child if it matches the tag_changes keys
        for obj in root.findall('object'):
            name = obj.find('name')
            if name.text in tag_changes:
                name.text = tag_changes[name.text]  # Update the tag based on the dictionary
        
        # Save the modified XML back to the file
        tree.write(file_path)
        print(f"Updated {filename}")

print("All XML files have been updated.")
