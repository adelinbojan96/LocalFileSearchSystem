import os

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileSerializer
from rest_framework.decorators import api_view
from .search_algorithm import index_files
from .database_handling import extract_file_from_db, restart_indexing_database

@api_view(['POST'])
def search_file(request):
    try:

        directory = request.data.get(
            'directory_path') or r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\be_django\be_django\searchingDir"
        # default parameters
        file_name = request.data.get('file_name', '').strip()
        exact_match = request.data.get('exact_match', False)
        page = 1
        page_size = 25 # max size of files that it can find

        if not file_name:
            return JsonResponse({'error': 'No file name provided'}, status=400)

        if not os.path.exists(directory):
            return JsonResponse({'error': 'Search directory not found'}, status=404)

        results = index_files(directory, file_name, exact_match)

        # pagination information
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


@api_view(['GET'])
def get_file_metadata(request, file_name):
    if not file_name:
        return Response({'error': 'No file name provided'}, status=status.HTTP_400_BAD_REQUEST)
    metadata = extract_file_from_db(file_name)
    if metadata:
        return Response(metadata, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def restart_database(request):
    restart_indexing_database()
    return Response({'message': 'Database restarted'}, status=200)

class FileListView(APIView):
    def get(self, request):
        # basic example of files
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