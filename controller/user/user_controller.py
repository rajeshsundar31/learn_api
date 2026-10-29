from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated

from database.database import get_db
from model.user.user_db import User
from model.user.user_detail_model import UserCreationModel, ResponseUserModel
from starlette import status


user_route = APIRouter()

db_session = Annotated[Session, Depends(get_db)]


@user_route.get("/getuser", response_model=list[ResponseUserModel], status_code=status.HTTP_200_OK)
def get_user(db: db_session):
    listofUsers = select(User)
    return db.scalars(listofUsers).all()


@user_route.post("/addUser", status_code=status.HTTP_201_CREATED)
def add_user(db: db_session, user_data: UserCreationModel):
    new_user = User(**user_data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@user_route.put("/updateuser/{user_id}", status_code=status.HTTP_200_OK)
def update_user(db:db_session, user_id: int, userDate: UserCreationModel):
    find_user = db.get(User, user_id)
    if find_user is None:
        return HTTPException(status_code=404, detail="User Not Foound!")

    updated_data = userDate.model_dump()

    for key, value in updated_data.items():
        setattr(find_user, key, value)

    db.commit()
    db.refresh(find_user)

    return find_user

@user_route.delete("/deleteuser/{user_id}")
def delete_user(db:db_session, user_id:int = Path(gt=0)):
    deleted_user = db.get(User, user_id)
    if deleted_user is None:
        return HTTPException(status_code=404, detail="User not found!")

    db.delete(deleted_user)
    db.commit()




    
