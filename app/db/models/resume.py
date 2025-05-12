from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    original_file_path = Column(String, unique=True, index=True, nullable=False)
    parsed_text = Column(String, index=True, nullable=False)
    extracted_skills = Column(JSON, index=True, nullable=False)
    experience = Column(JSON, index=True)  # stored as list
    education = Column(JSON, index=True)  # stored as list

