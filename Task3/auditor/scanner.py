
import os
import math
from datetime import datetime

PENALTY_PER_DAY = 20

def scan_directory(folder_path):

    audit_data = []
    penalties = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError("Folder does not exist!")

    current_time = datetime.now()

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):

            stats = os.stat(file_path)

            size_kb = math.ceil(stats.st_size / 1024)

            modified_time = datetime.fromtimestamp(stats.st_mtime)

            age_days = (current_time - modified_time).days

            file_info = {
                "name": filename,
                "size_kb": size_kb,
                "type": filename.split('.')[-1],
                "last_modified": modified_time,
                "age_days": age_days,
                "flagged": age_days > 30
            }

            audit_data.append(file_info)

            if age_days > 30:
                overdue = age_days - 30
                fine = overdue * PENALTY_PER_DAY

                penalties.append({
                    "name": filename,
                    "overdue_days": overdue,
                    "fine": fine
                })

    return audit_data, penalties
