import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
import os
# Get the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(os.path.dirname(script_dir), 'library.db')

# --- 1. Database Setup ---
print("🔌 Connecting to Database...")
# Connect to the file we created earlier
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Safety Check: Create table if it doesn't exist yet
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        rating TEXT,
        scraped_at TEXT
    )
''')

# --- 2. Scraping Logic ---
URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape_to_db(num_pages):
    print(f"🚀 Starting scrape for {num_pages} pages...")
    
    for page in range(1, num_pages + 1):
        print(f"📄 Scraping Page {page}...")
        
        response = requests.get(URL.format(page))
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        today = datetime.date.today()

        for book in books:
            # Extract Data
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            price = float(price_text.replace("£", "").replace("Â", ""))
            rating = book.find("p", class_="star-rating")["class"][1]

            # --- THE NEW PART (SQL Insert) ---
            # Instead of appending to a list, we write to the DB immediately
            cursor.execute('''
                INSERT INTO books (title, price, rating, scraped_at) 
                VALUES (?, ?, ?, ?)
            ''', (title, price, rating, today))
            # ---------------------------------

        # Commit (Save) changes after every page so we don't lose data if it crashes
        conn.commit()
        time.sleep(0.5)

    print("✅ Done! Data saved to library.db")
    conn.close()

# Run it for 2 pages just to test
if __name__ == "__main__":
    scrape_to_db(2)