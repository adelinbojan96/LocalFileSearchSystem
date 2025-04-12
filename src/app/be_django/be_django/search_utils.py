import re

def extract_path_filters(query: str):
    matches = re.findall(r'\bpath:(?:"([^"]+)"|(\S+))', query, re.IGNORECASE)
    return [quoted or unquoted for quoted, unquoted in matches if quoted or unquoted]

def extract_content_filters(query: str) -> list[str]:
    matches = re.findall(r'\bcontent:\s*(?:"([^"]+)"|(\S+))', query, re.IGNORECASE)
    filters = []
    for quoted, unquoted in matches:
        if quoted:
            filters.append(quoted.strip())
        elif unquoted:
            filters.extend(unquoted.strip().split())
    return filters

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