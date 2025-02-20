# Use an official Python image
FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port
EXPOSE 5000

# Run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "ocr:app"]
