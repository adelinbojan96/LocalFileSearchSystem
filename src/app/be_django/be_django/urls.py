

from django.contrib import admin
from django.urls import path, include
from .views import FileListView, search_file, get_file_metadata, restart_database

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', FileListView.as_view(), name='file-list'),
    path('api/search/', search_file, name='search-file'),
    path('api/restart/', restart_database, name='restart-database'),
    path('', FileListView.as_view(), name='home'),
    path('api/files/<str:file_name>/', get_file_metadata, name='get_file_metadata')
]
