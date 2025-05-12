"""
schemas/user.py

This module defines the Pydantic data model for users listings used in the application.
It ensures that user data conforms to the expected structure for validation, serialization,
and communication between components (e.g., APIs, databases).

Using Pydantic's BaseModel enables automatic data parsing and validation,
which is especially useful in FastAPI and other Python web frameworks.
"""


from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role:str
    model_config = ConfigDict(
        from_attributes=True,
    )
    # model_config = ConfigDict(from_attributes=True)  # Use ConfigDict and from_attributes