#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Run database initialization
echo "Initializing database..."
python -m app.init_models

# Start the main application
echo "Starting scraper..."
exec python -m app.main 