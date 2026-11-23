from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


class UserCreationModel(BaseModel):
    name:str = Field(min_length=5, max_length=50)
    email:EmailStr
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def only_gmail(cls, v: str) -> str:
        if v.split("@")[1].lower() != "gmail.com":
            raise ValueError("Only Gmail addresses are allowed")
        return v.lower()


class ResetPasswordModel(BaseModel):
    new_password: str = Field(min_length=8)

class ResponseUserModel(UserCreationModel):
    id:int

    model_config = ConfigDict(from_attributes=True)