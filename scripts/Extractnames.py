def extract_file_names(file_path):
    file_names = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Unique names in' in line:
                # Extracts the portion of the line that contains the file name
                start = line.find('Unique names in ') + len('Unique names in ')
                end = line.find('.xml')
                if end != -1:
                    file_name = line[start:end]  # includes '.xml'
                    file_names.append(file_name)
    return file_names

# Path to your text file
file_path = './Desktop/badlabel.txt'
file_names = extract_file_names(file_path)
for name in file_names:
    print(name + '.xml')
