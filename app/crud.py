from sqlalchemy.orm import Session
from . import models, schemas


def get_meme(db: Session, meme_id: int):
    return db.query(models.Meme).filter(models.Meme.id == meme_id).first()


def update_meme(db: Session, meme: models.Meme):
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme


def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def create_meme(db: Session, meme: schemas.MemeCreate, image_url: str):
    db_meme = models.Meme(**meme.dict(), image_url=image_url)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    db.delete(meme)
    db.commit()
