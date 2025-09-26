"""
Personal Habit Tracker - A minimalist command-line habit tracking application.

This application embodies the philosophy that meaningful change happens through
small, consistent daily actions. It prioritizes privacy, simplicity, and user
control while providing essential habit formation features.

Philosophy: All data stays local, no external dependencies, hackable and extensible.
"""

# TODO - Remaining tasks from spec (.kiro/specs/personal-habit-tracker-core/tasks.md):
# 8.1 Add error handling and robustness - Implement graceful error handling for file operations
# THEN: 9.1 Write unit tests for core functions - Test habit creation, streak calculation, data persistence
# THEN: 9.2 Write integration tests for workflows - Test complete application runs with mock input
#
# Future enhancements (philosophy-compliant for THIS project):
# - Add a GUI (graphical interface) with tkinter (optional, standard library)
# - Add data export capabilities (CSV, plain text) for user control
# - Add habit categories or tags (simple, local organization)
# - Add configurable streak reset policies (user choice, local settings)
# - Add habit completion history view (show past week/month progress)
#
# Ideas for SEPARATE projects (would violate this project's philosophy of simplicity):
# - Connect to APIs and fetch live data (violates privacy/local-only principle)
# - Try pygame for game development (violates simplicity, adds complexity)
# - Explore pandas and matplotlib for data projects (violates minimal dependencies)
# - Web interface or mobile apps (violates hackability and local-only storage)
# - Social features or sharing (violates privacy-first philosophy)
#
# These complex ideas could inspire new projects that build on this foundation
# while serving different philosophies (e.g., "Advanced Habit Analytics" or "Social Habit Tracker")

import datetime
import json
from pathlib import Path
from typing import List, Dict, Optional

# Configuration constants
HABITS_FILE = "habits_data.json"
STREAK_CELEBRATION_THRESHOLD = 3
AMAZING_STREAK_THRESHOLD = 7

def convert_date_strings_to_objects(habits: List[Dict]) -> None:
    """
    Convert ISO date strings to date objects in habit data.

    Args:
        habits: List of habit dictionaries to convert in-place.
    """
    for habit in habits:
        if habit.get('last_completed'):
            habit['last_completed'] = datetime.datetime.strptime(
                habit['last_completed'], '%Y-%m-%d'
            ).date()


def load_habits() -> List[Dict]:
    """
    Load habits from JSON file, converting date strings to date objects.

    Returns:
        List of habit dictionaries with converted date objects.
        Returns empty list if file doesn't exist.
    """
    if not Path(HABITS_FILE).exists():
        return []

    with open(HABITS_FILE, 'r') as f:
        data = json.load(f)

    # Convert ISO date strings back to date objects for calculations
    convert_date_strings_to_objects(data)
    return data

def convert_dates_for_serialization(habits: List[Dict]) -> List[Dict]:
    """
    Convert date objects to ISO strings for JSON serialization.

    Args:
        habits: List of habit dictionaries with date objects.

    Returns:
        List of habit dictionaries with date strings.
    """
    return [
        {
            **habit,
            'last_completed': habit['last_completed'].strftime('%Y-%m-%d')
            if habit.get('last_completed') else None
        }
        for habit in habits
    ]


def save_habits(habits: List[Dict]) -> None:
    """
    Save habits to JSON file, converting date objects to ISO strings.

    Args:
        habits: List of habit dictionaries to save.
    """
    serializable_data = convert_dates_for_serialization(habits)

    with open(HABITS_FILE, 'w') as f:
        json.dump(serializable_data, f, indent=2)

def create_habit(name: str) -> Dict:
    """
    Create a new habit dictionary with default values.

    Args:
        name: The habit name/description.

    Returns:
        Dictionary representing a new habit with zero progress.
    """
    return {
        'habit': name,
        'total_completed': 0,
        'current_streak': 0,
        'last_completed': None
    }

def update_habit_streak(habit: Dict, today: datetime.date) -> None:
    """
    Update habit streak based on completion date.

    Streak logic:
    - If completed yesterday: increment existing streak
    - If not completed today already: start new streak (1 day)
    - Multiple completions same day: no additional increment

    Args:
        habit: Habit dictionary to update.
        today: Current date for streak calculation.
    """
    last_completed = habit['last_completed']
    yesterday = today - datetime.timedelta(days=1)

    if last_completed == yesterday:
        # Consecutive day completion - increment streak
        habit['current_streak'] += 1
    elif last_completed != today:
        # New streak starts today (handles gaps and first completion)
        habit['current_streak'] = 1

    # Update last completion date
    habit['last_completed'] = today

def check_streak_break(habit: Dict, today: datetime.date) -> None:
    """
    Check if streak should be broken for incomplete habit.

    Breaks streak if last completion was more than one day ago.
    This handles missed days by resetting streak to 0.

    Args:
        habit: Habit dictionary to check.
        today: Current date for gap calculation.
    """
    last_completed = habit['last_completed']
    day_before_yesterday = today - datetime.timedelta(days=1)

    # Break streak if there's a gap of more than one day
    if last_completed and last_completed < day_before_yesterday:
        habit['current_streak'] = 0

def get_streak_message(streak: int, habit_name: str) -> Optional[str]:
    """
    Get appropriate streak celebration message based on streak length.

    Celebration thresholds:
    - 7+ days: Amazing message with week count
    - 3+ days: Great message with day count
    - < 3 days: No celebration message

    Args:
        streak: Current streak count.
        habit_name: Name of the habit for personalized message.

    Returns:
        Celebration message string or None if below threshold.
    """
    if streak >= AMAZING_STREAK_THRESHOLD:
        weeks = streak // 7
        week_text = 'week' if weeks == 1 else 'weeks'
        return f"🏆 Amazing! {weeks} {week_text} streak for {habit_name}!"
    elif streak >= STREAK_CELEBRATION_THRESHOLD:
        return f"🔥 Great! {streak} day streak for {habit_name}!"

    return None

def setup_new_habits() -> List[Dict]:
    """
    Interactive setup workflow for creating initial habits.

    Prompts user to enter habit names until they type 'done'.
    Each habit is initialized with zero progress.

    Returns:
        List of newly created habit dictionaries.
    """
    habits = []
    print("No existing habits found. Let's create some!")

    while True:
        habit_name = input("Enter a habit to track (or type 'done' when finished): ").strip()

        if habit_name.lower() == 'done':
            break

        if habit_name:  # Only add non-empty habit names
            habits.append(create_habit(habit_name))

    return habits

def get_user_completion_status(habit_name: str) -> bool:
    """
    Get user input for habit completion status.

    Args:
        habit_name: Name of the habit to ask about.

    Returns:
        True if user completed the habit, False otherwise.
    """
    while True:
        user_input = input(f"Did you complete '{habit_name}' today? yes/no: ").strip().lower()

        if user_input in ['yes', 'y']:
            return True
        elif user_input in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")


def process_habit_completion(habit: Dict, today: datetime.date) -> bool:
    """
    Process completion of a single habit.

    Args:
        habit: Habit dictionary to process.
        today: Current date.

    Returns:
        True if habit was completed, False otherwise.
    """
    habit_name = habit['habit']
    completed = get_user_completion_status(habit_name)

    if completed:
        # Update progress and track completion
        habit['total_completed'] += 1
        update_habit_streak(habit, today)
        print('Great job! Keep up the streak! 🔥')
        return True
    else:
        # Check for streak breaks and provide encouragement
        check_streak_break(habit, today)
        print('No worries! Tomorrow is another chance! 🌤️')
        return False


def process_daily_habits(habits: List[Dict]) -> List[str]:
    """
    Process daily habit completion workflow.

    Prompts user for each habit's completion status, updates progress,
    and provides immediate feedback for motivation.

    Args:
        habits: List of habit dictionaries to process.

    Returns:
        List of habit names that were completed today.
    """
    performed_habits = []
    today = datetime.date.today()

    for habit in habits:
        if process_habit_completion(habit, today):
            performed_habits.append(habit['habit'])

    return performed_habits

def display_daily_summary(performed_habits: List[str]) -> None:
    """
    Display summary of today's completed habits.

    Args:
        performed_habits: List of habit names completed today.
    """
    if performed_habits:
        habits_text = ', '.join(performed_habits)
        print(f"\nHabits performed today: {habits_text}")
    else:
        print("\nNo habits performed today. Keep trying!")


def display_progress_summary(habits: List[Dict]) -> None:
    """
    Display comprehensive progress summary for all habits.

    Shows total completions, current streaks, and celebration messages
    for each habit.

    Args:
        habits: List of all habit dictionaries.
    """
    print("\n📅 Your Habit Progress:")

    for habit in habits:
        habit_name = habit['habit'].title()
        total_count = habit['total_completed']
        current_streak = habit['current_streak']

        print(f"{habit_name}: {total_count} times total, {current_streak} day streak")

        # Show celebration message if streak is significant
        streak_msg = get_streak_message(current_streak, habit['habit'])
        if streak_msg:
            print(streak_msg)


def display_results(habits: List[Dict], performed_habits: List[str]) -> None:
    """
    Display complete results including daily summary and progress.

    Args:
        habits: List of all habit dictionaries.
        performed_habits: List of habit names completed today.
    """
    display_daily_summary(performed_habits)
    display_progress_summary(habits)

def initialize_habits() -> List[Dict]:
    """
    Initialize habits by loading existing data or creating new ones.

    Returns:
        List of habit dictionaries ready for processing.
    """
    habits = load_habits()

    if not habits:
        habits = setup_new_habits()

    return habits


def main():
    """
    Main application entry point.

    Orchestrates the complete habit tracking workflow:
    1. Welcome user and initialize habits
    2. Process daily habit completions
    3. Save updated progress
    4. Display results and progress summary
    """
    print("📝 Welcome to your Personal Habit Tracker!")

    # Initialize habits (load existing or create new)
    habits = initialize_habits()

    # Process today's habit completions
    performed_habits = process_daily_habits(habits)

    # Persist updated habit data
    save_habits(habits)

    # Show results and progress to user
    display_results(habits, performed_habits)

if __name__ == "__main__":
    main()