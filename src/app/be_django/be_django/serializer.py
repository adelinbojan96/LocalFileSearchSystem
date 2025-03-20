from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    size = serializers.IntegerField()
    path = serializers.CharField(max_length=1024)