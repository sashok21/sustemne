import os
import json

from starlette import status
from starlette.testclient import TestClient
from app import app, DATA_FILE
from app import app

class TestBookEndpoints:


    def test_list_books(self):
        with TestClient(app) as client:
            response = client.get("/books")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data["books"]) == 3
            first_book = data["books"][0]
            assert "id" in first_book
            assert "title" in first_book
            assert "author" in first_book

    def test_get_book_detail(self):
        with TestClient(app) as client:
            response = client.get("/books/1")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == 1
            assert data["author"] == "Jack Kerouac"
            assert data["title"] == "On the Road"


            response = client.get("/books/999")
            assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_create_book(self):
        with TestClient(app) as client:
            new_book = {"title": "The Dharma Bums", "author": "Jack Kerouac"}
            response = client.post("/books", json=new_book)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["title"] == new_book["title"]
            assert data["author"] == new_book["author"]
            assert "id" in data


    def test_update_book(self):
        with TestClient(app) as client:
            updated_book = {"title": "On the Road (Updated)", "author": "Jack Kerouac"}
            response = client.put("/books/1", json=updated_book)
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["title"] == updated_book["title"]
            assert data["author"] == updated_book["author"]

            response = client.put("/books/999", json=updated_book)
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_book(self):
        with TestClient(app) as client:
            response = client.delete("/books/1")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["message"] == "Book deleted"

            response = client.delete("/books/1")
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_json_file_created(self):
        with TestClient(app) as client:
            new_book = {"title": "Big Sur", "author": "Jack Kerouac"}
            response = client.post("/books", json=new_book)
            assert response.status_code == 201

            assert os.path.exists(DATA_FILE)

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert any(book["title"] == "Big Sur" for book in data.values())
