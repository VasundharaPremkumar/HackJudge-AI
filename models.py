
from sqlalchemy import Column, String, Integer, DateTime, Text, Float
from sqlalchemy.sql import func

from database import Base


class Submission(Base):

    __tablename__ = "submissions"

    submission_id = Column(String(36), primary_key=True, index=True)

    filename = Column(String(255), nullable=True)

    file_path = Column(String(500), nullable=True)

    file_type = Column(String(20), nullable=False)

    file_size = Column(Integer, nullable=True)

    github_url = Column(String(500), nullable=True)

    status = Column(String(30), default="RECEIVED", nullable=False)

    # Execution results
    stdout = Column(Text, nullable=True)

    stderr = Column(Text, nullable=True)

    exit_code = Column(Integer, nullable=True)

    execution_time = Column(Float, nullable=True)

    memory_usage = Column(Float, nullable=True)

    # Submission creation timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
