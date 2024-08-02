# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and other necessary files into the container
COPY outliers.py /app/
COPY D:/LSEG/LSE/FLTRLSE.CSV /app/ 

# Set the default command to run the script
CMD ["python", "outliers.py"]
