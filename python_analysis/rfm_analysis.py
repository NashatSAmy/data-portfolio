#Importing necessary libraries.
import pandas as pd
import datetime as dt

#Loading the data.
df = pd.read_csv('Sample - Superstore.csv', encoding='windows-1252')
print("Data loaded successfully.")

#Converting 'Order Date' to datetime format.
df['Order Date'] = pd.to_datetime(df['Order Date'])
analysis_date = df['Order Date'].max() + dt.timedelta(days=1)
print(f"Analysis Date set to: {analysis_date.date()}")

#Calculating RFM metrics.
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (analysis_date - x.max()).days, # Recency
    'Order ID': 'nunique', # Frequency
    'Sales': 'sum' # Monetary
}).reset_index()

rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

#Defining RFM segments.
r_labels = range(4, 0, -1) # Recency labels
f_labels = range(1, 5) # Frequency labels
m_labels = range(1, 5) # Monetary labels

#Creating RFM quartiles.
rfm['R_Quartile'] = pd.qcut(rfm['Recency'], 4, labels=r_labels)
rfm['F_Quartile'] = pd.qcut(rfm['Frequency'], 4, labels=f_labels)
rfm['M_Quartile'] = pd.qcut(rfm['Monetary'], 4, labels=m_labels)

#Combining RFM quartiles to create RFM Score.
rfm['RFM_Score'] = rfm[['R_Quartile', 'F_Quartile', 'M_Quartile']].sum(axis=1)

#Identifying top customers (RFM Score of 12).
vips = rfm[rfm['RFM_Score'] == 12]
print(f"Total VIP Customers found: {len(vips)}")
#Saving VIP customer report to a new file.
vips.to_csv('rfm_vip_customers.csv', index=False)
print("VIP customer report saved to 'rfm_vip_customers.csv'")
print(df['Sales'].dtype)    
