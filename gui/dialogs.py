"""
Dialog windows for the Personal Habit Tracker GUI.

This module contains modal dialogs for habit management and progress viewing,
maintaining the project's philosophy of simplicity and user control.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional, Callable

from personal_habit_tracker import create_habit, get_streak_message


class HabitManagementDialog:
    """Dialog for managing habits (add/remove)."""

    def __init__(self, parent, habits: List[Dict], callback: Callable):
        self.habits = habits
        self.callback = callback

        # Create modal dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Manage Habits")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))

        self.create_widgets()
        self.refresh_habits_list()
        self.dialog.protocol("WM_DELETE_WINDOW", self.close_dialog)

    def create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Current habits section
        tk.Label(main_frame,
                text="Current Habits:",
                font=('TkDefaultFont', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Habits listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.habits_listbox = tk.Listbox(list_frame, font=('TkDefaultFont', 10))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.habits_listbox.yview)
        self.habits_listbox.configure(yscrollcommand=scrollbar.set)

        self.habits_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Remove button
        remove_btn = ttk.Button(main_frame,
                               text="Remove Selected",
                               command=self.remove_habit)
        remove_btn.pack(pady=(0, 20))

        # Add new habit section
        tk.Label(main_frame,
                text="Add New Habit:",
                font=('TkDefaultFont', 12, 'bold')).pack(anchor=tk.W)

        add_frame = ttk.Frame(main_frame)
        add_frame.pack(fill=tk.X, pady=(5, 20))

        self.new_habit_var = tk.StringVar()
        self.new_habit_entry = ttk.Entry(add_frame,
                                        textvariable=self.new_habit_var,
                                        font=('TkDefaultFont', 10))
        self.new_habit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        add_btn = ttk.Button(add_frame,
                            text="Add Habit",
                            command=self.add_habit)
        add_btn.pack(side=tk.RIGHT)

        # Bind Enter key
        self.new_habit_entry.bind('<Return>', lambda e: self.add_habit())

        # Close button
        close_btn = ttk.Button(main_frame,
                              text="Close",
                              command=self.close_dialog)
        close_btn.pack(pady=(10, 0))

        # Focus on entry
        self.new_habit_entry.focus()

    def refresh_habits_list(self):
        """Refresh the habits listbox."""
        self.habits_listbox.delete(0, tk.END)

        for habit in self.habits:
            habit_name = habit.get('habit', 'Unknown')
            total = habit.get('total_completed', 0)
            streak = habit.get('current_streak', 0)
            display_text = f"{habit_name} ({total} total, {streak} streak)"
            self.habits_listbox.insert(tk.END, display_text)

    def add_habit(self):
        """Add a new habit with validation."""
        try:
            habit_name = self.new_habit_var.get().strip()

            # Validate input
            validation_error = self.validate_habit_name(habit_name)
            if validation_error:
                messagebox.showwarning("Invalid Input", validation_error)
                return

            # Check for duplicates
            existing_names = [h.get('habit', '').lower() for h in self.habits]
            if habit_name.lower() in existing_names:
                messagebox.showwarning("Duplicate Habit", "A habit with this name already exists.")
                return

            # Create and add habit
            new_habit = create_habit(habit_name)
            self.habits.append(new_habit)
            self.refresh_habits_list()
            self.new_habit_var.set("")

            # Notify parent
            if self.callback:
                self.callback()

        except Exception as e:
            error_msg = f"Failed to add habit: {e}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def validate_habit_name(self, name: str) -> Optional[str]:
        """Validate habit name and return error message if invalid."""
        if not name:
            return "Please enter a habit name."

        if len(name) > 100:
            return "Habit name is too long (maximum 100 characters)."

        if len(name) < 2:
            return "Habit name is too short (minimum 2 characters)."

        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in name:
                return f"Habit name cannot contain the character: {char}"

        # Check if name is only whitespace or special characters
        if not any(c.isalnum() for c in name):
            return "Habit name must contain at least one letter or number."

        return None

    def remove_habit(self):
        """Remove selected habit."""
        selection = self.habits_listbox.curselection()

        if not selection:
            messagebox.showwarning("No Selection", "Please select a habit to remove.")
            return

        index = selection[0]
        habit_name = self.habits[index].get('habit', 'Unknown')

        result = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove '{habit_name}'?\n\nThis will delete all progress data for this habit.",
            icon='warning'
        )

        if result:
            try:
                del self.habits[index]
                self.refresh_habits_list()

                if self.callback:
                    self.callback()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove habit: {e}")

    def close_dialog(self):
        """Close the dialog."""
        self.dialog.destroy()


class ProgressHistoryDialog:
    """Dialog for viewing progress history."""

    def __init__(self, parent, habits: List[Dict]):
        self.habits = habits

        # Create modal dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Progress History")
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center on parent
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 25,
            parent.winfo_rooty() + 25
        ))

        self.create_widgets()
        self.dialog.protocol("WM_DELETE_WINDOW", self.close_dialog)

    def create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame,
                text="📊 Overall Progress",
                font=('TkDefaultFont', 14, 'bold')).pack(anchor=tk.W, pady=(0, 15))

        # Progress display with scrollbar
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Display habits progress
        if not self.habits:
            tk.Label(scrollable_frame,
                    text="No habits to display.",
                    font=('TkDefaultFont', 11),
                    fg='#666666').pack(pady=20)
        else:
            for i, habit in enumerate(self.habits):
                self.create_progress_row(scrollable_frame, i, habit)

        # Close button
        close_btn = ttk.Button(main_frame,
                              text="Close",
                              command=self.close_dialog)
        close_btn.pack(pady=(20, 0))

        # Bind mousewheel
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def create_progress_row(self, parent, index: int, habit: Dict):
        """Create a progress display row for a habit."""
        row_frame = ttk.Frame(parent, padding="10")
        row_frame.pack(fill=tk.X, pady=5)

        # Habit name
        habit_name = habit.get('habit', 'Unknown Habit')
        name_label = tk.Label(row_frame,
                             text=f"{habit_name}:",
                             font=('TkDefaultFont', 11, 'bold'),
                             anchor='w')
        name_label.pack(anchor=tk.W)

        # Progress bar
        progress_frame = ttk.Frame(row_frame)
        progress_frame.pack(fill=tk.X, pady=(5, 0))

        total = habit.get('total_completed', 0)
        streak = habit.get('current_streak', 0)

        # Calculate progress bar (max 30 characters)
        max_total = max([h.get('total_completed', 0) for h in self.habits]) or 1
        progress_width = min(30, max(1, int((total / max_total) * 30)))

        progress_bar = "█" * progress_width + "░" * (30 - progress_width)
        progress_text = f"{progress_bar} {total} total, {streak} day streak"

        progress_label = tk.Label(progress_frame,
                                 text=progress_text,
                                 font=('Courier', 9),
                                 fg='#4CAF50' if streak > 0 else '#666666',
                                 anchor='w')
        progress_label.pack(anchor=tk.W)

        # Add celebration message if applicable
        message = get_streak_message(streak, habit_name)
        if message:
            celebration_label = tk.Label(row_frame,
                                       text=message,
                                       font=('TkDefaultFont', 9),
                                       fg='#FF9800' if '🏆' in message else '#4CAF50',
                                       anchor='w')
            celebration_label.pack(anchor=tk.W, pady=(2, 0))

    def close_dialog(self):
        """Close the dialog."""
        self.dialog.destroy()