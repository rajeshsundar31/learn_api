from fastapi import FastAPI
from model.user.user_db import User
from database.database import Base, engine
from controller.user.user_controller import route


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(route)