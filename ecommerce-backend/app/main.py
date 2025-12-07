# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from sqlmodel import SQLModel
from app.routers import auth, products, orders
from app import models
from app.routers import users
from app.core.exceptions import ExceptionHandlerMiddleware


app = FastAPI(title="E-commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # عنوان الفرونت اند
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ExceptionHandlerMiddleware)




@app.get("/")
def read_root():
    return {"message": "Welcome to your ecommerce backend!"}


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(users.router)



