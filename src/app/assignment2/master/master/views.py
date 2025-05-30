from rest_framework.decorators import api_view
from .search_controller import search_files

@api_view(["GET"])
def master_search(request):
    return search_files(request)