
"""
schemas/jobs.py

This module defines the Pydantic data model for job listings used in the application.
It ensures that job data conforms to the expected structure for validation, serialization,
and communication between components (e.g., APIs, databases).

Using Pydantic's BaseModel enables automatic data parsing and validation,
which is especially useful in FastAPI and other Python web frameworks.
"""

from pydantic import BaseModel, ConfigDict
from typing import List

class JobsData(BaseModel):
    id: int
    title: str
    description: str
    company: str
    location: str
    salary_range: List[str]
    required_skills: List[str]
    posted_by: int

    # Correct approach in Pydantic v2: using ConfigDict directly
    model_config = ConfigDict(
        from_attributes=True,  # Allows attribute names to be used as aliases
    )
