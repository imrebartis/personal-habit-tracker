"""
Main GUI window for the Personal Habit Tracker.

This module contains the primary application window and core functionality.
Follows the project philosophy of privacy, simplicity, and user control.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from typing import List, Dict

from personal_habit_tracker import (
    load_habits, save_habits, update_habit_streak,
    get_streak_message, STREAK_CELEBRATION_THRESHOLD,
    AMAZING_STREAK_THRESHOLD
)
from .dialogs import HabitManagementDialog, ProgressHistoryDialog
from .widgets import HabitRow, CelebrationPopup


class HabitTrackerGUI:
    """Main GUI application for habit tracking."""

    def __init__(self):
        """Initialize the GUI application with error handling."""
        try:
            self.root = tk.Tk()
            self.habits = []
            self.habit_buttons = {}
            self.today_completions = {}
            self.is_closing = False

            self.root.report_callback_exception = self.handle_tk_error
            self.setup_window()
            self.create_widgets()
            self.load_data()

        except Exception as e:
            self.handle_initialization_error(e)

    def handle_initialization_error(self, error):
        """Handle errors during GUI initialization."""
        error_msg = f"Failed to initialize GUI: {error}"
        print(f"❌ {error_msg}")

        try:
            if hasattr(self, 'root') and self.root:
                messagebox.showerror("Initialization Error", error_msg)
        except:
            pass

        raise RuntimeError(error_msg)

    def handle_tk_error(self, exc_type, exc_value, exc_traceback):
        """Handle tkinter callback exceptions."""
        error_msg = f"GUI Error: {exc_value}"
        print(f"⚠️ {error_msg}")

        try:
            if not self.is_closing:
                result = messagebox.askyesno(
                    "Application Error",
                    f"An error occurred:\n\n{exc_value}\n\nContinue using the application?",
                    icon='warning'
                )
                if not result:
                    self.safe_close()
        except:
            print(f"❌ Failed to show error dialog: {exc_value}")

    def setup_window(self):
        """Configure the main window properties."""
        try:
            self.root.title("Personal Habit Tracker")

            # Screen-aware sizing
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            window_width = min(600, int(screen_width * 0.8))
            window_height = min(500, int(screen_height * 0.8))

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.minsize(500, 400)
            self.root.configure(bg='#F5F5F5')

        except Exception as e:
            print(f"⚠️ Screen detection failed: {e}")
            self.root.geometry("600x500")
            self.root.configure(bg='#F5F5F5')

        # Configure styles
        self.setup_styles()

        # Keyboard shortcuts
        self.setup_keyboard_shortcuts()

        # Focus management for accessibility
        self.focusable_widgets = []

        # Window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Action.TButton',
                       background='#E3F2FD',
                       foreground='#1976D2',
                       font=('TkDefaultFont', 10))

        style.configure('Card.TFrame',
                       background='white',
                       relief='solid',
                       borderwidth=1)

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts and accessibility."""
        self.root.bind('<Control-m>', lambda e: self.manage_habits())
        self.root.bind('<Control-h>', lambda e: self.view_history())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Escape>', lambda e: self.root.quit())

    def create_widgets(self):
        """Create and layout all GUI widgets."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = tk.Label(main_frame,
                              text="📝 Today's Habits",
                              font=('TkDefaultFont', 14, 'bold'),
                              bg='#F5F5F5',
                              fg='#333333')
        title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))

        # Habits frame
        self.create_habits_frame(main_frame)

        # Celebrations frame
        self.create_celebrations_frame(main_frame)

        # Buttons frame
        self.create_buttons_frame(main_frame)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(main_frame,
                               textvariable=self.status_var,
                               font=('TkDefaultFont', 9),
                               bg='#F5F5F5',
                               fg='#666666')
        status_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 0))

    def create_habits_frame(self, parent):
        """Create the scrollable habits display frame."""
        habits_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        habits_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        habits_frame.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        # Scrollable canvas
        canvas = tk.Canvas(habits_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(habits_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        habits_frame.rowconfigure(0, weight=1)
        habits_frame.columnconfigure(0, weight=1)

        self.habits_canvas = canvas
        canvas.bind("<MouseWheel>", self._on_mousewheel)

    def create_celebrations_frame(self, parent):
        """Create the celebrations display frame."""
        celebrations_title = tk.Label(parent,
                                    text="🎉 Celebrations",
                                    font=('TkDefaultFont', 12, 'bold'),
                                    bg='#F5F5F5',
                                    fg='#333333')
        celebrations_title.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))

        self.celebrations_frame = ttk.Frame(parent, style='Card.TFrame', padding="10")
        self.celebrations_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 15))
        self.celebrations_frame.columnconfigure(0, weight=1)
        self.celebrations_frame.grid_remove()

    def create_buttons_frame(self, parent):
        """Create the action buttons frame."""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        manage_btn = ttk.Button(buttons_frame,
                               text="Manage Habits",
                               style='Action.TButton',
                               command=self.manage_habits)
        manage_btn.grid(row=0, column=0, padx=(0, 10))

        history_btn = ttk.Button(buttons_frame,
                                text="View History",
                                style='Action.TButton',
                                command=self.view_history)
        history_btn.grid(row=0, column=1)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.habits_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_data(self):
        """Load habit data and refresh display."""
        try:
            self.habits = load_habits()
            self.verify_data_format()

            if not self.habits:
                self.show_first_time_setup()
            else:
                self.refresh_habits_display()
                self.status_var.set(f"Loaded {len(self.habits)} habits")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load habits: {e}")
            self.status_var.set("Error loading data")

    def verify_data_format(self):
        """Verify data compatibility with CLI."""
        for i, habit in enumerate(self.habits):
            required_fields = ['habit', 'total_completed', 'current_streak', 'last_completed']
            for field in required_fields:
                if field not in habit:
                    if field == 'last_completed':
                        habit[field] = None
                    elif field in ['total_completed', 'current_streak']:
                        habit[field] = 0
                    else:
                        habit[field] = f"Habit {i+1}"

            # Ensure correct data types
            if not isinstance(habit['total_completed'], int) or habit['total_completed'] < 0:
                habit['total_completed'] = 0
            if not isinstance(habit['current_streak'], int) or habit['current_streak'] < 0:
                habit['current_streak'] = 0
            if not isinstance(habit['habit'], str):
                habit['habit'] = str(habit['habit']) if habit['habit'] else f"Habit {i+1}"

    def show_first_time_setup(self):
        """Show first-time setup dialog."""
        result = messagebox.askyesno(
            "Welcome!",
            "No habits found. Would you like to create some habits to get started?",
            icon='question'
        )

        if result:
            self.manage_habits()
        else:
            self.status_var.set("No habits configured")

    def refresh_habits_display(self):
        """Refresh the habits display."""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.habit_buttons.clear()

        if not self.habits:
            empty_label = tk.Label(self.scrollable_frame,
                                  text="No habits configured.\nClick 'Manage Habits' to add some!",
                                  font=('TkDefaultFont', 11),
                                  fg='#666666',
                                  bg='white',
                                  justify=tk.CENTER)
            empty_label.grid(row=0, column=0, pady=20)
            return

        # Create habit rows
        for i, habit in enumerate(self.habits):
            habit_row = HabitRow(self.scrollable_frame, i, habit,
                               self.on_habit_complete, self.get_today_completions)
            habit_row.create()
            self.habit_buttons[i] = habit_row.complete_btn

        self.update_celebrations()

    def on_habit_complete(self, habit_index: int):
        """Handle habit completion."""
        if habit_index >= len(self.habits):
            return

        habit = self.habits[habit_index]
        today = datetime.date.today()

        try:
            habit['total_completed'] = habit.get('total_completed', 0) + 1
            update_habit_streak(habit, today)

            # Track today's completions
            habit_name = habit.get('habit', 'Unknown')
            if habit_name not in self.today_completions:
                self.today_completions[habit_name] = 0
            self.today_completions[habit_name] += 1

            # Show celebration if applicable
            streak = habit.get('current_streak', 0)
            celebration = get_streak_message(streak, habit['habit'])
            if celebration:
                self.show_celebration_popup(celebration)

            # Update status
            today_count = self.today_completions[habit_name]
            if today_count == 1:
                self.status_var.set(f"✅ Completed: {habit['habit']}")
            else:
                self.status_var.set(f"✅ Completed: {habit['habit']} ({today_count} times today)")

            self.auto_save()
            self.refresh_habits_display()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete habit: {e}")
            habit['total_completed'] = max(0, habit.get('total_completed', 0) - 1)

    def get_today_completions(self, habit: Dict) -> int:
        """Get today's completion count for a habit."""
        habit_name = habit.get('habit', 'Unknown')
        return self.today_completions.get(habit_name, 0)

    def update_celebrations(self):
        """Update celebration messages."""
        for widget in self.celebrations_frame.winfo_children():
            widget.destroy()

        celebrations = []
        for habit in self.habits:
            streak = habit.get('current_streak', 0)
            habit_name = habit.get('habit', 'Unknown')
            message = get_streak_message(streak, habit_name)
            if message:
                celebrations.append(message)

        if celebrations:
            self.celebrations_frame.grid()
            for i, message in enumerate(celebrations):
                label = tk.Label(self.celebrations_frame,
                               text=message,
                               font=('TkDefaultFont', 10),
                               bg='white',
                               fg='#FF9800' if '🏆' in message else '#4CAF50',
                               wraplength=500)
                label.grid(row=i, column=0, sticky=tk.W, pady=2)
        else:
            self.celebrations_frame.grid_remove()

    def auto_save(self):
        """Auto-save data after changes."""
        try:
            save_habits(self.habits)
        except Exception as e:
            self.status_var.set(f"⚠️ Auto-save failed: {str(e)[:30]}...")

    def manage_habits(self):
        """Open habit management dialog."""
        HabitManagementDialog(self.root, self.habits, self.on_habits_changed)

    def on_habits_changed(self):
        """Callback when habits are modified."""
        self.refresh_habits_display()
        self.status_var.set(f"Updated - {len(self.habits)} habits")

    def view_history(self):
        """Open progress history dialog."""
        ProgressHistoryDialog(self.root, self.habits)

    def show_help(self):
        """Show help dialog."""
        help_text = """
Personal Habit Tracker - Keyboard Shortcuts

Navigation:
• Tab / Shift+Tab - Navigate between elements
• Space / Enter - Complete selected habit
• Escape - Close application

Actions:
• Ctrl+M - Manage habits (add/remove)
• Ctrl+H - View progress history
• F1 - Show this help

Tips:
• Click "Complete" buttons to mark habits done
• You can complete the same habit multiple times per day
• Progress bars show your current streaks
• Celebration messages appear for milestones
• All data is saved automatically

Philosophy:
This app focuses on simplicity and privacy.
Your data stays on your machine, no accounts needed.
        """
        messagebox.showinfo("Help - Personal Habit Tracker", help_text.strip())

    def show_celebration_popup(self, message: str):
        """Show celebration popup for achievements."""
        CelebrationPopup(self.root, message).show()

    def ensure_cli_compatibility(self):
        """Ensure data format is fully compatible with CLI version."""
        for habit in self.habits:
            # Validate all required fields exist and have correct types
            if 'habit' not in habit or not isinstance(habit['habit'], str):
                habit['habit'] = 'Unknown Habit'
            if 'total_completed' not in habit or not isinstance(habit['total_completed'], int):
                habit['total_completed'] = 0
            if 'current_streak' not in habit or not isinstance(habit['current_streak'], int):
                habit['current_streak'] = 0
            if 'last_completed' not in habit:
                habit['last_completed'] = None

            # Ensure non-negative values
            habit['total_completed'] = max(0, habit['total_completed'])
            habit['current_streak'] = max(0, habit['current_streak'])

            # Ensure last_completed is None or a date object
            if habit['last_completed'] is not None and not isinstance(habit['last_completed'], datetime.date):
                habit['last_completed'] = None

    def save_progress(self):
        """Save current progress to file with CLI compatibility."""
        try:
            # Ensure data format is CLI-compatible before saving
            self.ensure_cli_compatibility()

            save_habits(self.habits)
            self.status_var.set("✅ Progress saved successfully")

            # Show temporary confirmation (with error handling)
            try:
                self.root.after(3000, lambda: self.status_var.set("Ready"))
            except tk.TclError:
                # Window may be destroyed, ignore
                pass

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save progress: {e}")
            self.status_var.set("❌ Save failed")

    def on_closing(self):
        """Handle application closing."""
        if self.is_closing:
            return

        self.is_closing = True

        try:
            save_habits(self.habits)
            self.safe_close()
        except Exception as e:
            try:
                result = messagebox.askyesnocancel(
                    "Save Error",
                    f"Failed to save progress: {e}\n\nClose anyway?",
                    icon='warning'
                )

                if result is True:
                    self.safe_close()
                elif result is False:
                    self.is_closing = False
            except Exception:
                self.safe_close()

    def safe_close(self):
        """Safely close the application."""
        try:
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
            import sys
            sys.exit(0)

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()