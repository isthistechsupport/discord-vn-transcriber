# Using an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY bot.py .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

# Run bot.py when the container launches
CMD [ "python", "bot.py" ]
