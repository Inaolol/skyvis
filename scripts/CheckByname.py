import os
import xml.dom.minidom

# Define the path to the directory containing your XML files
annotation_path = "C:/"

# Define a set of names to exclude
exclusions = {'Vehicle', 'Human', 'FCP', 'FAL'}

# List all files in the directory
files = os.listdir(annotation_path)

# Loop over each file in the directory
for file_name in files:
    if file_name.endswith('.xml'):  # Ensure it's an XML file
        # Construct the full file path
        file_path = os.path.join(annotation_path, file_name)
        
        # Parse the XML file
        dom = xml.dom.minidom.parse(file_path)
        
        # Get all 'object' elements
        objects = dom.getElementsByTagName("object")
        
        # Create a set to store unique names
        unique_names = set()

        # Collect all unique names from the 'object' elements
        for obj in objects:
            name = obj.getElementsByTagName('name')[0].firstChild.data
            if name not in exclusions:
                unique_names.add(name)
                
    
        # Print the name of the current file and unique names
      #  print(f"Unique names in {file_name}:")
      #  for name in unique_names:
      #      print(name)
      #  print()  # Adds a newline for better separation between files

       # Print the name of the current file and unique names if there are any
        if unique_names:
            print(f"Unique names in {file_name}:")
            for name in unique_names:
                print(name)
            print()  # Adds a newline for better separation between files
       # else:
       #     print(f"No allowed unique names in {file_name}.\n")
