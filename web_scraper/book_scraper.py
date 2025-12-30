#import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Define the URL of the website to scrape
URL = "http://books.toscrape.com/"

# Function to scrape book data
def scrape_books():
    print(f"🤖 Connecting to {URL}...")
    # Make a GET request to fetch the raw HTML content
    response = requests.get(URL)
    # Check if the request was successful
    if response.status_code != 200:
        print("❌ Failed to retrieve the webpage.")
        return
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all book entries
    books = soup.find_all("article", class_="product_pod")
    print(f"📚 Found {len(books)} books. Extracting data...")

    data_list = []
    
    # Loop through each book and extract details
    for book in books:
        # Extract book title
        title = book.h3.a['title']
        # Extract book price
        price_text = book.find("p", class_="price_color").text
        # Extract book rating
        rating = book.find("p", class_="star-rating")["class"][1]
        
        # Clean price text
        clean_price = price_text.replace("£", "").replace("Â", "")
        # Append to data list
        data_list.append({
            "Title": title,
            "Price_GBP": float(clean_price), # Convert to number for analysis
            "Rating": rating
        })
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data_list)
    df.to_csv("books_scraped.csv", index=False)

    print("\n✅ Success! Data saved to 'books_scraped.csv'")
    print(df.head()) # Show preview

# Run the scraper
if __name__ == "__main__":
    scrape_books()