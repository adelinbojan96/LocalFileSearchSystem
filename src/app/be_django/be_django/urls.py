

from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', FileListView.as_view(), name='file-list'),
    path('api/search/', search_file, name='search-file'),
    path('', FileListView.as_view(), name='home'),
    path('api/files/<str:file_name>/', get_file_metadata, name='get_file_metadata'),
    path('api/suggestions/', get_suggestions, name='get_suggestions'),
]
