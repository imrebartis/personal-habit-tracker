@echo off
REM Personal Habit Tracker Windows Launcher
REM This batch file makes it easy to run the habit tracker on Windows

echo Personal Habit Tracker
echo ======================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Run the interactive launcher
python habit_tracker.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)