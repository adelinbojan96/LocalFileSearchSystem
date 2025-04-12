import datetime

from .file_utils import *
from .search_utils import *
from .database_handling import insert_file_to_db, restart_indexing_database, fulltext_search, exact_search

def score_result(result, search_term, content_filters):
    score = 0

    preview = result.get('preview', '').lower()
    file_type = result.get('type', '').lower()
    size = result.get('size', '')
    last_modified = result.get('last_modified')

    if search_term and search_term.lower() in result['name'].lower():
        score += 10

    if content_filters:
        preview = result.get('preview', '').lower()
        score += sum(3 for term in content_filters if term.lower() in preview)

    preferred_types = ['text/plain', 'application/pdf', 'application/msword']
    if file_type in preferred_types:
        score += 2

    if preview:
        score += len(preview) / 500

    if size > 10 * 1024:  # > 10 KB
        score -= 2

    if isinstance(last_modified, datetime.datetime):
        score += last_modified.timestamp() / 1e9

    return score

def index_files(src_filepath, search_term, exact_match, content_filters):
    restart_indexing_database()
    for filepath in walk_files(src_filepath):
        metadata = get_metadata(filepath)
        if metadata:
            insert_file_to_db(filepath, metadata)

    if exact_match:
        clean_name = re.sub(r'(path|content):\S+', '', search_term).strip()
        results = exact_search(clean_name, content_filters)
    else:
        results = fulltext_search(search_term, content_filters)

    scored_results = sorted(results, key=lambda r: score_result(r, search_term, content_filters), reverse=True)
    return scored_results

def walk_files(src_filepath):
    for root, _, files in os.walk(src_filepath):
        for file in files:
            yield os.path.join(root, file)