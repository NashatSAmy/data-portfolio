import sqlite3
import pandas as pd
import streamlit as st
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_folder, '..', 'library.db')
db_path = os.path.abspath(db_path)
# 1. Setup Page
st.set_page_config(page_title="📚 Book Price Tracker", layout="wide")
st.title("📚 Book Market Analytics")

# 2. Load Data from SQLite
# We use a function with @st.cache_data so it doesn't reload the DB every time you click a button
@st.cache_data
def load_data():
    conn = sqlite3.connect(db_path)
    # Read all data into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    
    # Convert 'scraped_at' to a real datetime object for plotting
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    return df

df = load_data()

# --- NEW: KPI Section ---
st.markdown("### 📊 Market Snapshot")

# Calculate metrics
latest_date = df['scraped_at'].max()
latest_data = df[df['scraped_at'] == latest_date]

# 1. Total Books
total_books = latest_data['title'].nunique()

# 2. Average Price
avg_price = latest_data['price'].mean()

# 3. Biggest Drop (Re-using logic)
yesterday = latest_date - pd.Timedelta(days=1)
yesterday_prices = df[df['scraped_at'] == yesterday].set_index('title')['price']
today_prices = latest_data.set_index('title')['price']
# Calculate change and find the biggest negative number (drop)
price_changes = (today_prices - yesterday_prices)
biggest_drop = price_changes.min()

# Display Columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Books Tracked", total_books)
col2.metric("Average Market Price", f"£{avg_price:.2f}")
col3.metric("Best Deal (24h)", f"£{biggest_drop:.2f}", delta=f"{biggest_drop:.2f}")
st.markdown("---")

# 3. Sidebar: Select a Book
st.sidebar.header("Filters")
# Get unique titles
titles = df['title'].unique()
selected_book = st.sidebar.selectbox("Select a Book to Analyze", titles)

# 4. Main Section: Price History Chart
st.subheader(f"Price Trend: {selected_book}")

# Filter data for just that book
book_data = df[df['title'] == selected_book].sort_values(by='scraped_at')

# Calculate current vs previous price
if len(book_data) >= 2:
    current_price = book_data.iloc[-1]['price']
    start_price = book_data.iloc[0]['price']
    delta = current_price - start_price
    st.metric(label="Current Price", value=f"£{current_price}", delta=f"{delta:.2f}")
else:
    st.write("Not enough data for metrics.")

# Draw the Line Chart
st.line_chart(book_data.set_index('scraped_at')['price'])

# 5. "Market Movers" Analysis
st.markdown("---")
st.subheader("📉 Biggest Price Drops (Last 24h)")

# Logic: Find the difference between the last two dates
# (This is complex logic that proves you know Pandas)
latest_date = df['scraped_at'].max()
yesterday = latest_date - pd.Timedelta(days=1)

today_prices = df[df['scraped_at'] == latest_date].set_index('title')['price']
yesterday_prices = df[df['scraped_at'] == yesterday].set_index('title')['price']

# Calculate the drop
diff = (today_prices - yesterday_prices).sort_values()

# Show the top 5 books that got cheaper
st.table(diff.head(5).rename("Price Change (£)"))