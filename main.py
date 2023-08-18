#!/usr/bin/python3

"""FastAPI Main Module"""


import asyncio
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from celery import states
from typing import Optional
from pydantic import BaseModel

from jobs.job_engine import generate_report_task
from models.report import Report
from db import db
from core.settings import get_settings
from api.v1.report_route import router

settings = get_settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix="", tags=["reports"])

@app.get('/')
def root() -> dict:
    """Returns Hello World"""
    return {"message": 'Hello World!'}

if __name__ == "__main__":
    import uvicorn
    if settings.DEV_MODE:
        uvicorn.run(app="main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, log_level="info")
    else:
        uvicorn.run(app="main:app", host=settings.APP_HOST, port=settings.APP_PORT, workers=4, log_level="error")
