from fastapi import FastAPI
from database.database import Base, engine
from controller.user.user_controller import route
from controller.expense.expense_controller import expense_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(route)
app.include_router(expense_router)

@app.get("/")
def health_check():
    return {"status": "I'm Healthy!"}