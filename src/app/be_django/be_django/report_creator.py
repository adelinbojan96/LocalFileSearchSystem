from .serializer import ItemSerializer
import json
import os

def update_file_txt(results):
    serialized_data = ItemSerializer(results, many=True).data
    with open("report.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(serialized_data, default=str) + "\n")

def update_file_json(results):
    serialized_data = ItemSerializer(results, many=True).data
    search_block = {
        "search_info": "New Search",
        "results": serialized_data
    }
    if os.path.exists("report.json"):
        with open("report.json", "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    existing_data.append(search_block)
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2, default=str)

def create_large_results_report(results):
    if len(results) > 20:
        serialized_data = ItemSerializer(results, many=True).data
        report_data = {
            "search_info": "Large Results Report",
            "results": serialized_data
        }
        with open("large_results_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
