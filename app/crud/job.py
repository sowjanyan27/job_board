from sqlalchemy.orm import Session
from app.db.models.job import Job
from app.core.logger import get_logger
from typing import Optional

def get_jobs(db: Session, skip: int = 0, limit: int = 10000):
    """
          Fetch a jobs from the database .
          - db: SQLAlchemy Session
          - users: The list  of the user to fetch
          """
    return db.query(Job).order_by(Job.id).offset(skip).limit(limit).all()

def get_job_by_id(db: Session, user_id: int) -> Optional[Job]:
    """
       Fetch a jobs from the database by their ID.
       - db: SQLAlchemy Session
       - id: The ID of the job to fetch
       """
    return db.query(Job).filter(Job.id == user_id).first()