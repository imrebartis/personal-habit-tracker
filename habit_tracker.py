#!/usr/bin/env python3
"""
Personal Habit Tracker Launcher

A simple launcher script that provides easy access to both CLI and GUI interfaces
of the Personal Habit Tracker application.

Usage:
    python habit_tracker.py           # Interactive mode selection
    python habit_tracker.py --cli     # Direct CLI launch
    python habit_tracker.py --gui     # Direct GUI launch
"""

import sys
import os
import argparse


def main():
    """Main launcher with interface selection."""
    parser = argparse.ArgumentParser(
        description="Personal Habit Tracker Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This launcher provides easy access to both interfaces:

CLI Interface:
  - Command-line based interaction
  - Works on any system with Python
  - Minimal resource usage
  - Perfect for terminal users

GUI Interface:
  - Visual interface with checkboxes and progress bars
  - Mouse and keyboard interaction
  - Real-time progress updates
  - Celebration animations for achievements

Both interfaces share the same data file and are fully compatible.
        """
    )

    parser.add_argument(
        '--cli',
        action='store_true',
        help='Launch CLI interface directly'
    )

    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI interface directly'
    )

    args = parser.parse_args()

    # Direct launch if specified
    if args.cli:
        launch_cli()
        return
    elif args.gui:
        launch_gui()
        return

    # Interactive mode selection
    print("📝 Personal Habit Tracker")
    print("=" * 40)
    print()
    print("Choose your interface:")
    print("1. CLI (Command Line) - Default")
    print("2. GUI (Graphical Interface)")
    print("3. Exit")
    print()

    while True:
        try:
            choice = input("Enter your choice (1-3) [1]: ").strip()

            if choice == '' or choice == '1':
                launch_cli()
                break
            elif choice == '2':
                launch_gui()
                break
            elif choice == '3':
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("⚠️  Please enter 1, 2, or 3")

        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            sys.exit(0)


def launch_cli():
    """Launch CLI interface."""
    print("\n🖥️  Launching CLI interface...")
    try:
        import personal_habit_tracker
        personal_habit_tracker.launch_cli()
    except ImportError:
        print("❌ Error: personal_habit_tracker.py not found")
        print("Make sure all files are in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching CLI: {e}")
        sys.exit(1)


def launch_gui():
    """Launch GUI interface."""
    print("\n🖼️  Launching GUI interface...")

    # Check if tkinter is available
    try:
        import tkinter
    except ImportError:
        print("❌ Error: GUI interface requires tkinter")
        print("tkinter should be included with Python")
        print("Falling back to CLI interface...")
        launch_cli()
        return

    try:
        from gui import gui_habit_tracker
        gui_habit_tracker.main()
    except ImportError:
        print("❌ Error: gui_habit_tracker.py not found")
        print("Make sure all files are in the same directory")
        print("Falling back to CLI interface...")
        launch_cli()
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("Falling back to CLI interface...")
        launch_cli()


if __name__ == "__main__":
    main()