#!/bin/bash
# Personal Habit Tracker Unix/Linux/macOS Launcher
# This script makes it easy to run the habit tracker on Unix-like systems

echo "Personal Habit Tracker"
echo "======================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python from your package manager or https://python.org"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Run the interactive launcher
$PYTHON_CMD habit_tracker.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "An error occurred. Check the output above for details."
    read -p "Press Enter to exit..."
fi