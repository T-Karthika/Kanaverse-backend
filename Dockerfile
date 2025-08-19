# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the backend port (change if your app runs on another port)
EXPOSE 8000

# Command to run the backend
CMD ["python", "app.py"]
