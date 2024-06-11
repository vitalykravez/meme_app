import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def create_files():

    # Создание тестовых файлов
    test_images_dir = '/'
    if not os.path.exists(test_images_dir):
        os.makedirs(test_images_dir)

    with open(os.path.join(test_images_dir, 'test_image.jpg'), 'wb') as f:
        f.write(os.urandom(1024))  # Создаем файл размером 1KB

    with open(os.path.join(test_images_dir, 'updated_test_image.jpg'), 'wb') as f:
        f.write(os.urandom(1024))  # Создаем файл размером 1KB
