import os
import mimetypes
from .database_handling import insert_file_to_db, restart_indexing_database, fulltext_search, exact_search
import re

def extract_path_filters(query: str):
    matches = re.findall(r'\bpath:(?:"([^"]+)"|(\S+))', query, re.IGNORECASE)
    return [quoted or unquoted for quoted, unquoted in matches if quoted or unquoted]

def extract_content_filters(query: str) -> list[str]:
    matches = re.findall(r'\bcontent:(?:"([^"]+)"|(\S+))', query, re.IGNORECASE)
    return [quoted or unquoted for quoted, unquoted in matches]


def build_search_query(path_filters: list[str], content_filters: list[str]):
    conditions = []
    params = []

    if path_filters:
        path_conditions = []
        for path in path_filters:
            path_conditions.append("path LIKE %s")
            params.append(f"%{path}%")
        conditions.append(f"({' AND '.join(path_conditions)})")

    if content_filters:
        content_conditions = []
        for content in content_filters:
            content_conditions.append("MATCH(preview) AGAINST (%s IN BOOLEAN MODE)")
            params.append(f"+{content}")
        conditions.append(f"({' AND '.join(content_conditions)})")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT name, path, size, last_modified, creation_time, type, preview
        FROM file_info
        WHERE {where_clause}
        LIMIT 100
    """

    return query, params

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
        if file_type and 'text' in file_type:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(500)
        return ''
    except Exception as e:
        print(f"Preview error for {filepath}: {str(e)}")
        return ''

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