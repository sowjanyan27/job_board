"""
created_by: sowjanya
created_date:05-05-2025
modified_date:06-05-2025
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import time
from app.db.models.user import User
from app.schemas.user import UserOut
from app.db.session import get_db
from app.crud.user import get_users, get_user_by_id
from app.core.logger import logger
from fastapi.responses import StreamingResponse
import json
from starlette.middleware.base import BaseHTTPMiddleware

router = APIRouter()


@router.get("/", response_model=list[UserOut])  # The endpoint returns a list of UserOut schema objects
def list_users(
        skip: int = Query(0),  # Query parameter: how many records to skip (for pagination)
        limit: int = Query(10000),  # Query parameter: max number of records to return
        db: Session = Depends(get_db)  # Dependency injection: get a database session
):
    start_time = time.time()  # Start timer

    """
        Fetches a list of users from the database, optionally paginated by last_id.

        Args:
           last_id: The ID of the last user retrieved. Used for pagination.
            limit: The maximum number of users to fetch.
            db: The database session dependency.

         Returns:
           A list of UserOut models representing the users fetched.
         """

    try:
        logger.info(f"Fetching users with skip={skip}, limit={limit}")  # Log the fetch request
        users = get_users(db, skip=skip, limit=limit)  # Fetch users
        duration = time.time() - start_time  # End timer
        logger.info(f"Fetched {len(users)} users in {duration:.3f} seconds.")
        return users

    except Exception as e:
        logger.error(f"Error in list_users: {e}")  # Log any errors that occur
        raise HTTPException(status_code=500, detail="Could not fetch users")  # Raise an HTTP 500 error for the client


@router.get("/stream", response_class=StreamingResponse)
def stream_users(limit: int = Query(10000), db: Session = Depends(get_db)) -> StreamingResponse:
    """
    Streams user data in JSON format, with logging of the streaming duration.

    Args:
        limit: The maximum number of users to fetch per batch.
        db: The database session dependency.

    Returns:
        A StreamingResponse containing user data in JSON format.
    """
    # Start the timer for the streaming process
    start_time = time.time()
    logger.info("Starting to stream users in JSON format.")

    def generate():
        skip = 0
        first_batch_time = None

        while True:
            # Fetch the next batch of users
            users = db.query(User).order_by(User.id).offset(skip).limit(limit).all()

            # If no users are found, break the loop
            if not users:
                break

            # For the first batch, start the streaming timer
            if first_batch_time is None:
                first_batch_time = time.time()

            # Yield each user record as a JSON string
            for user in users:
                yield json.dumps({"id": user.id, "name": user.name}) + "\n"

            # Increment the skip by the limit to fetch the next batch
            skip += limit
            logger.info(f"Streaming batch with {len(users)} users. Total streamed: {skip}")

        # If streaming has finished, calculate the total duration
        if first_batch_time:
            total_duration = time.time() - first_batch_time
            logger.info(f"Streaming completed. Duration: {total_duration:.2f} seconds.")

    # Start the streaming process
    response = StreamingResponse(generate(), media_type="application/json")

    return response


@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    """
    Fetches a single user by their ID from the database.

    Args:
        user_id: The ID of the user to retrieve.
        db: The database session dependency.

    Returns:
        A UserOut model representing the fetched user.

    Raises:
        HTTPException: If the user with the specified ID is not found.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
