FROM python:3.11-slim

WORKDIR /app

# Install dependencies in one go
RUN pip install --no-cache-dir cloudlink ujson cerberus snowflake-id websockets

# Copy your code
COPY . .

# Cloudlink servers usually need to stay unbuffered to see logs in Render
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
