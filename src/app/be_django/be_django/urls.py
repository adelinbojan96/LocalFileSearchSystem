

from django.contrib import admin
from django.urls import path, include
from .views import FileListView, ExampleView, search_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', FileListView.as_view(), name='file-list'),
    path('api/example/', ExampleView.as_view(), name='example-api'),
    path('api/search/', search_file, name='search-file'),
    path('', FileListView.as_view(), name='home'),
]
