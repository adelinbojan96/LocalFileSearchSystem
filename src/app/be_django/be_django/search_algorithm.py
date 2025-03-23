import os
import time
import mimetypes
from .database_handling import insert_file_to_db

def get_metadata(filepath):
    try:
        stats = os.stat(filepath)
        return {
            'filename': os.path.basename(filepath),
            'path': filepath,
            'size': stats.st_size,  #bytes
            'last_modified': stats.st_mtime,  #timestamp
            'creation_time': stats.st_ctime,  #timestamp
            'file_type': mimetypes.guess_type(filepath)[0] or 'unknown',
            'preview': get_file_preview(filepath)
        }
    except Exception as e:
        print(f"Metadata error for {filepath}: {str(e)}")
        return None


def get_file_preview(filepath):
    try:
        file_type = mimetypes.guess_type(filepath)[0]
        if file_type and 'text' in file_type:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(500)
        return ''
    except Exception as e:
        print(f"Preview error for {filepath}: {str(e)}")
        return ''


def index_files(src_filepath, search_term, exact_match):
    results = []
    search_words = search_term.lower().split() if not exact_match else []


    for filepath in walk_files(src_filepath):
        filename = os.path.basename(filepath)

        if exact_match:
            match = filename.lower() == search_term.lower()
        else:
            match = any(word in filename for word in search_words) if search_words else search_term.lower() in filename

        if match:
            metadata = get_metadata(filepath)
            if metadata:
                insert_file_to_db(filepath, metadata)
                results.append(metadata)
    return results

def walk_files(src_filepath):
    for root, _, files in os.walk(src_filepath):
        for file in files:
            yield os.path.join(root, file)