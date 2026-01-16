#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    echo "Installing dependencies..."
    source $VENV_DIR/bin/activate
    pip install -r requirements.txt
else
    source $VENV_DIR/bin/activate
fi

# Run the game
echo "Starting Space Shooter..."
python main.py
