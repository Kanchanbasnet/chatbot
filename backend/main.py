
from fastapi import FastAPI

from backend.routes.chat_routes import router as chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}

