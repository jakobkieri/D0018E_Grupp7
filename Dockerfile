# Use an official MySQL runtime as the base image
FROM mysql:latest

# Environment variables
ENV MYSQL_ROOT_PASSWORD=bingus
ENV MYSQL_DATABASE=mydb

# Copy the SQL file into the Docker image
COPY script.sql /docker-entrypoint-initdb.d/

# Expose port 3306 to allow external connections to the database
EXPOSE 3306