
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

    # Execution details
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None

    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubmissionStatusResponse(BaseModel):

    submission_id: str
    status: str


class SubmissionExecutionUpdate(BaseModel):

    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
