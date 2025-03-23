import os

from .serializer import ItemSerializer
import json

def update_file(results):
    serialized_data = ItemSerializer(results, many=True).data
    with open("report.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized_data, default=str) + "\n")