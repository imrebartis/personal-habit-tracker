"""
Personal Habit Tracker - A minimalist command-line habit tracking application.

This application embodies the philosophy that meaningful change happens through
small, consistent daily actions. It prioritizes privacy, simplicity, and user
control while providing essential habit formation features.

Philosophy: All data stays local, no external dependencies, hackable and extensible.
"""

# TODO - Remaining tasks from spec (.kiro/specs/personal-habit-tracker-core/tasks.md):
# 10. Add optional GUI interface with tkinter
#
# Future enhancements (philosophy-compliant for THIS project):
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
import sys
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

    Raises:
        ValueError: If date string format is invalid.
        TypeError: If habit data structure is malformed.
    """
    if not isinstance(habits, list):
        raise TypeError("Habits data must be a list")

    for i, habit in enumerate(habits):
        if not isinstance(habit, dict):
            raise TypeError(f"Habit at index {i} must be a dictionary")

        if habit.get('last_completed'):
            try:
                habit['last_completed'] = datetime.datetime.strptime(
                    habit['last_completed'], '%Y-%m-%d'
                ).date()
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid date format in habit '{habit.get('habit', 'unknown')}': {e}")


def load_habits() -> List[Dict]:
    """
    Load habits from JSON file, converting date strings to date objects.

    Returns:
        List of habit dictionaries with converted date objects.
        Returns empty list if file doesn't exist or on error.
    """
    if not Path(HABITS_FILE).exists():
        return []

    try:
        with open(HABITS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"⚠️  Warning: Could not read habits file ({e}). Starting fresh.")
        return []
    except (OSError, IOError) as e:
        print(f"⚠️  Warning: Could not access habits file ({e}). Starting fresh.")
        return []

    # Validate and convert data
    try:
        if not isinstance(data, list):
            print("⚠️  Warning: Habits file format is invalid. Starting fresh.")
            return []

        # Validate required fields for each habit
        for i, habit in enumerate(data):
            if not isinstance(habit, dict):
                print(f"⚠️  Warning: Invalid habit data at position {i}. Starting fresh.")
                return []

            required_fields = ['habit', 'total_completed', 'current_streak']
            for field in required_fields:
                if field not in habit:
                    print(f"⚠️  Warning: Missing required field '{field}' in habit data. Starting fresh.")
                    return []

            # Validate data types
            if not isinstance(habit['habit'], str) or not habit['habit'].strip():
                print(f"⚠️  Warning: Invalid habit name at position {i}. Starting fresh.")
                return []

            if not isinstance(habit['total_completed'], int) or habit['total_completed'] < 0:
                print(f"⚠️  Warning: Invalid total_completed value for habit '{habit['habit']}'. Starting fresh.")
                return []

            if not isinstance(habit['current_streak'], int) or habit['current_streak'] < 0:
                print(f"⚠️  Warning: Invalid current_streak value for habit '{habit['habit']}'. Starting fresh.")
                return []

        # Convert ISO date strings back to date objects for calculations
        convert_date_strings_to_objects(data)
        return data

    except (ValueError, TypeError) as e:
        print(f"⚠️  Warning: Invalid data in habits file ({e}). Starting fresh.")
        return []

def convert_dates_for_serialization(habits: List[Dict]) -> List[Dict]:
    """
    Convert date objects to ISO strings for JSON serialization.

    Args:
        habits: List of habit dictionaries with date objects.

    Returns:
        List of habit dictionaries with date strings.

    Raises:
        TypeError: If habits is not a list or contains invalid data.
    """
    if not isinstance(habits, list):
        raise TypeError("Habits must be a list")

    result = []
    for i, habit in enumerate(habits):
        if not isinstance(habit, dict):
            raise TypeError(f"Habit at index {i} must be a dictionary")

        try:
            converted_habit = {
                **habit,
                'last_completed': habit['last_completed'].strftime('%Y-%m-%d')
                if habit.get('last_completed') else None
            }
            result.append(converted_habit)
        except (AttributeError, ValueError) as e:
            raise ValueError(f"Invalid date object in habit '{habit.get('habit', 'unknown')}': {e}")

    return result


def save_habits(habits: List[Dict]) -> None:
    """
    Save habits to JSON file, converting date objects to ISO strings.

    Args:
        habits: List of habit dictionaries to save.

    Raises:
        SystemExit: If critical save operation fails.
    """
    try:
        serializable_data = convert_dates_for_serialization(habits)
    except (TypeError, ValueError) as e:
        print(f"❌ Error: Could not prepare data for saving ({e})")
        print("Your progress for this session may be lost.")
        return

    try:
        # Create backup of existing file if it exists
        backup_path = Path(f"{HABITS_FILE}.backup")
        if Path(HABITS_FILE).exists():
            try:
                Path(HABITS_FILE).rename(backup_path)
            except OSError:
                pass  # Continue without backup if rename fails

        # Write new data
        with open(HABITS_FILE, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)

        # Remove backup on successful write
        if backup_path.exists():
            try:
                backup_path.unlink()
            except OSError:
                pass  # Leave backup if cleanup fails

    except (OSError, IOError) as e:
        print(f"❌ Error: Could not save habits file ({e})")
        print("Your progress for this session may be lost.")

        # Restore backup if write failed
        backup_path = Path(f"{HABITS_FILE}.backup")
        if backup_path.exists():
            try:
                backup_path.rename(HABITS_FILE)
                print("Previous data has been restored.")
            except OSError:
                print("Could not restore previous data.")

    except json.JSONEncodeError as e:
        print(f"❌ Error: Could not encode data for saving ({e})")
        print("Your progress for this session may be lost.")

def create_habit(name: str) -> Dict:
    """
    Create a new habit dictionary with default values.

    Args:
        name: The habit name/description.

    Returns:
        Dictionary representing a new habit with zero progress.

    Raises:
        ValueError: If name is empty or invalid.
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("Habit name must be a string")

    if not name or not name.strip():
        raise ValueError("Habit name cannot be empty")

    return {
        'habit': name.strip(),
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

    Raises:
        TypeError: If habit is not a dict or today is not a date.
        KeyError: If habit is missing required fields.
    """
    if not isinstance(habit, dict):
        raise TypeError("Habit must be a dictionary")

    if not isinstance(today, datetime.date):
        raise TypeError("Today must be a datetime.date object")

    # Validate required fields
    required_fields = ['current_streak', 'last_completed']
    for field in required_fields:
        if field not in habit:
            raise KeyError(f"Habit missing required field: {field}")

    if not isinstance(habit['current_streak'], int) or habit['current_streak'] < 0:
        raise ValueError("current_streak must be a non-negative integer")

    last_completed = habit['last_completed']

    # Validate last_completed is None or a date
    if last_completed is not None and not isinstance(last_completed, datetime.date):
        raise TypeError("last_completed must be None or a datetime.date object")

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

    Raises:
        TypeError: If habit is not a dict or today is not a date.
        KeyError: If habit is missing required fields.
    """
    if not isinstance(habit, dict):
        raise TypeError("Habit must be a dictionary")

    if not isinstance(today, datetime.date):
        raise TypeError("Today must be a datetime.date object")

    # Validate required fields
    required_fields = ['current_streak', 'last_completed']
    for field in required_fields:
        if field not in habit:
            raise KeyError(f"Habit missing required field: {field}")

    if not isinstance(habit['current_streak'], int) or habit['current_streak'] < 0:
        raise ValueError("current_streak must be a non-negative integer")

    last_completed = habit['last_completed']

    # Validate last_completed is None or a date
    if last_completed is not None and not isinstance(last_completed, datetime.date):
        raise TypeError("last_completed must be None or a datetime.date object")

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

    Raises:
        TypeError: If streak is not an int or habit_name is not a string.
        ValueError: If streak is negative.
    """
    if not isinstance(streak, int):
        raise TypeError("Streak must be an integer")

    if not isinstance(habit_name, str):
        raise TypeError("Habit name must be a string")

    if streak < 0:
        raise ValueError("Streak cannot be negative")

    if not habit_name.strip():
        habit_name = "your habit"  # Fallback for empty names

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
    max_attempts = 100  # Prevent infinite loops in automated testing

    attempt_count = 0
    while attempt_count < max_attempts:
        habit_name = ""  # Initialize variable
        try:
            habit_name = input("Enter a habit to track (or type 'done' when finished): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSetup interrupted. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️  Input error: {e}. Please try again.")
            attempt_count += 1
            continue

        if habit_name.lower() == 'done':
            break

        if habit_name:  # Only add non-empty habit names
            try:
                # Validate habit name length
                if len(habit_name) > 100:
                    print("⚠️  Habit name too long (max 100 characters). Please try a shorter name.")
                    continue

                # Check for duplicate names
                existing_names = [h['habit'].lower() for h in habits]
                if habit_name.lower() in existing_names:
                    print("⚠️  You already have a habit with that name. Please choose a different name.")
                    continue

                habits.append(create_habit(habit_name))
                print(f"✅ Added habit: {habit_name}")

            except (ValueError, TypeError) as e:
                print(f"⚠️  Invalid habit name: {e}. Please try again.")
        else:
            print("⚠️  Habit name cannot be empty. Please enter a valid name or type 'done'.")

        attempt_count += 1

    if attempt_count >= max_attempts:
        print("⚠️  Too many attempts. Exiting setup.")
        sys.exit(1)

    if not habits:
        print("⚠️  No habits were created. You need at least one habit to continue.")
        print("Exiting...")
        sys.exit(0)

    return habits

def get_user_completion_status(habit_name: str) -> bool:
    """
    Get user input for habit completion status.

    Args:
        habit_name: Name of the habit to ask about.

    Returns:
        True if user completed the habit, False otherwise.

    Raises:
        SystemExit: If user interrupts or input fails repeatedly.
    """
    if not isinstance(habit_name, str) or not habit_name.strip():
        habit_name = "this habit"  # Fallback for invalid names

    max_attempts = 10  # Prevent infinite loops
    attempt_count = 0

    while attempt_count < max_attempts:
        try:
            user_input = input(f"Did you complete '{habit_name}' today? yes/no: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n\nInput interrupted. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️  Input error: {e}. Please try again.")
            attempt_count += 1
            continue

        if user_input in ['yes', 'y', '1', 'true']:
            return True
        elif user_input in ['no', 'n', '0', 'false']:
            return False
        else:
            print("Please enter 'yes' or 'no' (or 'y'/'n')")
            attempt_count += 1

    print("⚠️  Too many invalid attempts. Assuming 'no' for this habit.")
    return False


def process_habit_completion(habit: Dict, today: datetime.date) -> bool:
    """
    Process completion of a single habit.

    Args:
        habit: Habit dictionary to process.
        today: Current date.

    Returns:
        True if habit was completed, False otherwise.
    """
    if not isinstance(habit, dict):
        print("⚠️  Error: Invalid habit data. Skipping...")
        return False

    if not isinstance(today, datetime.date):
        print("⚠️  Error: Invalid date. Skipping...")
        return False

    # Validate habit has required fields
    if 'habit' not in habit:
        print("⚠️  Error: Habit missing name. Skipping...")
        return False

    if 'total_completed' not in habit:
        habit['total_completed'] = 0  # Initialize if missing

    habit_name = habit['habit']

    try:
        completed = get_user_completion_status(habit_name)
    except Exception as e:
        print(f"⚠️  Error getting input for '{habit_name}': {e}")
        return False

    if completed:
        try:
            # Update progress and track completion
            habit['total_completed'] += 1
            update_habit_streak(habit, today)
            print('Great job! Keep up the streak! 🔥')
            return True
        except Exception as e:
            print(f"⚠️  Error updating habit '{habit_name}': {e}")
            # Rollback the increment
            habit['total_completed'] -= 1
            return False
    else:
        try:
            # Check for streak breaks and provide encouragement
            check_streak_break(habit, today)
            print('No worries! Tomorrow is another chance! 🌤️')
            return False
        except Exception as e:
            print(f"⚠️  Error checking streak for '{habit_name}': {e}")
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
    if not isinstance(habits, list):
        print("⚠️  Error: Invalid habits data.")
        return []

    if not habits:
        print("⚠️  No habits to process.")
        return []

    performed_habits = []

    try:
        today = datetime.date.today()
    except Exception as e:
        print(f"⚠️  Error getting current date: {e}")
        return []

    for i, habit in enumerate(habits):
        if not isinstance(habit, dict):
            print(f"⚠️  Skipping invalid habit at position {i}")
            continue

        try:
            if process_habit_completion(habit, today):
                habit_name = habit.get('habit', f'Habit {i+1}')
                performed_habits.append(habit_name)
        except Exception as e:
            habit_name = habit.get('habit', f'Habit {i+1}')
            print(f"⚠️  Error processing habit '{habit_name}': {e}")
            continue

    return performed_habits

def display_daily_summary(performed_habits: List[str]) -> None:
    """
    Display summary of today's completed habits.

    Args:
        performed_habits: List of habit names completed today.
    """
    try:
        if not isinstance(performed_habits, list):
            print("\n⚠️  Error displaying daily summary: Invalid data")
            return

        # Filter out any non-string items
        valid_habits = [h for h in performed_habits if isinstance(h, str) and h.strip()]

        if valid_habits:
            habits_text = ', '.join(valid_habits)
            print(f"\nHabits performed today: {habits_text}")
        else:
            print("\nNo habits performed today. Keep trying!")
    except Exception as e:
        print(f"\n⚠️  Error displaying daily summary: {e}")


def display_progress_summary(habits: List[Dict]) -> None:
    """
    Display comprehensive progress summary for all habits.

    Shows total completions, current streaks, and celebration messages
    for each habit.

    Args:
        habits: List of all habit dictionaries.
    """
    try:
        if not isinstance(habits, list):
            print("\n⚠️  Error displaying progress: Invalid habits data")
            return

        if not habits:
            print("\n📅 No habits to display.")
            return

        print("\n📅 Your Habit Progress:")

        for i, habit in enumerate(habits):
            if not isinstance(habit, dict):
                print(f"⚠️  Skipping invalid habit at position {i+1}")
                continue

            try:
                habit_name = habit.get('habit', f'Habit {i+1}')
                total_count = habit.get('total_completed', 0)
                current_streak = habit.get('current_streak', 0)

                # Validate data types
                if not isinstance(total_count, int) or total_count < 0:
                    total_count = 0
                if not isinstance(current_streak, int) or current_streak < 0:
                    current_streak = 0

                # Format habit name safely
                display_name = str(habit_name).strip().title() if habit_name else f'Habit {i+1}'

                print(f"{display_name}: {total_count} times total, {current_streak} day streak")

                # Show celebration message if streak is significant
                try:
                    streak_msg = get_streak_message(current_streak, habit_name)
                    if streak_msg:
                        print(streak_msg)
                except Exception as e:
                    # Don't let celebration message errors break the display
                    pass

            except Exception as e:
                print(f"⚠️  Error displaying habit {i+1}: {e}")
                continue

    except Exception as e:
        print(f"\n⚠️  Error displaying progress summary: {e}")


def display_results(habits: List[Dict], performed_habits: List[str]) -> None:
    """
    Display complete results including daily summary and progress.

    Args:
        habits: List of all habit dictionaries.
        performed_habits: List of habit names completed today.
    """
    try:
        display_daily_summary(performed_habits)
        display_progress_summary(habits)
    except Exception as e:
        print(f"\n⚠️  Error displaying results: {e}")
        print("Your progress has been saved, but display failed.")

def initialize_habits() -> List[Dict]:
    """
    Initialize habits by loading existing data or creating new ones.

    Returns:
        List of habit dictionaries ready for processing.

    Raises:
        SystemExit: If initialization fails critically.
    """
    try:
        habits = load_habits()
    except Exception as e:
        print(f"⚠️  Error loading habits: {e}")
        print("Starting with fresh habits...")
        habits = []

    if not habits:
        try:
            habits = setup_new_habits()
        except Exception as e:
            print(f"❌ Error setting up new habits: {e}")
            print("Cannot continue without habits. Exiting...")
            sys.exit(1)

    # Final validation
    if not isinstance(habits, list) or not habits:
        print("❌ No valid habits available. Exiting...")
        sys.exit(1)

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
    try:
        print("📝 Welcome to your Personal Habit Tracker!")

        # Initialize habits (load existing or create new)
        habits = initialize_habits()

        # Process today's habit completions
        performed_habits = process_daily_habits(habits)

        # Persist updated habit data
        save_habits(habits)

        # Show results and progress to user
        display_results(habits, performed_habits)

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Your progress has been saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("The application encountered an unexpected problem.")
        print("Your data may not have been saved properly.")
        sys.exit(1)

if __name__ == "__main__":
    main()