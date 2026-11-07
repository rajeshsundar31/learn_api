import os
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from sqlalchemy import select
from typing import Annotated
from dotenv import load_dotenv
from database.database import get_db
from model.model_db import User
from model.user.user_detail_model import UserCreationModel, ResponseUserModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


route = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHAM", "HS256")


db_session = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth_password_bearer = OAuth2PasswordBearer(tokenUrl='auth/verifiy')




@route.post("/addUser", status_code=status.HTTP_201_CREATED)
def add_user(db: db_session, user_data: UserCreationModel):
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = bcrypt_context.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def verifiy_user(username: str, password: str, db):
    user_verifiy = db.query(User).filter(User.name == username).first()

    if user_verifiy is None:
        return False
    if not bcrypt_context.verify(password, user_verifiy.password):
        return False
    return user_verifiy

def create_access_token(username:str, user_id:int, expire_at: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expire_at
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def verifiy_current_user(token: Annotated[str, Depends(oauth_password_bearer)]):
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized user!")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized user!")


@route.post("/verifiy")
def validate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_session):
    user = verifiy_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized user!")
    access_token = create_access_token(user.name, user.id, timedelta(minutes=20))

    return {"access_token": access_token, "token_type": "bearer"}


# @route.get("/getuser", response_model=list[ResponseUserModel], status_code=status.HTTP_200_OK)
# def get_user(db: db_session):
#     listofUsers = select(User)
#     return db.scalars(listofUsers).all()

# @route.put("/updateuser/{user_id}", status_code=status.HTTP_200_OK)
# def update_user(db:db_session, user_id: int, userDate: UserCreationModel):
#     find_user = db.get(User, user_id)
#     if find_user is None:
#         return HTTPException(status_code=404, detail="User Not Foound!")

#     updated_data = userDate.model_dump()

#     for key, value in updated_data.items():
#         setattr(find_user, key, value)

#     db.commit()
#     db.refresh(find_user)

#     return find_user

# @route.delete("/deleteuser/{user_id}")
# def delete_user(db:db_session, user_id:int = Path(gt=0)):
#     deleted_user = db.get(User, user_id)
#     if deleted_user is None:
#         return HTTPException(status_code=404, detail="User not found!")

#     db.delete(deleted_user)
#     db.commit()




    
