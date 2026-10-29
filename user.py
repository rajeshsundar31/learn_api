from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, StrictInt, Field
from model.user_model import User
from starlette import status


app = FastAPI()

class UserRequest(BaseModel):
    int : StrictInt = Field(gt=0)
    name: str = Field(min_length=6)
    age: StrictInt
    email: str
    gender: str

userList = [
   User(1, "rajesh", 29, "raje@g.com", "male")
]



@app.get("/")
def heealth_check():
    return "I'm Healthy!"

@app.get("/getlist", status_code=status.HTTP_200_OK)
def get_user_list():
    return userList


@app.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_exact_user(id:int = Path(gt=0)):
    for users in userList:
        if users.id == id:
            return users
    raise HTTPException(status_code=404, detail="Item Not Found!")


@app.post("/createuser")
def create_user(create_request: UserRequest):
    return userList.append(create_request)
