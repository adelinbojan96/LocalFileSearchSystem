from datetime import datetime

import mysql.connector
import os


def insert_file_to_db(filepath, metadata):
    global connection, cursor
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='files'
        )
        cursor = connection.cursor()

        # Convert timestamps to MySQL DATETIME format
        last_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
        creation_time = datetime.fromtimestamp(os.path.getctime(filepath))

        cursor.execute("""
            INSERT INTO file_info 
                (name, path, type, size, last_modified, creation_time, preview)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            os.path.basename(filepath),
            filepath,
            metadata.get('file_type', 'unknown'),
            metadata.get('size', 0),
            last_modified,
            creation_time,
            metadata.get('preview', '')[:2000]  # Truncate to prevent overflow
        ))

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()