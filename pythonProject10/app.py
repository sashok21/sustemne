import json
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


books_db = {}
next_id = 1
DATA_FILE = "books.json"


def save_to_file():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books_db, f, ensure_ascii=False, indent=4)


def load_from_file():
    global books_db, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            books_db = json.load(f)
        if books_db:
            next_id = max(int(i) for i in books_db.keys()) + 1


async def list_books(request):
    return JSONResponse({"books": list(books_db.values()), "total": len(books_db)})

async def get_book(request):
    book_id = request.path_params["book_id"]
    book = books_db.get(str(book_id))
    if not book:
        return JSONResponse({"error": "Book not found"}, status_code=404)
    return JSONResponse(book)

async def create_book(request):
    global next_id
    data = await request.json()
    book = {"id": next_id, "title": data["title"], "author": data["author"]}
    books_db[str(next_id)] = book
    next_id += 1
    save_to_file()
    return JSONResponse(book, status_code=201)

async def update_book(request):
    book_id = request.path_params["book_id"]
    data = await request.json()
    if str(book_id) not in books_db:
        return JSONResponse({"error": "Book not found"}, status_code=404)
    books_db[str(book_id)].update(data)
    save_to_file()
    return JSONResponse(books_db[str(book_id)])

async def delete_book(request):
    book_id = request.path_params["book_id"]
    if str(book_id) not in books_db:
        return JSONResponse({"error": "Book not found"}, status_code=404)
    del books_db[str(book_id)]
    save_to_file()
    return JSONResponse({"message": "Book deleted"})


async def startup():
    global next_id
    load_from_file()
    if not books_db:
        books_db.update({
            "1": {"id": 1, "title": "On the Road", "author": "Jack Kerouac"},
            "2": {"id": 2, "title": "Howl", "author": "Allen Ginsberg"},
            "3": {"id": 3, "title": "Naked Lunch", "author": "William S. Burroughs"},
        })
        next_id = 4
        save_to_file()


routes = [
    Route("/books", list_books, methods=["GET"]),
    Route("/books", create_book, methods=["POST"]),
    Route("/books/{book_id:int}", get_book, methods=["GET"]),
    Route("/books/{book_id:int}", update_book, methods=["PUT"]),
    Route("/books/{book_id:int}", delete_book, methods=["DELETE"]),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
