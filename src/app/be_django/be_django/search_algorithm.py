import os
import time
import mimetypes
from database_handling import insert_file_to_db

def get_metadata(filepath):
    #metadata used as dictionary
    metadata = {'size': os.path.getsize(filepath), 'last_modified': time.ctime(os.path.getmtime(filepath)),
                'creation_time': time.ctime(os.path.getctime(filepath))}

    file_type, _ = mimetypes.guess_type(filepath)
    metadata['file_type'] = file_type if file_type else "unknown"

    #text-based files will use extraction of the first 500 characters as content
    if file_type and 'text' in file_type:
        try:
            with open(filepath, 'r', encoding='utf-u') as file:
                content = file.read(500)
                metadata['preview'] = content
        except Exception as e:
            print(f"Error reading file with the path {filepath}: {e}")
    else:
        metadata['preview'] = ''

    return metadata

def index_files(src_filepath = "."):
    filepath_list = walk_files(src_filepath)
    for filepath in filepath_list:
        metadata = get_metadata(filepath)
        insert_file_to_db(metadata, filepath)

def walk_files(src_filepath="."):
    filepath_list = []
    for root, dirs, files in os.walk(src_filepath):
        for file in files:
            filepath = os.path.join(root, file)
            filepath_list.append(filepath)

    return filepath_list

