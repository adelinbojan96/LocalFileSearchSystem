import os
import sys
import argparse
from flask import Flask, request, jsonify

app = Flask(__name__)

# command line arguments
parser = argparse.ArgumentParser(description="slave worker server")
parser.add_argument("-p", "--port", type=int, required=True, help="port to run the server on")
parser.add_argument("-b", "--base_directory", required=True, help="base directory to search")
parser.add_argument("-s", "--server_id", type=int, required=True, help="server id")
args = parser.parse_args()

# config
port = args.port
base_directory = args.base_directory
server_id = args.server_id

@app.route("/api/search/", methods=["POST"])
def worker_search():
    query = request.json.get("query", "").strip()
    files = request.json.get("files", [])
    results = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        if query.lower() in file_name.lower():
            results.append({
                'server': server_id,
                'name': file_name,
                'path': file_path,
                'size': os.path.getsize(file_path),
                'last_modified': os.path.getmtime(file_path),
                'creation_time': os.path.getctime(file_path),
                'type': os.path.splitext(file_name)[1] or 'unknown',
            })

    return jsonify({'results': results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)