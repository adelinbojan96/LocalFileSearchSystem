from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import FileSerializer

class FileListView(APIView):
    def get(self, request):
        #basic example of files
        files = [
            {'name': 'file1.txt', 'size': 1234, 'path': '/path/to/file1.txt'},
            {'name': 'file2.jpg', 'size': 5678, 'path': '/path/to/file2.jpg'}
        ]
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
