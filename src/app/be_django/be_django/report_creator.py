from .serializer import ItemSerializer
import json

def update_file_txt(results):
    serialized_data = ItemSerializer(results, many=True).data
    with open("report.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized_data, default=str) + "\n")

def update_file_json(results):
    serialized_data = ItemSerializer(results, many=True).data
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(serialized_data, f, ensure_ascii=False, indent=2, default=str)