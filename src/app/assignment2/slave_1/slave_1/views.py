import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def worker_search(request):
    query = request.data.get('query', '').strip()
    files = request.data.get('files', [])
    results = []
    for file_path in files:
        file_name = os.path.basename(file_path)
        if query.lower() in file_name.lower():
            results.append({
                'server' : 1,
                'name': file_name,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'last_modified': os.path.getmtime(file_path),
                'creation_time': os.path.getctime(file_path),
                'type': os.path.splitext(file_name)[1] or 'unknown',
            })
    return Response({'results': results})
