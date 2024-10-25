import os 


def search_files(directory, type, sub_name=None):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(type):
                if sub_name is None or any(name in file for name in sub_name):
                    file_paths.append(os.path.join(root, file))
    return file_paths

