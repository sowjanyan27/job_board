from sqlalchemy.orm import Session
from app.db.models.user import User
from typing import List, Optional

def get_users_cursor(
    db: Session,
    last_id: Optional[int] = None,
    limit: int = 100
) -> List[User]:
    query = db.query(User).order_by(User.id.asc())
    if last_id:
        query = query.filter(User.id > last_id)
    return query.limit(limit).all()
