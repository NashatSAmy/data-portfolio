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
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            rating = book.find("p", class_="star-rating")["class"][1]
            
            clean_price = price_text.replace("£", "").replace("Â", "")
            
            all_books_data.append({
                "Title": title,
                "Price_GBP": float(clean_price),
                "Rating": rating,
                "Page": page_num # Traceability (Good for debugging)
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