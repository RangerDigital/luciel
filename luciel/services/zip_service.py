
import requests
import zipfile

from typing import List
from tinydb import Query

from settings.config import settings
from database import database


def create_archive(archive_hash: str, urls: List[str]):
    database.update({"status": "in-progress"}, Query().archive_hash == archive_hash)
    
    files = []
    errors = []

    for url in urls:
        try:
            response = requests.get(url)

            if response.status_code != 200:
                errors.append(f"{url} - {response.status_code}")
                continue

            files.append((url.split("/")[-1], response.content))
        except Exception as e:
            errors.append(f"{url} - {e}")
    

    with zipfile.ZipFile(f"cache/{archive_hash}.zip", "w") as zf:
        try:
            for filename, file in files:
                zf.writestr(filename, file)
        except Exception as e:
            errors.append(f"{filename} - {e}")

    if len(errors) > 0:
        database.update({"status": "error", "errors": errors}, Query().archive_hash == archive_hash)
    else:
        database.update({"status": "ready"}, Query().archive_hash == archive_hash)

        # Webhook feature
        if settings.WEBHOOK_URL:
            requests.post(settings.WEBHOOK_URL, json={"archive_hash": archive_hash})