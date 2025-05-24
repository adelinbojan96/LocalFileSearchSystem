import os
import mimetypes

def get_metadata(filepath):
    try:
        stats = os.stat(filepath)
        return {
            'filename': os.path.basename(filepath),
            'path': filepath,
            'size': stats.st_size,
            'last_modified': stats.st_mtime,
            'creation_time': stats.st_ctime,
            'file_type': mimetypes.guess_type(filepath)[0] or 'unknown',
            'preview': get_file_preview(filepath)
        }
    except Exception as e:
        print(f"Metadata error for {filepath}: {str(e)}")
        return None

def get_file_preview(filepath):
    try:
        file_type = mimetypes.guess_type(filepath)[0]
        file_extension = os.path.splitext(filepath)[1].lower()
        if (file_type and 'text' in file_type) or file_extension == '.log':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(500)
        return ''
    except Exception as e:
        print(f"Preview error for {filepath}: {str(e)}")
        return ''

def walk_files(src_filepath):
    for root, _, files in os.walk(src_filepath):
        for file in files:
            yield os.path.join(root, file)
