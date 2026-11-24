
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubmissionResponse(BaseModel):

    submission_id: str
    filename: Optional[str] = None
    file_type: str
    file_size: Optional[int] = None
    github_url: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubmissionStatusResponse(BaseModel):

    submission_id: str
    status: str
