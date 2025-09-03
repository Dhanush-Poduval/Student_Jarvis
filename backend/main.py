from fastapi import FastAPI
from . import models
from.database import engine
from .routers import user , aimodel
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

origins = [
    "http://localhost:3000",  # Next.js local dev
    "http://127.0.0.1:3000", # just in case
    # you can add deployed frontend URLs here too
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE etc.
    allow_headers=["*"],            # Allow all headers
)


models.Base.metadata.create_all(bind=engine)

app.include_router(aimodel.router)
app.include_router(user.router)