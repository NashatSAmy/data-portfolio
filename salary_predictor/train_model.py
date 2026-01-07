import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import joblib

# 1. Load Data
data = pd.read_csv('salary_data.csv')
X = data[['YearsExperience']]
y = data['Salary']

# 2. Create Polynomial Features (The "Curve" Maker)
# degree=2 means we look for x^2 patterns (Parabola)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# 3. Split Data (Note: We use X_poly now, not X)
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# 4. Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Check Accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Polynomial Model Trained! Accuracy: {accuracy:.2f}")

# 6. Save BOTH the Model AND the Converter
# We need the converter to transform the user's input in the app later
joblib.dump(model, 'salary_model.pkl')
joblib.dump(poly, 'poly_converter.pkl')
print("💾 Model and Converter saved.")