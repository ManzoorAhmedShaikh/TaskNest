# Use official Python image
FROM python:3.11

RUN apt-get update && apt-get install -y netcat-openbsd

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Run the app
CMD ["/wait-for-db.sh", "python", "ToDoApp/manage.py", "runserver", "0.0.0.0:8000"]