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

################### 1--------------- get data by  pagination with get users -------------------
"""
  Fetches a all  jobs  from the database.

  Args:
      db: The database session dependency.

  Returns:
      A Jobs data model representing the fetched job.

  Raises:
      HTTPException: If the jobs are not find then exception will be  is not found.
  """

@router.get("/",response_model=List[JobsData],summary="Get all Jobs (paginated)")
async def get_all_jobs(skip: int = Query(0),limit: int = Query(10000),db: Session = Depends(get_db),):
    """
        Fetches a all  jobs by  pagination  from the database or cache.
        """

    start_time = time.time()

    try:

        logger.info(f"[GET /jobs] skip={skip}, limit={limit}")

        # Fetch jobs from DB
        jobs = db.query(Job).order_by(Job.id).offset(skip).limit(limit).all()

        # Log the number of jobs retrieved
        logger.info(f"[GET /Jobs] Retrieved {len(jobs)} jobs from DB")
        duration = time.time() - start_time  # End timing the request
        logger.info(f"[GET /Jobs] Retrieved {len(jobs)} jobs in {duration:.3f} seconds")

        # Return the jobs (You may choose to stream compressed data if needed)
        return jobs

    except Exception as e:
        logger.exception(f"Failed to fetch jobs. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch jobs")

################## 2. get all users with pagination and filtering data ######################
"""
  Fetches a all  jobs  with filter  from the database.

  Args:
      db: The database session dependency.
  Returns:
      A Jobs data model with filtering  representing the fetched job.

  Raises:
      HTTPException: If the jobs are not find then exception will be  is not found.
  """
@router.get("/filter", response_model=list[JobsData], summary="Get Jobs with filters")
async def fetch_jobs_with_filters(
        tittle: Optional[str] = Query(None),  # Optional filter for tittle
        company: Optional[str] = Query(None),  # Optional filter for company
        location: Optional[str] = Query(None),  # Optional filter for location
        skip: int = Query(...),  # Pagination is mandatory, no default value
        limit: int = Query(...),  # Pagination is mandatory, no default value
        db: Session = Depends(get_db),  # Dependency for DB session
):
    """
        Fetches All   jobs  with pagination and filter  from the database or cache.
        """
    try:
        start_time = time.time()
        logger.info(f"[GET /jobs/filter] Filters: tittle={tittle}, company={company}, location={location}, skip={skip}, limit={limit}")

        # Create a cache key based on the filters and pagination
        cache_key = f"jobs_{tittle}_{company}_{location}_{skip}_{limit}"

        # Check if the result is already cached
        cached_result = await cache.get(cache_key)
        if cached_result:
            logger.info(f"[GET /jobs/filter] Cache hit for filters: {cache_key}")
            return cached_result
        else:
            logger.info(f"[GET /jobs/filter] Cache miss for filters: {cache_key}")

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
            jobs = query.offset(skip).limit(limit).all()

            logger.info(f"[GET /jobs/filter] Retrieved {len(jobs)} filtered jobs, total matching: {total}")

            # Log the query duration
            duration = time.time() - start_time
            logger.info(f"[GET /jobs/filter] Query executed in {duration:.3f} seconds")

            # Optionally cache the result
            await cache.set(cache_key, jobs)

            return jobs

    except Exception as e:
        logger.exception(f"Failed to fetch filtered jobs. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch filtered Jobs")

##################   3. fetch  job by id            ###########################

"""
  Fetches a   job details   by the id   from the database.
  
  Args:
      job_id: The ID of the job to retrieve.
      db: The database session dependency.
  Returns:
      A Jobs data model with filtering  representing the fetched job.

  Raises:
      HTTPException: If the jobs are not find then exception will be  is not found.
  """
@router.get("/jobs/{job_id}", response_model=JobsData)
async def read_job(job_id: int, db: Session = Depends(get_db)) -> JobsData:
    """
    Fetches a single job by their ID from the database or cache.
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
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            # If job not found in the database
            logger.warning(f"[GET /jobs/{job_id}] job not found in database.")
            raise HTTPException(status_code=404, detail="job not found")

        # Log that the data was fetched from the database
        logger.info(f"[GET /job/{job_id}] job fetched from database. Caching result for future requests.")

        # Cache the result for future requests
        await cache.set(cache_key, job, ttl=300)  # Cache the job for 5 minutes

        # Log the query execution time
        duration = time.time() - start_time
        logger.info(f"[GET /job/{job_id}] Query executed in {duration:.3f} seconds. job returned from database.")

        return job

    except Exception as e:
        # Log the error and raise an HTTPException with a status code of 500 (Internal Server Error)
        logger.error(f"[GET /job/{job_id}] An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
