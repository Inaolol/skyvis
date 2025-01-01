# Define the classes
classes = ['Vehicle', 'Human', 'FCP', 'FAL']

# Specify the path to the output text file
output_file_path = 'C:/Users/'

# Open the file at the specified path in write mode
with open(output_file_path, 'w') as f:
    # Write each class name to the file on a new line
    for cls in classes:
        f.write(cls + '\n')

print("Class names have been saved to:", output_file_path)
