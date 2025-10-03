"""
Personal Habit Tracker GUI Package

This package contains the graphical user interface components for the
Personal Habit Tracker, maintaining the project's philosophy of privacy,
simplicity, and user control.

Modules:
- gui_habit_tracker: Main entry point and error handling
- main_window: Primary application window and core functionality
- widgets: Reusable UI components
- dialogs: Modal dialog windows
"""

from .gui_habit_tracker import main
from .main_window import HabitTrackerGUI
from .dialogs import HabitManagementDialog, ProgressHistoryDialog

__all__ = ['main', 'HabitTrackerGUI', 'HabitManagementDialog', 'ProgressHistoryDialog']