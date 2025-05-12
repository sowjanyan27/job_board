
from aiocache import Cache
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import time
from app.db.models.resume import Resume
from app.schemas.resumes import ResumesData
from app.db.session import get_db
from app.core.logger import get_logger

router = APIRouter()
cache = Cache.from_url("memory://")  # In-memory cache


logger = get_logger("resumes")

@router.get("/",response_model=List[ResumesData],summary="Get all Resumes")
async def get_all_resumes(skip: int = Query(0),limit: int = Query(10000),db: Session = Depends(get_db),):
    start_time = time.time()
    try:
        logger.info(f"[GET /resumes] skip={skip}, limit={limit}")

        # Fetch Resumes from DB
        Resumes = db.query(Resume).order_by(Resume.id).offset(skip).limit(limit).all()

        # Log the number of users retrieved
        logger.info(f"[GET /Resumes] Retrieved {len(Resumes)} users from DB")
        duration = time.time() - start_time  # End timing the request
        logger.info(f"[GET /Resumes] Retrieved {len(Resumes)} users in {duration:.3f} seconds")

        # Return the Resumes (You may choose to stream compressed data if needed)
        return Resumes

    except Exception as e:
        logger.exception(f"Failed to fetch Resumes. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch Resumes")


@router.get("/filter", response_model=list[ResumesData], summary="Get Resumes with filters")
async def fetch_resumes_with_filters(
        user_id: Optional[str] = Query(None),  # Optional filter for user_id
        extracted_skills: Optional[str] = Query(None),  # Optional filter for extracted_skills
        experience: Optional[str] = Query(None),  # Optional filter for experience
        skip: int = Query(...),  # Pagination is mandatory, no default value
        limit: int = Query(...),  # Pagination is mandatory, no default value
        db: Session = Depends(get_db),  # Dependency for DB session
):
    try:
        start_time = time.time()
        logger.info(f"[GET /Resumes/filter] Filters: user_id={user_id}, extracted_skills={extracted_skills}, experience={experience}, skip={skip}, limit={limit}")

        # Create a cache key based on the filters and pagination
        cache_key = f"Resumes_{user_id}_{extracted_skills}_{experience}_{skip}_{limit}"

        # Check if the result is already cached
        cached_result = await cache.get(cache_key)
        if cached_result:
            logger.info(f"[GET /Resumes/filter] Cache hit for filters: {cache_key}")
            return cached_result
        else:
            logger.info(f"[GET /Resumes/filter] Cache miss for filters: {cache_key}")

            # Start the base query
            query = db.query(Resume).order_by(Resume.id)

            # Apply filters if provided
            if user_id:
                query = query.filter(Resume.user_id.like(f"%{user_id}%"))
            if extracted_skills:
                query = query.filter(Resume.extracted_skills.like(f"%{extracted_skills}%"))
            if experience:
                query = query.filter(Resume.experience.like(f"%{experience}%"))

            # Get the total count of Resumes matching the filters (useful for pagination)
            total = query.count()

            # Apply pagination (mandatory)
            Resumes = query.offset(skip).limit(limit).all()

            logger.info(f"[GET /Resumes/filter] Retrieved {len(Resumes)} filtered Resumes, total matching: {total}")

            # Log the query duration
            duration = time.time() - start_time
            logger.info(f"[GET /Resumes/filter] Query executed in {duration:.3f} seconds")

            # Optionally cache the result
            await cache.set(cache_key, Resumes)

            return Resumes

    except Exception as e:
        logger.exception(f"Failed to fetch filtered Resumes. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch filtered Resumes")


@router.get("/resumes/{resume_id}", response_model=ResumesData)
async def read_resume(resume_id: int, db: Session = Depends(get_db)) -> ResumesData:
    """
    Fetches a single Resume by their ID from the database or cache.
    """
    start_time = time.time()

    cache_key = f"Resume_{resume_id}"
    logger.info(cache_key)
    cached_result = await cache.get(cache_key)

    if cached_result:
        # Cache hit: log the cache hit
        logger.info(f"[GET /Resume/{resume_id}] Cache hit for Resume {resume_id}. Returning from cache.")
        return cached_result  # Returning cached result

    # If data is not found in cache, query the database
    try:
        user = db.query(Resume).filter(Resume.id == resume_id).first()

        if not user:
            # If user not found in the database
            logger.warning(f"[GET /Resume/{resume_id}] Resume not found in database.")
            raise HTTPException(status_code=404, detail="Resume not found")

        # Log that the data was fetched from the database
        logger.info(f"[GET /Resume/{resume_id}] Resume fetched from database. Caching result for future requests.")

        # Cache the result for future requests
        await cache.set(cache_key, user, ttl=300)  # Cache the user for 5 minutes

        # Log the query execution time
        duration = time.time() - start_time
        logger.info(f"[GET /Resume/{resume_id}] Query executed in {duration:.3f} seconds. User returned from database.")

        return user

    except Exception as e:
        # Log the error and raise an HTTPException with a status code of 500 (Internal Server Error)
        logger.error(f"[GET /Resume/{resume_id}] An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
