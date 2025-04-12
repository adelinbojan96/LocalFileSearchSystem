from datetime import datetime
import os
import logging
from django.db import connection
from .models import FileInfo
from django.utils import timezone

logger = logging.getLogger(__name__)

def exact_search(search_item, content_filters):
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT name, path, size, last_modified, creation_time, type, preview
                FROM file_info
                WHERE name = %s
            """
            params = [search_item]

            if content_filters:
                sql += " AND MATCH(preview) AGAINST (%s IN BOOLEAN MODE)"
                params.append(" ".join(f"+{term}" for term in content_filters))

            sql += " LIMIT 1;"

            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row:
                return dict(zip([col[0] for col in cursor.description], row))
            return None
    except Exception as e:
        logger.error("Exact search failed: %s", e, exc_info=True)
        return None

def fulltext_search(search_query, content_filters, limit=50):
    try:
        with connection.cursor() as cursor:
            conditions = []
            params = []

            if search_query.strip():
                conditions.append("MATCH(name, preview) AGAINST (%s IN NATURAL LANGUAGE MODE)")
                params.append(search_query)

            if content_filters:
                conditions.append("MATCH(preview) AGAINST (%s IN BOOLEAN MODE)")
                params.append(" ".join(f"+{term}" for term in content_filters))

            sql = """
                SELECT
                    name, path, size, last_modified, creation_time, type, preview
                FROM file_info
            """

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " LIMIT %s;"
            params.append(limit)

            cursor.execute(sql, params)

            return [
                dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()
            ]
    except Exception as e:
        logger.error("Full-text search failed: %s", e, exc_info=True)
        return []

def insert_file_to_db(filepath, metadata):
    try:
        last_modified = timezone.make_aware(
            datetime.fromtimestamp(os.path.getmtime(filepath))
        )
        creation_time = timezone.make_aware(
            datetime.fromtimestamp(os.path.getctime(filepath))
        )

        file_info = FileInfo(
            name=os.path.basename(filepath),
            path=filepath,
            type=metadata.get('file_type', 'unknown'),
            size=metadata.get('size', 0),
            last_modified=last_modified,
            creation_time=creation_time,
            preview=metadata.get('preview', '')[:500]
        )
        file_info.save()
    except Exception as err:
        logger.error("Database error in insert_file_to_db for %s: %s", filepath, err, exc_info=True)

def extract_file_from_db(file_name):
    try:
        file_info = FileInfo.objects.filter(name=file_name).first()
        if file_info:
            return {
                'filename': file_info.name,
                'path': file_info.path,
                'size': file_info.size,
                'last_modified': file_info.last_modified,
                'creation_time': file_info.creation_time,
                'file_type': file_info.type,
                'preview': file_info.preview,
            }
        return None
    except Exception as err:
        logger.error("Database error in extract_file_from_db for file_name %s: %s", file_name, err, exc_info=True)
        return None

def restart_indexing_database():
    try:
        FileInfo.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE file_info AUTO_INCREMENT = 1;")
    except Exception as err:
        logger.error("Database error in restart_indexing_database: %s", err, exc_info=True)