#!/bin/bash

# Set -e option to exit immediately if a command exits with a non-zero status
set -e

# Function to print colored messages
print_color() {
    case $1 in
        "green") echo -e "\033[0;32m$2\033[0m" ;;
        "red")   echo -e "\033[0;31m$2\033[0m" ;;
        "yellow") echo -e "\033[1;33m$2\033[0m" ;;
    esac
}

# Function to create directory with sudo if necessary
create_directory() {
    if mkdir -p "$1"; then
        print_color "green" "Directory $1 created successfully."
    else
        print_color "yellow" "Permission denied. Attempting with sudo..."
        if sudo mkdir -p "$1"; then
            print_color "green" "Directory $1 created successfully with sudo."
        else
            print_color "red" "Failed to create directory $1 even with sudo."
            exit 1
        fi
    fi
}

# Print header
print_color "green" "Setting up Blippy..."

# Create and activate virtual environment
print_color "yellow" "Creating virtual environment..."
python -m venv .venv || { print_color "red" "Failed to create virtual environment."; exit 1; }
source .venv/bin/activate || { print_color "red" "Failed to activate virtual environment."; exit 1; }

# Install dependencies
print_color "yellow" "Installing dependencies..."
pip install -r requirements.txt || { print_color "red" "Failed to install dependencies."; exit 1; }

# Build the executable
print_color "yellow" "Building executable..."
pyinstaller --onefile --windowed blippy.py || { print_color "red" "Failed to build executable."; exit 1; }

# Move the executable to PATH
print_color "yellow" "Moving executable to PATH..."
sudo mv dist/blippy /usr/local/bin/ || { print_color "red" "Failed to move executable to PATH."; exit 1; }

# Create reactions directory if it doesn't exist
print_color "yellow" "Creating reactions directory..."
create_directory "/usr/local/bin/reactions"

# Unzip reactions.zip and move it alongside the executable
print_color "yellow" "Unzipping reactions.zip..."
if [ -f "reactions.zip" ]; then
    unzip reactions.zip || { print_color "red" "Failed to unzip reactions.zip."; exit 1; }
    sudo mv reactions/* /usr/local/bin/reactions/
    print_color "yellow" "Contents of reactions.zip:"
    sudo ls -l /usr/local/bin/reactions/
else
    print_color "yellow" "No reactions.zip found. Creating default folder."
fi

# Print success message
print_color "green" "Setup complete! Blippy is now ready to use."