import re

def extract_path_filters(query: str):
    matches = re.findall(r'\bpath:(?:"([^"]+)"|(\S+))', query, re.IGNORECASE)
    return [quoted or unquoted for quoted, unquoted in matches if quoted or unquoted]

def extract_content_filters(query: str):
    matches = re.findall(r'\bcontent:\s*(?:"([^"]*)"|([^\s]+))', query, re.IGNORECASE)
    terms = []
    for quoted, unquoted in matches:
        if quoted:
            terms.append(quoted.strip())
        elif unquoted:
            terms.extend([t.strip() for t in unquoted.split()])
    return terms
