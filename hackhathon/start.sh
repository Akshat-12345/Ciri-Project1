#!/bin/bash

echo "Starting Ciri AI Server..."

# Activate virtual environment (if used)
source venv/bin/activate  # For Linux/macOS
# source venv/Scripts/activate  # For Windows (Git Bash)

# Install dependencies
pip install -r requirements.txt

# Run the Python server
python server.py

echo "Server has stopped."
