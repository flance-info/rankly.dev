FROM python:3.11.3

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Rest of your Dockerfile...
WORKDIR /app

# Copy requirements if you have them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Any other commands you have... 