from django.db import models

class FileInfo(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    type = models.CharField(max_length=255, default='unknown')
    size = models.BigIntegerField(default=0)
    last_modified = models.DateTimeField()
    creation_time = models.DateTimeField()
    preview = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'file_info'
