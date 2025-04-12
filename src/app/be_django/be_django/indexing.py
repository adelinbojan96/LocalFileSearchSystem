import os
from .database_handling import insert_file_to_db, restart_indexing_database, fulltext_search, exact_search
import re

def index_files(src_filepath, search_term, exact_match, content_filters):
    restart_indexing_database()
    for filepath in walk_files(src_filepath):
        metadata = get_metadata(filepath)
        if metadata:
            insert_file_to_db(filepath, metadata)

    if exact_match:
        clean_name = re.sub(r'(path|content):\S+', '', search_term).strip()
        return exact_search(clean_name, content_filters)
    else:
        return fulltext_search(search_term, content_filters)

def walk_files(src_filepath):
    for root, _, files in os.walk(src_filepath):
        for file in files:
            yield os.path.join(root, file)