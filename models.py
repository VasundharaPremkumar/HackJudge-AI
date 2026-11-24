
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from database import Base


class Submission(Base):

    __tablename__ = "submissions"

    # Unique ID for every submission
    submission_id = Column(
        String(36),
        primary_key=True,
        index=True
    )

    # Name of uploaded project file
    filename = Column(
        String(255),
        nullable=True
    )

    # Location where uploaded file is stored
    file_path = Column(
        String(500),
        nullable=True
    )

    # File format: ZIP, PPT, PDF, etc.
    file_type = Column(
        String(20),
        nullable=False
    )

    # Uploaded file size in bytes
    file_size = Column(
        Integer,
        nullable=True
    )

    # GitHub repository URL (if submitted)
    github_url = Column(
        String(500),
        nullable=True
    )

    # Current submission/execution status
    status = Column(
        String(30),
        default="RECEIVED",
        nullable=False
    )

    # Submission creation timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
