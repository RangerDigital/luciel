from typing import List
from pydantic import BaseModel


class ArchiveCreate(BaseModel):
    urls: List[str]


class ArchiveCreateResponse(BaseModel):
    archive_hash: str
    urls: List[str]


class ArchiveStatusResponse(BaseModel):
    archive_hash: str
    status: str
    errors: List[str]
    filename: str
    created_at: str

   
