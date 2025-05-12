"""
created_by: sowjanya
created_date:05-05-2025
modified_date:06-05-2025
Description:Getting the users and user  by id from data base
"""
from pydantic import BaseModel
from sqlalchemy import select
import gzip
import io
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import time,asyncio
from app.db.models.user import User
from app.schemas.user import UserOut
from app.db.session import get_db
import json
from aiocache import Cache
from app.core.logger import get_logger


user_stream_cache = {}
router = APIRouter()

# Configure cache
# TTLCache with a max size of 100 and TTL of 300 seconds (5 minutes)
# cache = TTLCache(maxsize=100, ttl=800)
cache = Cache.from_url("memory://")  # In-memory cache
logger = get_logger("users")


class UserListResponse(BaseModel):
    total: int
    users: List[UserOut]

# --- 1. Standard Paginated Fetch ---
@router.get("/", response_model=List[UserOut], summary="Get all users (paginated)")
async def fetch_all_users(
        skip: int = Query(0),
        limit: int = Query(10000),
        db: Session = Depends(get_db),
):
    """
    Fetches all users from the database.

    Returns:
        A UserOut model representing the fetched users.

    Raises:
        HTTPException: If the users are not found or db connection will raise error.
    """
    start_time = time.time()
    try:
        logger.info(f"[GET /users] skip={skip}, limit={limit}")

        # Fetch users from DB
        users = db.query(User).order_by(User.id).offset(skip).limit(limit).all()

        # Log the number of users retrieved
        logger.info(f"[GET /users] Retrieved {len(users)} users from DB")

        # users_data = [UserOut.from_orm(user).dict() for user in users]
        users_data = [UserOut.model_validate(user).model_dump() for user in users]  # ✅ Correct for v2

        # Serialize to JSON
        json_data = json.dumps(users_data, indent=2)

        # Compress the data with Gzip in memory
        gzip_buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_buffer, mode='wb') as gz:
            gz.write(json_data.encode('utf-8'))

        # Rewind the buffer to the beginning
        gzip_buffer.seek(0)

        duration = time.time() - start_time  # End timing the request
        logger.info(f"[GET /users] Retrieved {len(users)} users in {duration:.3f} seconds")

        # Return the users (You may choose to stream compressed data if needed)
        return users  # Or StreamingResponse(gzip_buffer, media_type="application/gzip", headers={...})

    except Exception as e:
        logger.exception(f"Failed to fetch users. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch users")

# --- 2. Filtered User Fetch ---
@router.get("/filter", response_model=list[UserOut], summary="Get users with filters")
async def fetch_users_with_filters(
        name: Optional[str] = Query(None),  # Optional filter for name
        email: Optional[str] = Query(None),  # Optional filter for email
        role: Optional[str] = Query(None),  # Optional filter for role
        skip: int = Query(...),  # Pagination is mandatory, no default value
        limit: int = Query(...),  # Pagination is mandatory, no default value
        db: Session = Depends(get_db),  # Dependency for DB session
):
    """
        Fetches a Users with filter and pagination  from the database or cache.
        """
    try:
        start_time = time.time()
        logger.info(f"[GET /users/filter] Filters: name={name}, email={email}, role={role}, skip={skip}, limit={limit}")

        # Create a cache key based on the filters and pagination
        cache_key = f"users_{name}_{email}_{role}_{skip}_{limit}"

        # Check if the result is already cached
        cached_result = await cache.get(cache_key)
        if cached_result:
            logger.info(f"[GET /users/filter] Cache hit for filters: {cache_key}")
            return cached_result
        else:
            logger.info(f"[GET /users/filter] Cache miss for filters: {cache_key}")

            # Start the base query
            query = db.query(User).order_by(User.id)

            # Apply filters if provided
            if name:
                query = query.filter(User.name.like(f"%{name}%"))
            if email:
                query = query.filter(User.email.like(f"%{email}%"))
            if role:
                query = query.filter(User.role.like(f"%{role}%"))

            # Get the total count of users matching the filters (useful for pagination)
            total = query.count()

            # Apply pagination (mandatory)
            users = query.offset(skip).limit(limit).all()

            logger.info(f"[GET /users/filter] Retrieved {len(users)} filtered users, total matching: {total}")

            # Log the query duration
            duration = time.time() - start_time
            logger.info(f"[GET /users/filter] Query executed in {duration:.3f} seconds")

            # Optionally cache the result
            await cache.set(cache_key, users)

            return users

    except Exception as e:
        logger.exception(f"Failed to fetch filtered users. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch filtered users")

# --- 3. get by  User Id  Endpoint ---
@router.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    """
    Fetches a single user by their ID from the database or cache.
    """
    start_time = time.time()

    cache_key = f"users_{user_id}"
    cached_result = await cache.get(cache_key)

    if cached_result:
        # Cache hit: log the cache hit
        logger.info(f"[GET /users/{user_id}] Cache hit for user {user_id}. Returning from cache.")
        return cached_result  # Returning cached result

    # If data is not found in cache, query the database
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            # If user not found in the database
            logger.warning(f"[GET /users/{user_id}] User not found in database.")
            raise HTTPException(status_code=404, detail="User not found")

        # Log that the data was fetched from the database
        logger.info(f"[GET /users/{user_id}] User fetched from database. Caching result for future requests.")

        # Cache the result for future requests
        await cache.set(cache_key, user, ttl=300)  # Cache the user for 5 minutes

        # Log the query execution time
        duration = time.time() - start_time
        logger.info(f"[GET /users/{user_id}] Query executed in {duration:.3f} seconds. User returned from database.")

        return user

    except Exception as e:
        # Log the error and raise an HTTPException with a status code of 500 (Internal Server Error)
        logger.error(f"[GET /users/{user_id}] An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
