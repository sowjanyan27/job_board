from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.logger import get_logger
from typing import Optional

def get_users(db: Session, skip: int = 0, limit: int = 10000):
    """
          Fetch a users from the database .
          - db: SQLAlchemy Session
          - users: The ID of the user to fetch
          """
    return db.query(User).order_by(User.id).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
       Fetch a user from the database by their ID.
       - db: SQLAlchemy Session
       - user_id: The ID of the user to fetch
       """
    return db.query(User).filter(User.id == user_id).first()



