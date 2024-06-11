from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from .routes import memes

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.include_router(memes.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


@app.get("/")
def read_root():
    return {"message": "Welcome to the Meme API"}
