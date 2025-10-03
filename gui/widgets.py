"""
Custom widgets for the Personal Habit Tracker GUI.

This module contains reusable UI components that maintain the project's
philosophy of simplicity and clean design.
"""

import tkinter as tk
from tkinter import ttk
import datetime
from typing import Dict, Callable

from personal_habit_tracker import (
    STREAK_CELEBRATION_THRESHOLD,
    AMAZING_STREAK_THRESHOLD
)


class HabitRow:
    """A single habit row widget with completion button and progress display."""

    def __init__(self, parent, index: int, habit: Dict,
                 complete_callback: Callable, today_completions_callback: Callable):
        self.parent = parent
        self.index = index
        self.habit = habit
        self.complete_callback = complete_callback
        self.today_completions_callback = today_completions_callback
        self.complete_btn = None

    def create(self):
        """Create the habit row widgets."""
        row_frame = ttk.Frame(self.parent)
        row_frame.grid(row=self.index, column=0, sticky=(tk.W, tk.E), pady=3)
        row_frame.columnconfigure(1, weight=1)

        # Completion button
        self.complete_btn = ttk.Button(row_frame,
                                      text="✓ Complete",
                                      width=12,
                                      command=lambda: self.complete_callback(self.index))
        self.complete_btn.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.complete_btn.bind('<Return>', lambda e: self.complete_callback(self.index))

        # Habit name with styling
        habit_name = self.habit.get('habit', 'Unknown Habit')
        today = datetime.date.today()
        last_completed = self.habit.get('last_completed')
        is_completed_today = last_completed == today

        name_color = '#4CAF50' if is_completed_today else '#333333'
        name_font = ('TkDefaultFont', 11, 'bold' if is_completed_today else 'normal')

        name_label = tk.Label(row_frame,
                             text=habit_name,
                             font=name_font,
                             bg='white',
                             fg=name_color,
                             anchor='w')
        name_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))

        # Streak indicator
        self.create_streak_indicator(row_frame)

        # Progress info
        self.create_progress_info(row_frame)

    def create_streak_indicator(self, parent_frame):
        """Create visual streak indicator."""
        streak = self.habit.get('current_streak', 0)

        progress_frame = tk.Frame(parent_frame, bg='white')
        progress_frame.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(5, 5))

        # Visual progress bar
        if streak > 0:
            if streak >= AMAZING_STREAK_THRESHOLD:
                bar_color = '#FF9800'
                bar_char = '█'
            elif streak >= STREAK_CELEBRATION_THRESHOLD:
                bar_color = '#4CAF50'
                bar_char = '█'
            else:
                bar_color = '#81C784'
                bar_char = '▓'

            max_display_streak = 14
            bar_width = min(20, max(1, int((streak / max_display_streak) * 20)))
            filled_bar = bar_char * min(bar_width, streak)
            empty_bar = '░' * max(0, 20 - len(filled_bar))
            progress_text = filled_bar + empty_bar
        else:
            progress_text = '░' * 20
            bar_color = '#E0E0E0'

        progress_bar_label = tk.Label(progress_frame,
                                     text=progress_text,
                                     font=('Courier', 8),
                                     bg='white',
                                     fg=bar_color)
        progress_bar_label.pack()

        # Tooltip
        self.create_tooltip(progress_bar_label, f"Current streak: {streak} days")

    def create_progress_info(self, parent_frame):
        """Create progress information display."""
        total = self.habit.get('total_completed', 0)
        streak = self.habit.get('current_streak', 0)

        # Include today's completions if any
        today_completions = self.today_completions_callback(self.habit)
        if today_completions > 0:
            progress_text = f"{total} total • {streak} streak • {today_completions} today"
        else:
            progress_text = f"{total} total • {streak} streak"

        # Color coding
        if streak >= AMAZING_STREAK_THRESHOLD:
            progress_color = '#FF9800'
        elif streak >= STREAK_CELEBRATION_THRESHOLD:
            progress_color = '#4CAF50'
        else:
            progress_color = '#666666'

        progress_label = tk.Label(parent_frame,
                                 text=progress_text,
                                 font=('TkDefaultFont', 9),
                                 bg='white',
                                 fg=progress_color)
        progress_label.grid(row=0, column=3, sticky=tk.E, padx=(10, 0))

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip,
                           text=text,
                           background='#FFFFCC',
                           foreground='#333333',
                           font=('TkDefaultFont', 9),
                           relief=tk.SOLID,
                           borderwidth=1,
                           padx=5,
                           pady=3)
            label.pack()
            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)


class CelebrationPopup:
    """Animated celebration popup for achievements."""

    def __init__(self, parent, message: str):
        self.parent = parent
        self.message = message
        self.window = None

    def show(self):
        """Show the celebration popup."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🎉 Achievement!")
        self.window.geometry("350x120")
        self.window.resizable(False, False)
        self.window.overrideredirect(True)

        # Center on parent
        self.window.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 125,
            self.parent.winfo_rooty() + 150
        ))

        # Style the popup
        self.window.configure(bg='#FFF3E0')

        border_frame = tk.Frame(self.window, bg='#FF9800', bd=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        content_frame = tk.Frame(border_frame, bg='#FFF3E0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Icon
        icon_label = tk.Label(content_frame,
                             text="🎉",
                             font=('TkDefaultFont', 24),
                             bg='#FFF3E0')
        icon_label.pack(pady=(10, 5))

        # Message
        message_label = tk.Label(content_frame,
                               text=self.message,
                               font=('TkDefaultFont', 11, 'bold'),
                               bg='#FFF3E0',
                               fg='#FF9800',
                               wraplength=320,
                               justify=tk.CENTER)
        message_label.pack(pady=(0, 10))

        # Animation
        self.animate_icon(icon_label)

        # Auto-close
        self.window.after(4000, self.close)

        # Stay on top
        self.window.transient(self.parent)
        self.window.lift()
        self.window.attributes('-topmost', True)

    def animate_icon(self, icon_label):
        """Simple pulse animation for the icon."""
        def pulse_animation(step=0):
            if step < 6 and self.window and self.window.winfo_exists():
                size = 24 + (step % 2) * 4
                icon_label.configure(font=('TkDefaultFont', size))
                self.window.after(200, lambda: pulse_animation(step + 1))
            elif self.window and self.window.winfo_exists():
                icon_label.configure(font=('TkDefaultFont', 24))

        pulse_animation()

    def close(self):
        """Close the popup."""
        if self.window:
            self.window.destroy()
            self.window = None