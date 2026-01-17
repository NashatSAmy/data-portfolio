# 1. Use an official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the container to /app
WORKDIR /app

# 3. Copy the dependency file first (for caching speed)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your code into the container
COPY . .

# 6. Tell Docker this container listens on port 8501 (Streamlit default)
EXPOSE 8501

# 7. The command to run when the container starts
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]