import os
import logging
import re

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import FileSerializer
from .search_algorithm import index_files, extract_path_filters, extract_content_filters
from .database_handling import extract_file_from_db, restart_indexing_database
from .report_creator import update_file

logger = logging.getLogger(__name__)

@api_view(['POST'])
def search_file(request):
    try:
        raw_query = request.data.get('file_name', '').strip()
        exact_match = request.data.get('exact_match', False)
        path_filters = extract_path_filters(raw_query)
        content_filters = extract_content_filters(raw_query)

        if path_filters:
            directories = path_filters
        else:
            dir_from_req = request.data.get('directory_path')
            if dir_from_req:
                directories = [dir_from_req]
            else:
                directories = [r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\be_django\be_django\searchingDir"]

        if not raw_query:
            logger.warning("Search attempted without a file name provided.")
            return JsonResponse({'error': 'No file name provided'}, status=400)

        all_results = []
        clean_search_term = re.sub(r'(path|content):\S+', '', raw_query).strip()

        for directory in directories:
            if not os.path.exists(directory):
                logger.error("Search directory not found: %s", directory)
                continue

            try:
                results = index_files(directory, clean_search_term, exact_match, content_filters)
                print(results)
                if results is None:
                    results = []
                elif isinstance(results, dict):
                    results = [results]
                all_results.extend(results)

            except Exception as inner_exc:
                logger.error("Error indexing files in %s: %s", directory, inner_exc, exc_info=True)
                return JsonResponse({'error': 'Error processing search'}, status=500)

        update_file(all_results)

        return JsonResponse({
            'results': all_results
        })

    except Exception as e:
        logger.error("Search error: %s", e, exc_info=True)
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
