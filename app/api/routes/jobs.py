"""
created_by: sowjanya
created_date:07-05-2025
modified_date:08-05-2025
Description:Getting the jobs
"""
from aiocache import Cache
from pydantic import BaseModel
from sqlalchemy import select
import gzip
import io
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import time
from app.db.models.job import Job
from app.schemas.job import JobsData
from app.db.session import get_db
from app.core.logger import get_logger

router = APIRouter()
cache = Cache.from_url("memory://")  # In-memory cache


logger = get_logger("jobs")
logger.info("Logger test message")

@router.get("/",response_model=List[JobsData],summary="Get all Jobs")
async def get_all_jobs(skip: int = Query(0),limit: int = Query(10000),db: Session = Depends(get_db),):
    start_time = time.time()
    try:
        logger.info(f"[GET /users] skip={skip}, limit={limit}")

        # Fetch jobs from DB
        jobs = db.query(Job).order_by(Job.id).offset(skip).limit(limit).all()

        # Log the number of users retrieved
        logger.info(f"[GET /Jobs] Retrieved {len(jobs)} users from DB")
        duration = time.time() - start_time  # End timing the request
        logger.info(f"[GET /Jobs] Retrieved {len(jobs)} users in {duration:.3f} seconds")

        # Return the jobs (You may choose to stream compressed data if needed)
        return jobs

    except Exception as e:
        logger.exception(f"Failed to fetch jobs. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch jobs")


@router.get("/filter", response_model=list[JobsData], summary="Get Jobs with filters")
async def fetch_jobs_with_filters(
        tittle: Optional[str] = Query(None),  # Optional filter for name
        company: Optional[str] = Query(None),  # Optional filter for email
        location: Optional[str] = Query(None),  # Optional filter for role
        skip: int = Query(...),  # Pagination is mandatory, no default value
        limit: int = Query(...),  # Pagination is mandatory, no default value
        db: Session = Depends(get_db),  # Dependency for DB session
):
    try:
        start_time = time.time()
        logger.info(f"[GET /jobs/filter] Filters: tittle={tittle}, company={company}, location={location}, skip={skip}, limit={limit}")

        # Create a cache key based on the filters and pagination
        cache_key = f"users_{tittle}_{company}_{location}_{skip}_{limit}"

        # Check if the result is already cached
        cached_result = await cache.get(cache_key)
        if cached_result:
            logger.info(f"[GET /users/filter] Cache hit for filters: {cache_key}")
            return cached_result
        else:
            logger.info(f"[GET /users/filter] Cache miss for filters: {cache_key}")

            # Start the base query
            query = db.query(Job).order_by(Job.id)

            # Apply filters if provided
            if tittle:
                query = query.filter(Job.tittle.like(f"%{tittle}%"))
            if company:
                query = query.filter(Job.company.like(f"%{company}%"))
            if location:
                query = query.filter(Job.location.like(f"%{location}%"))

            # Get the total count of jobs matching the filters (useful for pagination)
            total = query.count()

            # Apply pagination (mandatory)
            users = query.offset(skip).limit(limit).all()

            logger.info(f"[GET /jobs/filter] Retrieved {len(users)} filtered jobs, total matching: {total}")

            # Log the query duration
            duration = time.time() - start_time
            logger.info(f"[GET /jobs/filter] Query executed in {duration:.3f} seconds")

            # Optionally cache the result
            await cache.set(cache_key, users)

            return users

    except Exception as e:
        logger.exception(f"Failed to fetch filtered users. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch filtered Jobs")



# @router.get("/jobs/{job_id}", response_model=JobsData)
# def read_user(job_id: int, db: Session = Depends(get_db)) -> JobsData:
#     """
#     Fetches a single job by their ID from the database.
#
#     Args:
#         job_id: The ID of the job to retrieve.
#         db: The database session dependency.
#
#     Returns:
#         A Jobsdata model representing the fetched user.
#
#     Raises:
#         HTTPException: If the job with the specified ID is not found.
#     """
#     start_time = time.time()
#     job = get_job_by_id(db, job_id)
#
#     if not job:
#         logger.warning(f"Job with ID {job_id} not found.")
#         raise HTTPException(status_code=404, detail="Job not found")
#
#     duration = time.time() - start_time
#     logger.info(f"[GET /jobs/{job_id}] job fetched in {duration:.3f} seconds")
#     return job
#

@router.get("/jobs/{job_id}", response_model=JobsData)
async def read_user(job_id: int, db: Session = Depends(get_db)) -> JobsData:
    """
    Fetches a single user by their ID from the database or cache.
    """
    start_time = time.time()

    cache_key = f"jobs_{job_id}"
    logger.info(cache_key)
    cached_result = await cache.get(cache_key)

    if cached_result:
        # Cache hit: log the cache hit
        logger.info(f"[GET /jobs/{job_id}] Cache hit for job {job_id}. Returning from cache.")
        return cached_result  # Returning cached result

    # If data is not found in cache, query the database
    try:
        user = db.query(Job).filter(Job.id == job_id).first()

        if not user:
            # If user not found in the database
            logger.warning(f"[GET /jobs/{job_id}] job not found in database.")
            raise HTTPException(status_code=404, detail="job not found")

        # Log that the data was fetched from the database
        logger.info(f"[GET /job/{job_id}] job fetched from database. Caching result for future requests.")

        # Cache the result for future requests
        await cache.set(cache_key, user, ttl=300)  # Cache the user for 5 minutes

        # Log the query execution time
        duration = time.time() - start_time
        logger.info(f"[GET /job/{job_id}] Query executed in {duration:.3f} seconds. User returned from database.")

        return user

    except Exception as e:
        # Log the error and raise an HTTPException with a status code of 500 (Internal Server Error)
        logger.error(f"[GET /job/{job_id}] An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
