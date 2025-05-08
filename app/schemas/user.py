from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role:str
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
    # model_config = ConfigDict(from_attributes=True)  # Use ConfigDict and from_attributes