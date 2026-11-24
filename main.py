
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

from database import engine, Base, get_db
from models import Submission
from schemas import (
    SubmissionResponse,
    SubmissionStatusResponse,
    SubmissionExecutionUpdate
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="HackJudge AI",
    description="Submission and Sandbox Management Backend",
    version="1.0.0"
)

# Upload configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".zip", ".ppt", ".pptx", ".pdf"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to HackJudge AI Backend",
        "status": "Running"
    }


# Database health API
@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "backend": "Running",
            "database": "Connected"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )


# Receive submission API
@app.post("/submissions", response_model=SubmissionResponse)
async def create_submission(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty file not allowed"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 50 MB limit"
        )

    submission_id = str(uuid.uuid4())

    safe_filename = submission_id + extension
    file_path = UPLOAD_DIR / safe_filename

    file_path.write_bytes(content)

    submission = Submission(
        submission_id=submission_id,
        filename=Path(file.filename).name,
        file_path=str(file_path),
        file_type=extension,
        file_size=len(content),
        status="RECEIVED"
    )

    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)

        return submission

    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to save submission"
        )


# Retrieve all submissions
@app.get("/submissions", response_model=list[SubmissionResponse])
def get_all_submissions(db: Session = Depends(get_db)):

    return db.query(Submission).order_by(
        Submission.created_at.desc()
    ).all()


# Retrieve submission by ID
@app.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: str,
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(
        Submission.submission_id == submission_id
    ).first()

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    return submission


# Retrieve submission status
@app.get(
    "/submissions/{submission_id}/status",
    response_model=SubmissionStatusResponse
)
def get_submission_status(
    submission_id: str,
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(
        Submission.submission_id == submission_id
    ).first()

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    return {
        "submission_id": submission.submission_id,
        "status": submission.status
    }


# Update submission execution status and results
@app.patch(
    "/submissions/{submission_id}/execution",
    response_model=SubmissionResponse
)
def update_submission_execution(
    submission_id: str,
    execution: SubmissionExecutionUpdate,
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(
        Submission.submission_id == submission_id
    ).first()

    if not submission:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )

    submission.status = execution.status
    submission.stdout = execution.stdout
    submission.stderr = execution.stderr
    submission.exit_code = execution.exit_code
    submission.execution_time = execution.execution_time
    submission.memory_usage = execution.memory_usage

    try:
        db.commit()
        db.refresh(submission)

        return submission

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to update execution results"
        )
