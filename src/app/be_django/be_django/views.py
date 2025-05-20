import base64

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import FileSerializer
from .indexing import index_files, extract_path_filters, extract_content_filters
from .database_handling import *
from .report_creator import update_file_json, update_file_txt
from datetime import datetime
from .search_history import *
logger = logging.getLogger(__name__)

original_dir = r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\be_django\be_django\searchingDir1"
@api_view(['POST'])
def search_file(request):
    try:
        raw_query = request.data.get('file_name', '').strip()
        exact_match = request.data.get('exact_match', False)
        json_format = request.data.get('json_format', False)

        if not raw_query:
            logger.warning("Search attempted without a file name provided.")
            return JsonResponse({'error': 'No file name provided'}, status=400)

        path_filters = extract_path_filters(raw_query)
        content_filters = extract_content_filters(raw_query)
        clean_search_term = re.sub(r'(path|content):\S+', '', raw_query).strip()

        directories = (
            path_filters if path_filters
            else [original_dir]
        )

        valid_directories = []
        invalid_directories = []
        for directory in directories:
            if os.path.exists(directory):
                valid_directories.append(directory)
            else:
                invalid_directories.append(directory)
                logger.error("Search directory not found: %s", directory)

        if not valid_directories:
            return JsonResponse({
                'error': 'No valid search directories',
                'invalid_paths': invalid_directories
            }, status=400)

        try:
            results = index_files(
                src_filepaths=valid_directories,
                search_term=clean_search_term,
                exact_match=exact_match,
                content_filters=content_filters,
                history_manager=history_manager
            )

            if results is None:
                all_results = []
            elif isinstance(results, dict):
                all_results = [results]
            else:
                all_results = results

        except Exception as processing_error:
            logger.error("Search processing failed: %s", processing_error, exc_info=True)
            return JsonResponse({
                'error': 'Error processing search',
                'valid_paths': valid_directories,
                'invalid_paths': invalid_directories
            }, status=500)

        if json_format:
            update_file_json(all_results)
        else:
            update_file_txt(all_results)

        search_data = {
            "timestamp": datetime.now().isoformat(),
            "query": raw_query,
            "results_count": len(all_results),
            "content_filters": content_filters,
            "searched_paths": valid_directories,
            "invalid_paths": invalid_directories
        }
        search_subject.notify(search_data)

        return JsonResponse({
            'results': all_results,
            'metadata': {
                'searched_paths': valid_directories,
                'invalid_paths': invalid_directories,
                'result_count': len(all_results)
            }
        })

    except Exception as e:
        logger.error("Unexpected search error: %s", e, exc_info=True)
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)

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

@api_view(['GET'])
def get_suggestions(request):
    query = request.GET.get('q', '').lower()
    print(query)
    try:
        popular_terms = history_manager.get_popular_terms(limit=50)
        print(popular_terms)
        suggestions = [
            term for term, count in popular_terms
            if query in term
        ]
        return JsonResponse({
            'suggestions': suggestions[:5]
        })
    except Exception as e:
        logger.error("Suggestions error: %s", e)
        return JsonResponse({'error': 'Failed to get suggestions'}, status=500)

@api_view(['GET'])
def get_widget(request):
    query = request.GET.get('q', '').lower()
    try:
        row = extract_widget(query)
        if not row:
            return JsonResponse({'widget': None}, status=status.HTTP_200_OK)

        # img in base64 for frontend
        image_bytes = row['image']
        b64 = base64.b64encode(image_bytes).decode('utf-8')

        widget_obj = {
            'id_word':   row['id_word'],
            'word_name': row['word_name'],
            'image':     b64,
        }
        return JsonResponse({'widget': widget_obj}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error("error retrieving widget: %s", e, exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )