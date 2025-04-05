
from django.contrib import admin
from django.urls import path
from .search_controller import search_files
from .search_controller import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/search/', search_files, name='search_files'),
    path('', home, name='home'),
]

