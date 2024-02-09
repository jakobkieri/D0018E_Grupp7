# Use the official Python image as the base image
FROM python:3.8-slim

# Install build dependencies
RUN apt-get update \
    && apt-get install -y build-essential libmariadb-dev-compat pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the SQL initialization script into the container at /app
COPY script.sql /app

# Copy the application code into the container at /app
COPY . /app/

# Expose port 5001 for Flask app
EXPOSE 5000



# Command to run the application and initialize the database
CMD ["sh", "-c", "python code/app.py && mysql -h localhost -u root -ppassword < /app/script.sql"]
