from sqlalchemy import Column, Integer, String
from .database import Base


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    image_url = Column(String, index=True)
