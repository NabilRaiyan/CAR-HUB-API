# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Run the FastAPI app on startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
