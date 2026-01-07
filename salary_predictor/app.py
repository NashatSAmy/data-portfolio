import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import numpy as np
import os 

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(script_dir, 'salary_data.csv')
model_path = os.path.join(script_dir, 'salary_model.pkl')
poly_path = os.path.join(script_dir, 'poly_converter.pkl')
# Load model and poly converter
model = joblib.load(model_path)
poly = joblib.load(poly_path)
data = pd.read_csv(csv_path)

# 1. Load Model, Converter, and Data
model = joblib.load('salary_model.pkl')
poly = joblib.load('poly_converter.pkl') # Load the tool that creates the curve
data = pd.read_csv('salary_data.csv')

st.title("💰 AI Salary Predictor (Polynomial)")
st.write("This model uses Polynomial Regression to capture the 'curved' growth of salaries.")

# 2. Sidebar
years = st.slider("Years of Experience:", 0.0, 15.0, 5.0, 0.1)

# 3. Prediction Logic
if st.button("Predict Salary"):
    # A. Prepare Input
    input_data = pd.DataFrame([[years]], columns=['YearsExperience'])
    
    # B. Transform Input (Turn "5" into "5, 25")
    input_poly = poly.transform(input_data)
    
    # C. Predict
    prediction = model.predict(input_poly)[0]
    
    st.success(f"Estimated Salary: ${prediction:,.2f}")
    
    # 4. The Curved Graph
    st.subheader("📊 Visualizing the Curve")
    fig, ax = plt.subplots()
    
    # Plot Real Data (Blue Dots)
    ax.scatter(data['YearsExperience'], data['Salary'], color='blue', label='Actual Data')
    
    # Plot The Curve (Red Line)
    # Create a range of numbers (0 to 15)
    X_range = pd.DataFrame(np.arange(0, 16, 0.1), columns=['YearsExperience'])
    # Transform them to polynomial too
    X_range_poly = poly.transform(X_range)
    # Predict
    y_range = model.predict(X_range_poly)
    
    ax.plot(X_range['YearsExperience'], y_range, color='red', linewidth=2, label='Polynomial Trend')
    
    # Plot User Prediction (Green Star)
    ax.scatter([years], [prediction], color='green', s=200, marker='*', label='Your Prediction')
    
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)