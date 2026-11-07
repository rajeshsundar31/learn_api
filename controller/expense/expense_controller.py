from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import Annotated
from database.database import get_db
from model.model_db import Expense
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