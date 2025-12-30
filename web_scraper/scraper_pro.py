"""
BOOK SCRAPER PROJECT
--------------------
Target Website: http://books.toscrape.com/

How to run this script:
1. Install requirements: pip install requests beautifulsoup4 pandas
2. Run the script: python scraper_pro.py
3. The data will be saved to 'all_books_1000.csv'

Concepts used:
- Requests: To connect to the website.
- BeautifulSoup: To read the HTML tags.
- Time.sleep: To pause between pages (politeness).
- Pandas: To save data to Excel/CSV.
"""

#Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time # New import for pausing

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape_all_books():
    all_books_data = []

    print("🚀 Starting Bulk Scraper (1,000 Books)...")

    for page_num in range(1, 51):  # 50 pages total
        print(f"📄 Scraping Page {page_num}...")

        url = BASE_URL.format(page_num)

        try:
            response = requests.get(url)
        except:
            print(f"❌ Network Error on page {page_num}")
            continue

        if response.status_code != 200:
            print(f"⚠️ Skipping page {page_num} (Status: {response.status_code})")
            continue

        # 3. Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        # 4. Extract Data (Same logic as before)
        for book in books:
            # 1. Title
            title = book.h3.a["title"]
            
            # 2. Price
            price_text = book.find("p", class_="price_color").text
            clean_price = price_text.replace("£", "").replace("Â", "")
            
            # 3. Rating
            rating = book.find("p", class_="star-rating")["class"][1]
            
            # --- NEW PART: Availability ---
            # We look for the paragraph with class "instock availability"
            # .strip() removes the extra whitespace around the text
            availability = book.find("p", class_="instock availability").text.strip()
            # ------------------------------
            
            all_books_data.append({
                "Title": title,
                "Price": float(clean_price),
                "Rating": rating,
                "Availability": availability,  # <--- Add this
                "Page": page_num
            })
            
        # 5. Sleep to be polite (Professional Standard)
        time.sleep(1)

    # 6. Save the massive dataset
    df = pd.DataFrame(all_books_data)
    df.to_csv("all_books_1000.csv", index=False)
    
    print(f"\n✅ Mission Complete! Scraped {len(df)} books.")
    print("📂 Data saved to 'all_books_1000.csv'")

if __name__ == "__main__":
    scrape_all_books()