# TODO - Remaining tasks from spec (.kiro/specs/personal-habit-tracker-core/tasks.md):
# PRIORITY: 7.1 Optimize code structure and readability - Refactor complex functions, ensure consistent style
# THEN: 8.1 Add error handling and robustness - Implement graceful error handling for file operations
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

HABITS_FILE = "habits_data.json"

def load_habits() -> List[Dict]:
    """Load habits from JSON file, converting date strings to date objects."""
    if not Path(HABITS_FILE).exists():
        return []

    with open(HABITS_FILE, 'r') as f:
        data = json.load(f)

    # Convert date strings back to date objects in-place
    for habit in data:
        if habit.get('last_completed'):
            habit['last_completed'] = datetime.datetime.strptime(
                habit['last_completed'], '%Y-%m-%d').date()
    return data

def save_habits(habits: List[Dict]) -> None:
    """Save habits to JSON file, converting date objects to strings."""
    # Use list comprehension for more efficient conversion
    data = [
        {**habit, 'last_completed': habit['last_completed'].strftime('%Y-%m-%d')
         if habit.get('last_completed') else None}
        for habit in habits
    ]

    with open(HABITS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_habit(name: str) -> Dict:
    """Create a new habit dictionary."""
    return {
        'habit': name,
        'total_completed': 0,
        'current_streak': 0,
        'last_completed': None
    }

def update_habit_streak(habit: Dict, today: datetime.date) -> None:
    """Update habit streak based on completion date."""
    last_completed = habit['last_completed']

    if last_completed == today - datetime.timedelta(days=1):
        habit['current_streak'] += 1
    elif last_completed != today:
        habit['current_streak'] = 1

    habit['last_completed'] = today

def check_streak_break(habit: Dict, today: datetime.date) -> None:
    """Check if streak should be broken for incomplete habit."""
    if (habit['last_completed'] and
        habit['last_completed'] < today - datetime.timedelta(days=1)):
        habit['current_streak'] = 0

def get_streak_message(streak: int, habit_name: str) -> Optional[str]:
    """Get appropriate streak celebration message."""
    if streak >= 7:
        weeks = streak // 7
        return f"🏆 Amazing! {weeks} week{'s' if weeks > 1 else ''} streak for {habit_name}!"
    elif streak >= 3:
        return f"🔥 Great! {streak} day streak for {habit_name}!"
    return None

def setup_new_habits() -> List[Dict]:
    """Interactive setup for new habits."""
    habits = []
    print("No existing habits found. Let's create some!")

    while True:
        habit_name = input("Enter a habit to track (or type 'done' when finished): ")
        if habit_name.lower() == 'done':
            break
        habits.append(create_habit(habit_name))

    return habits

def process_daily_habits(habits: List[Dict]) -> List[str]:
    """Process daily habit completion and return list of completed habits."""
    performed_habits = []
    today = datetime.date.today()

    for habit in habits:
        completed = input(f"Did you complete '{habit['habit']}' today? yes/no: ").lower() == 'yes'

        if completed:
            habit['total_completed'] += 1
            performed_habits.append(habit['habit'])
            update_habit_streak(habit, today)
            print('Great job! Keep up the streak! 🔥')
        else:
            check_streak_break(habit, today)
            print('No worries! Tomorrow is another chance! 🌤️')

    return performed_habits

def display_results(habits: List[Dict], performed_habits: List[str]) -> None:
    """Display daily results and progress summary."""
    # Show today's results
    if performed_habits:
        print(f"\nHabits performed today: {', '.join(performed_habits)}")
    else:
        print("\nNo habits performed today. Keep trying!")

    # Show progress summary
    print("\n📅 Your Habit Progress:")
    for habit in habits:
        print(f"{habit['habit'].title()}: {habit['total_completed']} times total, "
              f"{habit['current_streak']} day streak")

        # Show streak celebration if applicable
        streak_msg = get_streak_message(habit['current_streak'], habit['habit'])
        if streak_msg:
            print(streak_msg)

def main():
    """Main application entry point."""
    print("📝 Welcome to your Personal Habit Tracker!")

    # Load or create habits
    habits = load_habits() or setup_new_habits()

    # Process today's habits
    performed_habits = process_daily_habits(habits)

    # Save updated data
    save_habits(habits)

    # Display results
    display_results(habits, performed_habits)

if __name__ == "__main__":
    main()