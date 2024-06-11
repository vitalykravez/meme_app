from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import crud, schemas, s3
from ..dependencies import get_db
import logging
from ..database import init_db


router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.on_event("startup")
def on_startup():
    init_db()


@router.get("/memes", response_model=list[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes


@router.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@router.post("/memes", response_model=schemas.Meme)
async def create_meme(text: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        logger.info(f"Received text: {text}")
        logger.info(f"Received file: {file.filename}")

        image_url = s3.upload_file(file, 'memes')

        logger.info(f"File uploaded successfully, URL: {image_url}")
        meme_create = schemas.MemeCreate(text=text)

        created_meme = crud.create_meme(db=db, meme=meme_create, image_url=image_url)
        logger.info(f"Created meme: {created_meme}")

        return created_meme
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/memes/{id}", response_model=schemas.Meme)
async def update_meme(id: int, text: str = Form(None), file: UploadFile = File(None), db: Session = Depends(get_db)):
    try:
        meme = crud.get_meme(db, meme_id=id)
        if not meme:
            raise HTTPException(status_code=404, detail="Meme not found")

        if text:
            meme.text = text

        if file:
            image_url = s3.upload_file(file, 'memes')
            meme.image_url = image_url

        updated_meme = crud.update_meme(db=db, meme=meme)

        logger.info(f"Updated meme: {updated_meme}")

        return updated_meme
    except Exception as e:
        logger.error(f"Error updating meme: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/memes/{meme_id}")
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_meme(db, meme_id=meme_id)
        return {"message": "Meme deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting meme: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")