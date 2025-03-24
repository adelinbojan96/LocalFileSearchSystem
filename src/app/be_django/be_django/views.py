import os
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import FileSerializer
from .search_algorithm import index_files
from .database_handling import extract_file_from_db, restart_indexing_database
from .report_creator import update_file

logger = logging.getLogger(__name__)

@api_view(['POST'])
def search_file(request):
    try:
        directory = request.data.get(
            'directory_path'
        ) or r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\be_django\be_django\searchingDir"

        file_name = request.data.get('file_name', '').strip()
        exact_match = request.data.get('exact_match', False)
        page = 1
        page_size = 25

        if not file_name:
            logger.warning("search attempted without a file name provided.")
            return JsonResponse({'error': 'No file name provided'}, status=400)

        if not os.path.exists(directory):
            logger.error("search directory not found: %s", directory)
            return JsonResponse({'error': 'Search directory not found'}, status=400)

        try:
            results = index_files(directory, file_name, exact_match)

            if results is None:
                results = []
            elif isinstance(results, dict):
                results = [results]

        except Exception as inner_exc:
            logger.error("error indexing files in %s: %s", directory, inner_exc, exc_info=True)
            return JsonResponse({'error': 'Error processing search'}, status=500)

        # pagination
        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_results = results[start:end]

        update_file(results)

        return JsonResponse({
            'total_results': total,
            'page': page,
            'page_size': page_size,
            'results': paginated_results
        })

    except Exception as e:
        logger.error("search error: %s", e, exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)

@api_view(['GET'])
def get_file_metadata(request, file_name):
    try:
        if not file_name:
            logger.warning("file metadata requested with no file name provided.")
            return Response({'error': 'No file name provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            metadata = extract_file_from_db(file_name)
        except Exception as inner_exc:
            logger.error("error extracting metadata for %s: %s", file_name, inner_exc, exc_info=True)
            return Response({'error': 'Error retrieving file metadata'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if metadata:
            return Response(metadata, status=status.HTTP_200_OK)
        else:
            logger.info("file not found: %s", file_name)
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error("unexpected error in get_file_metadata: %s", e, exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def restart_database(request):
    try:
        restart_indexing_database()
        return Response({'message': 'Database restarted'}, status=200)
    except Exception as e:
        logger.error("error restarting database: %s", e, exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileListView(APIView):
    def get(self, request):
        try:
            # basic example of files for testing
            files = [
                {'name': 'file1.txt', 'size': 1234, 'path': '/path/to/file1.txt'},
                {'name': 'file2.jpg', 'size': 1243, 'path': '/path/to/file2.jpg'},
                {'name': 'file3.obj', 'size': 3251, 'path': '/path/to/file3.obj'},
            ]
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error("Error retrieving file list: %s", e, exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
