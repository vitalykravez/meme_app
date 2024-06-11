import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.dependencies import get_db


# Настроим тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Создадим схему базы данных
Base.metadata.create_all(bind=engine)


# Переопределение зависимости get_db для использования тестовой базы данных
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_meme():
    text = "Test meme"
    files = {'file': ('test_image.jpg', open('/test_image.jpg', 'rb'))}
    response = client.post(
        "/memes",
        data={"text": text},
        files=files
    )
    print(response.json())  # Отладочное сообщение
    assert response.status_code == 200
    assert response.json()["text"] == text
    assert "image_url" in response.json()


def test_get_meme():
    # Сначала создадим мем для теста
    text = "Test meme"
    files = {'file': ('test_image.jpg', open('/test_image.jpg', 'rb'))}
    create_response = client.post(
        "/memes",
        data={"text": text},
        files=files
    )
    print(create_response.json())  # Отладочное сообщение
    assert create_response.status_code == 200
    meme_id = create_response.json().get("id")
    assert meme_id is not None

    response = client.get(f"/memes/{meme_id}")
    print(response.json())  # Отладочное сообщение
    assert response.status_code == 200
    assert response.json()["id"] == meme_id


def test_update_meme():
    # Сначала создадим мем для теста
    text = "Test meme"
    files = {'file': ('test_image.jpg', open('/test_image.jpg', 'rb'))}
    create_response = client.post(
        "/memes",
        data={"text": text},
        files=files
    )
    print(create_response.json())  # Отладочное сообщение
    assert create_response.status_code == 200
    meme_id = create_response.json().get("id")
    assert meme_id is not None

    updated_text = "Updated test meme"
    updated_files = {'file': ('updated_test_image.jpg', open('/updated_test_image.jpg', 'rb'))}
    response = client.put(
        f"/memes/{meme_id}",
        data={"text": updated_text},
        files=updated_files
    )
    print(response.json())  # Отладочное сообщение
    assert response.status_code == 200
    assert response.json()["text"] == updated_text
    assert "image_url" in response.json()
