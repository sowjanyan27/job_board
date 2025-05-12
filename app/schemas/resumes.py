from pydantic import BaseModel, ConfigDict
from typing import List

class Education(BaseModel):
    year: int
    degree: str

class Experience(BaseModel):
    title:str
    years:int


class ResumesData(BaseModel):
    id: int
    user_id: int
    original_file_path: str
    parsed_text: str
    extracted_skills: List[str]
    experience: Experience
    education: Education  # A list of Education objects



    model_config = ConfigDict(
        from_attributes=True,
    )
