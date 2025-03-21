import os

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileSerializer
from rest_framework.decorators import api_view
from .search_algorithm import index_files, walk_files


@api_view(['POST'])
def search_file(request):
    try:
        # Extract parameters with defaults
        file_name = request.data.get('file_name', '').strip()
        exact_match = request.data.get('exact_match', False)
        page = int(request.data.get('page', 1))
        page_size = int(request.data.get('page_size', 10))

        if not file_name:
            return JsonResponse({'error': 'No file name provided'}, status=400)

        directory = r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\be_django\be_django\searchingDir"

        if not os.path.exists(directory):
            return JsonResponse({'error': 'Search directory not found'}, status=404)

        # Get matching files with metadata
        results = index_files(directory, file_name, exact_match)

        # Pagination
        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = results[start:end]

        return JsonResponse({
            'total_results': total,
            'page': page,
            'page_size': page_size,
            'results': paginated_results
        })

    except Exception as e:
        print(f"Search error: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

class FileListView(APIView):
    def get(self, request):
        #basic example of files
        files = [
            {'name': 'file1.txt', 'size': 1234, 'path': '/path/to/file1.txt'},
            {'name': 'file2.jpg', 'size': 5678, 'path': '/path/to/file2.jpg'}
        ]
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

class ExampleView(APIView):
    def get(self, request):
        data = {"message": "Hello from Django!"}
        return Response(data, status=status.HTTP_200_OK)