from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class ExpenseCreationModel(BaseModel):
    amount:int = Field(gt=0)
    category:str = Field(min_length=3)
    note:str
    date: date

class ExpenseResponse(ExpenseCreationModel):
    id:int
    
    model_config = ConfigDict(from_attributes=True)