from django.http import JsonResponse
import os

def search_files(query, root_dir):
    matches = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if query.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return matches

def search(request, root_dir):
    query = request.GET.get('query', '')
    results = search_files(query, root_dir)
    return JsonResponse({'results': results})