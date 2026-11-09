from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from database.database import get_db
from model.model_db import Expense, User
from model.expense.expense_detail_model import ExpenseCreationModel, ExpenseResponse
from starlette import status
from controller.user.user_controller import verifiy_current_user



expense_router = APIRouter(
    tags=["Expense"]
)

db_session = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verifiy_current_user)]

@expense_router.post("/addexpense", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def add_expense(db: db_session, user: user_dependency, expense_dict: ExpenseCreationModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UnAuthoriized user!!')

    add_spend = Expense(**expense_dict.model_dump(), owner_id = user.get('id'))


    db.add(add_spend)
    db.commit()
    return add_spend

@expense_router.get("/getdetails", response_model=list[ExpenseResponse], status_code=status.HTTP_200_OK)
async def get_expense_details(db:db_session, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='UnAuthoriized user!!')

    expense_detail = db.query(Expense).filter(Expense.owner_id == user.get('id')).all()
    
    return expense_detail

@expense_router.get("/detail/{detail_id}", response_model=ExpenseResponse)
async def get_particular_detail(db: db_session, detail_id: int, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized User!")

    detail = db.query(Expense).filter(
        Expense.id == detail_id,
    ).first()

    if detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found!"
        )

    return detail

@expense_router.get("/username")
async def get_userName(db: db_session, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized User!")

    username = db.query(User).filter(User.id == user.get('id')).first()

    if username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not Found!")

    return {"username": username.name}

@expense_router.delete("/detail/{id}")
async def delete_expense_detail(db: db_session, user: user_dependency, id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found!")

    del_detail = db.query(Expense).filter(Expense.id == id).first()

    if del_detail is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Details Not Found!")

    db.delete(del_detail)
    db.commit()

    return {"message": "Deletion Successfully!!"}