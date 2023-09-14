#!/usr/bin/python3
"""FastAPI Main Module"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.report_route import router
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="", tags=["reports"])


@app.get("/")
def root() -> dict:
    """Returns Hello World"""
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import uvicorn

    SERVER: dict = {
        "app": "main:app",
        "host": settings.APP_HOST,
        "port": settings.APP_PORT,
    }
    if settings.DEV_MODE:
        uvicorn.run(
            **SERVER,
            reload=True,
            log_level="info",
        )
    else:
        uvicorn.run(
            **SERVER,
            workers=4,
            log_level="error",
        )
