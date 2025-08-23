#!/bin/bash

echo "=== Expense Tracker Flask Backend ==="
echo "Starting server setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please make sure you're in the correct directory."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
pip list | grep -q Flask
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Test database connection
echo "Testing database connection..."
python test_db.py

if [ $? -eq 0 ]; then
    echo "✓ Database connection successful"
    echo "Starting Flask server..."
    echo "Server will be available at: http://localhost:5003"
    echo "API endpoints available at: http://localhost:5003/api/"
    echo "Press Ctrl+C to stop the server"
    echo ""
    python src/main.py
else
    echo "✗ Database connection failed"
    echo "Please check your database configuration"
    exit 1
fi

