import logging

from fastapi import FastAPI

from router import assesment, survey

app: FastAPI = FastAPI(
    title="A Cloud Run API",
)
app.include_router(survey.router)
app.include_router(assesment.router)


@app.get("/health", status_code=200)
async def health() -> dict:
    """Checks that the API is up and running"""
    return {
        "status": "OK",
    }
