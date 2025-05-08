# app/services/user_service.py
from sqlalchemy.orm import Session
from app.db.models.user import User

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of users from the database, with pagination support.
    - skip: Number of users to skip (default 0)
    - limit: Number of users to return (default 100)
    """
    return db.query(User).offset(skip).limit(limit).all()
