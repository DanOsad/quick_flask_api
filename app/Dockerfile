# Use Python base image
FROM python:3.6.9-alpine

# Install dependencies for any package compilation
RUN apk update
RUN apk add --no-cache build-base libffi-dev gpgme-dev

# Run the container as a non-root user (optional security step)
RUN adduser --disabled-password flaskuser

# Create a folder for your application inside the container
WORKDIR /app

# Copy requirements file first, to cache them in docker layers if they don’t change
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Change ownership of the entire app directory
RUN chown -R flaskuser:flaskuser /app

# Define the Flask environment (optional but recommended)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Use user flaskuser (non-priveleged)
USER flaskuser

# Start the Flask app
CMD ["python", "app.py"]