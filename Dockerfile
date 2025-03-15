# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the app files
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure onnxruntime is installed
RUN pip install --no-cache-dir onnxruntime

# Expose the port dynamically assigned by Render
EXPOSE $PORT

# Run the app with Uvicorn using the dynamic PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
