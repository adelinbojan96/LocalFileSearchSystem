

from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', search_file, name='search-file'),
    path('api/files/<str:file_name>/', get_file_metadata, name='get_file_metadata'),
    path('api/suggestions/', get_suggestions, name='get_suggestions'),
    path('api/widgets/', get_widget, name='get_widget'),
]
