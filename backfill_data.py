import sqlite3
import random
import datetime

# 1. Connect to the DB
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 2. Get the list of books that exist in your DB (from Friday's scrape)
# We only need Title and Base Price to calculate the new values
cursor.execute("SELECT title, price, rating FROM books GROUP BY title")
existing_books = cursor.fetchall()

print(f"Found {len(existing_books)} books. Generating history...")

# 3. Define the dates we missed (The weekend)
missing_dates = [
    datetime.date(2026, 1, 10), # Saturday
    datetime.date(2026, 1, 11), # Sunday
    datetime.date(2026, 1, 12)  # Today (Monday) - Optional if you haven't run it today
]

# 4. Generate data
count = 0
for fake_date in missing_dates:
    print(f"Generating data for {fake_date}...")
    
    for book in existing_books:
        title = book[0]
        base_price = book[1]
        rating = book[2]
        
        # MARKET SIMULATION: +/- 10% fluctuation
        fluctuation = random.uniform(0.90, 1.10)
        new_price = round(base_price * fluctuation, 2)
        
        # Insert the backfilled record
        cursor.execute('''
            INSERT INTO books (title, price, rating, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (title, new_price, rating, fake_date))
        count += 1

# 5. Commit and Close
conn.commit()
conn.close()

print(f"Success! Added {count} new records to the database.")