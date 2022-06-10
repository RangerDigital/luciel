import uuid
import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

from tinydb import Query
from database import database

from schemas.archive import ArchiveCreate, ArchiveCreateResponse, ArchiveStatusResponse
from services.zip_service import create_archive

router = APIRouter()


@router.post("/archive/create", response_model=ArchiveCreateResponse, status_code=201, )
def post_archive(body: ArchiveCreate, background_tasks: BackgroundTasks):
    archive_hash = str(uuid.uuid4())

    database.insert({"archive_hash": archive_hash, "urls": body.urls, "status": "in-queue", "errors": [], "filename": f"{archive_hash}.zip", "created_at": str(datetime.datetime.now())})
    background_tasks.add_task(create_archive, archive_hash, body.urls)

    return {"archive_hash": archive_hash, "urls": body.urls}



@router.get("/archive/status/{archive_hash}", response_model=ArchiveStatusResponse)
def get_archive_status(archive_hash: str ):
    archive = database.search(Query().archive_hash == archive_hash)
    
    if not archive:
        raise HTTPException(status_code=404, detail="Archive with that hash not found!")
  
    return archive[0]


@router.get("/archive/get/{archive_hash}")
def get_archive_file(archive_hash: str ):
    archive = database.search(Query().archive_hash == archive_hash)

    if not archive:
        raise HTTPException(status_code=404, detail="Archive with that hash not found!")

    if archive[0]["status"] != "ready":
        raise HTTPException(status_code=400, detail="Archive is not done yet!")


    headers = { "Content-Disposition":f"attachment;filename={archive_hash}.zip"}
    return FileResponse(f"cache/{archive_hash}.zip", media_type="application/x-zip-compressed",headers=headers)

