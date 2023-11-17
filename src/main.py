from fastapi import FastAPI
import logging 
from logging.config import dictConfig
from log_config import log_config

dictConfig(log_config)

app = FastAPI()
logger = logging.getLogger('foo-logger')

@app.get("/")
async def root():
    return {
        "status":"Success",
        "data": "Welcome to the bestfriend API"
    }