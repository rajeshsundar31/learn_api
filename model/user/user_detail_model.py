from pydantic import BaseModel, Field, ConfigDict


class UserCreationModel(BaseModel):
    name:str = Field(min_length=5, max_length=22)
    age:int = Field(gt=18)
    gender:str 
    email:str


class ResponseUserModel(UserCreationModel):
    id:int

    model_config = ConfigDict(from_attributes=True)