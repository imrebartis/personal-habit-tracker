"""
Personal Habit Tracker GUI - Entry point and error handling.

This module provides the main entry point for the GUI application
and handles fallback to CLI mode when GUI is unavailable.

Philosophy: All data stays local, uses only standard library (tkinter),
hackable and extensible, distraction-free design.
"""

import tkinter as tk
from tkinter import messagebox
import sys

from .main_window import HabitTrackerGUI


def main():
    """Main entry point for GUI application with comprehensive error handling."""
    try:
        # Check if tkinter is available
        import tkinter

        # Test basic tkinter functionality
        test_root = tk.Tk()
        test_root.withdraw()
        test_root.destroy()

    except ImportError:
        print("❌ Error: tkinter is not available.")
        print("GUI mode requires tkinter, which should be included with Python.")
        print("Please use the CLI version instead: python personal_habit_tracker.py")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error: tkinter is not working properly: {e}")
        print("This might be due to display issues or missing GUI libraries.")
        print("Falling back to CLI mode...")
        fallback_to_cli()
        return

    # Try to create and run GUI application
    try:
        app = HabitTrackerGUI()
        app.run()

    except KeyboardInterrupt:
        print("\n👋 GUI application interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error starting GUI application: {e}")

        # Show error dialog if possible
        try:
            error_root = tk.Tk()
            error_root.withdraw()
            messagebox.showerror(
                "GUI Error",
                f"Failed to start GUI application:\n\n{e}\n\nWould you like to use CLI mode instead?"
            )
            error_root.destroy()
        except:
            pass

        print("Falling back to CLI mode...")
        fallback_to_cli()


def fallback_to_cli():
    """Fallback to CLI mode when GUI fails."""
    try:
        from personal_habit_tracker import main as cli_main
        print("Starting CLI version...")
        cli_main()
    except Exception as cli_error:
        print(f"❌ CLI fallback also failed: {cli_error}")
        print("Please check your Python installation and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()