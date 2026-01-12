import sqlite3
from fastapi import FastAPI
import os

app = FastAPI()

# Helper function to connect to the DB
def get_db_connection():
    dbPath = os.path.abspath("../library.db")
    conn = sqlite3.connect(dbPath)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library API"}

@app.get("/book/{title}")
def get_book(title: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL query to find a book by its title (partial match)
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    books = cursor.fetchall()
    conn.close()
    
    if not books:
        return {"error": "Book not found"}
    
    # Return the results
    return {"results": books}