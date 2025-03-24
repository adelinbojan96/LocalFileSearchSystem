from datetime import datetime
from rest_framework import serializers

class TimestampField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value).isoformat()
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value

class FileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    size = serializers.IntegerField()
    path = serializers.CharField(max_length=1024)

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    path = serializers.CharField(max_length=1024)
    type = serializers.CharField(max_length=255, default='unknown')
    size = serializers.IntegerField()
    last_modified = TimestampField()
    creation_time = TimestampField()
    preview = serializers.CharField(allow_blank=True)