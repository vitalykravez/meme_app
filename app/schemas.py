from pydantic import BaseModel


class MemeCreate(BaseModel):
    text: str


class MemeUpdate(BaseModel):
    text: str = None
    image_url: str = None


class Meme(BaseModel):
    id: int
    text: str
    image_url: str

    class Config:
        orm_mode = True
