from typing import List

from pydantic import BaseModel, ConfigDict

class JobsData(BaseModel):
    id:int
    title:str
    description:str
    company:str
    location:str
    salary_range: List[str]  # Accepts a list like ["$31000 - $81000"]
    required_skills: List[str]  # Accepts ["Python", "SQL", "FastAPI"]
    posted_by:int
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
