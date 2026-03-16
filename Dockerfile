# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install required dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose the port (Render handles mapping automatically via the $PORT env var)
EXPOSE 10000

# Run the server
if __name__ == "__main__":
    print(f"Starting Cloudlink 4.0 server on port {port}...")
    # Cloudlink 4 usually expects 'ip' instead of 'host'
    server_inst.run(ip="0.0.0.0", port=port)
