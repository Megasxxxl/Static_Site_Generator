import os
import shutil

def copy_files(static_path, public_path):
    if not os.path.exists(public_path):
        os.mkdir(public_path)
        
    files = os.listdir(static_path)

    for file in files:
        formatted_path = os.path.join(static_path, file)
        public_path_file = os.path.join(public_path, file)
        
        if os.path.isfile(formatted_path):
            shutil.copy(formatted_path, public_path_file)
        else:
            copy_files(formatted_path, public_path_file)