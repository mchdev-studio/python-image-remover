# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn rembg pillow

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
