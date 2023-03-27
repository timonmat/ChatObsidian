import os
from pathlib import Path
import subprocess

def get_file_list(folder_path, extensions=None):
    if extensions is None:
        extensions = [".md"]

    files = []
    for root, dirs, dir_files in os.walk(folder_path):
        for file in dir_files:
            for ext in extensions:
                if file.endswith(ext):
                    files.append(os.path.join(root, file))
                    break
    return files



def open_finder_to_folder(path: str):
    folder_path = os.path.dirname(path)
    if os.path.exists(folder_path):
        subprocess.run(["open", folder_path])
    else:
        print(f"Folder does not exist: {folder_path}")