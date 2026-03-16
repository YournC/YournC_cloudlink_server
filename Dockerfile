# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install required dependencies
RUN pip install cloudlink ujson cerberus snowflake-id websockets

# Expose the port (Render handles mapping automatically via the $PORT env var)
EXPOSE 10000

# Run the server
CMD ["python", "main.py"]
