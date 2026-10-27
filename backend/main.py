import logging

from fastapi import FastAPI

from backend.logging_config import setup_logging
from backend.routes.chat_routes import router as chat_router

setup_logging()
logger = logging.getLogger(__name__)



app = FastAPI()

app.include_router(chat_router)

@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message": "Welcome to the FastAPI application!"}

