from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreationModel(BaseModel):
    name:str = Field(min_length=5, max_length=22)
    email:EmailStr
    password: str


class ResponseUserModel(UserCreationModel):
    id:int

    model_config = ConfigDict(from_attributes=True)