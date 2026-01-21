import logging

from fastapi import FastAPI
from router import survey


app: FastAPI = FastAPI(
    title="A Cloud Run API",
)
app.include_router(survey.router)


@app.get("/health", status_code=200)
async def health() -> dict:
    """Checks that the API is up and running"""
    return {
        "status": "OK",
    }
