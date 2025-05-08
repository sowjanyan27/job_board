from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, unique=True, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    salary_range = Column(JSON, index=True)  # stored as list
    required_skills = Column(JSON, index=True)  # stored as list
    posted_by = Column(Integer, index=True)
