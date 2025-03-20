import mysql.connector
import os

def insert_file_to_db(filepath, metadata):
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='filesearch'
    )
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO files (name, path, type, size, last_modified, preview)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (os.path.basename(filepath), filepath, metadata['file_type'],
          metadata['size'], metadata['last_modified'], metadata['preview']))

    connection.commit()
    cursor.close()
    connection.close()