import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time 

# --- 1. The Frontend (UI) ---
st.set_page_config(page_title="Book Scraper Bot", page_icon="📚")

st.title("📚 AI Book Scraper")
st.markdown("Click the button below to scrape book titles and authors from **Books to Scrape** automatically.")

# Sidebar controls
pages_to_scrape = st.sidebar.slider("How many pages to scrape?", min_value=1, max_value=5, value=1)

# --- 2. The Backend (Logic) ---
def scrape_books(num_pages):
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    
    # Progress bar widget
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for page in range(1, num_pages + 1):
        status_text.text(f"⏳ Scraping Page {page} of {num_pages}...")
        
        # Requests & Soup logic (You know this!)
        url = base_url.format(page)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find_all("article", class_="product_pod")
                
                for book in books:
                    title = book.h3.a["title"]
                    price = book.find("p", class_="price_color").text.replace("£", "")
                    rating = book.find("p", class_="star-rating")["class"][1]
                    availability = book.find("p", class_="instock availability").text.strip()
                    
                    all_books.append({
                        "Title": title,
                        "Price": float(price.replace("Â", "")),
                        "Rating": rating,
                        "Availability": availability
                    })
            else:
                st.error(f"Failed to load page {page}")
                
        except Exception as e:
            st.error(f"Error: {e}")
            
        # Update progress bar
        progress_bar.progress(page / num_pages)
        time.sleep(0.5) # Slight pause
        
    status_text.success("✅ Scraping Complete!")
    return pd.DataFrame(all_books)

# --- 3. The Trigger ---
if st.button("Start Scraping"):
    # Run the function
    df = scrape_books(pages_to_scrape)
    
    # Show the data
    st.write(f"Found {len(df)} books:")
    st.dataframe(df)
    
    # Create the Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="scraped_books.csv",
        mime="text/csv"
    )