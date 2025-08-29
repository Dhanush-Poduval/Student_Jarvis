from fastapi import FastAPI
from . import models
from.database import engine
from .routers import user , aimodel

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(aimodel.router)
app.include_router(user.router)