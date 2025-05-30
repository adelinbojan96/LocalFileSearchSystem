import subprocess
import time

slave_configs = [
    {"port": 8001, "server_id": 1, "base_directory": r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\assignment2\documents_to_search"},
    {"port": 8002, "server_id": 2, "base_directory": r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\assignment2\documents_to_search2"},
    {"port": 8003, "server_id": 3, "base_directory": r"D:\SoftwareDesign_Iteartion1_LocalFileSeachSystem\src\app\assignment2\documents_to_search3"},
]

slave_processes = []

for config in slave_configs:
    process = subprocess.Popen([
        "python", "../../slave_1/slave_1/worker_run.py",
        "-p", str(config["port"]),
        "-b", config["base_directory"],
        "-s", str(config["server_id"]),
    ])
    slave_processes.append(process)

master_process = subprocess.Popen(["python", "../manage.py", "runserver", "8000"])