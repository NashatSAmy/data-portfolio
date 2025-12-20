# 1. Load the data
import pandas as pd

df = pd.read_csv('Sample - Superstore.csv', encoding='windows-1252')

# 2. Clean the Data
print("Data loaded successfully.")
print(df.head())

df['Sales'] = df['Sales'].astype(str).str.replace('$', '').astype(str).str.replace(',', '').astype(float)
df['Profit'] = df['Profit'].astype(str).str.replace('$', '').astype(str).str.replace(',', '').astype(float)

# 3. Calculate Profit Margin (Column U in your Sheet)
df['Profit Margin'] = (df['Profit'] / df['Sales'])

# 4. Group By Category (The Pivot Table)
analysis = df.groupby('Category')[['Sales', 'Profit', 'Profit Margin']].agg({'Sales': 'sum', 'Profit': 'sum', 'Profit Margin': 'mean'})

analysis['True Margin'] = analysis['Profit'] / analysis['Sales']

# 5. Format and Print
print("\n--- Python Analysis Results ---")
print(analysis)

# 6. Save results to a new file (For the client)
analysis.to_csv('final_report.csv')
print("\nReport saved to 'final_report.csv'")