import os
from pathlib import Path


def get_file_list(folder_path):
        files = []
        for root, dirs, dir_files in os.walk(folder_path):
            for file in dir_files:
                if file.endswith(".md"):
                    files.append(os.path.join(root, file))
        return files