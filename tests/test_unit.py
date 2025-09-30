"""
Unit tests for Personal Habit Tracker core functions.

Tests cover:
- Habit creation and initialization
- Streak calculation logic with various scenarios
- Data persistence round-trip operations
- Celebration message generation
- Error handling scenarios

Philosophy compliance: Tests maintain privacy (local only), simplicity (standard library),
and focus on core functionality without external dependencies.
"""

import unittest
import datetime
import json
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Add parent directory to path to import the module under test
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import personal_habit_tracker as pht
from tests.test_base import BaseHabitTrackerTest


class TestHabitCreation(unittest.TestCase):
    """Test habit creation and initialization functions."""

    def test_create_habit_valid_name(self):
        """Test creating a habit with a valid name."""
        habit = pht.create_habit("Exercise")

        self.assertEqual(habit['habit'], "Exercise")
        self.assertEqual(habit['total_completed'], 0)
        self.assertEqual(habit['current_streak'], 0)
        self.assertIsNone(habit['last_completed'])

    def test_create_habit_strips_whitespace(self):
        """Test that habit creation strips leading/trailing whitespace."""
        habit = pht.create_habit("  Read Books  ")
        self.assertEqual(habit['habit'], "Read Books")

    def test_create_habit_empty_name_raises_error(self):
        """Test that empty habit names raise ValueError."""
        with self.assertRaises(ValueError):
            pht.create_habit("")

        with self.assertRaises(ValueError):
            pht.create_habit("   ")

    def test_create_habit_non_string_raises_error(self):
        """Test that non-string habit names raise TypeError."""
        with self.assertRaises(TypeError):
            pht.create_habit(123)

        with self.assertRaises(TypeError):
            pht.create_habit(None)

        with self.assertRaises(TypeError):
            pht.create_habit(['Exercise'])


class TestStreakCalculation(unittest.TestCase):
    """Test streak calculation logic with various scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.today = datetime.date(2024, 1, 15)
        self.yesterday = datetime.date(2024, 1, 14)
        self.two_days_ago = datetime.date(2024, 1, 13)

    def test_update_habit_streak_first_completion(self):
        """Test streak update for first-time completion."""
        habit = pht.create_habit("Exercise")
        pht.update_habit_streak(habit, self.today)

        self.assertEqual(habit['current_streak'], 1)
        self.assertEqual(habit['last_completed'], self.today)

    def test_update_habit_streak_consecutive_days(self):
        """Test streak increment for consecutive day completion."""
        habit = pht.create_habit("Exercise")
        habit['current_streak'] = 3
        habit['last_completed'] = self.yesterday

        pht.update_habit_streak(habit, self.today)

        self.assertEqual(habit['current_streak'], 4)
        self.assertEqual(habit['last_completed'], self.today)

    def test_update_habit_streak_after_gap(self):
        """Test streak reset after missing days."""
        habit = pht.create_habit("Exercise")
        habit['current_streak'] = 5
        habit['last_completed'] = self.two_days_ago

        pht.update_habit_streak(habit, self.today)

        self.assertEqual(habit['current_streak'], 1)
        self.assertEqual(habit['last_completed'], self.today)

    def test_update_habit_streak_same_day_no_increment(self):
        """Test that completing same day multiple times doesn't increment streak."""
        habit = pht.create_habit("Exercise")
        habit['current_streak'] = 2
        habit['last_completed'] = self.today

        pht.update_habit_streak(habit, self.today)

        self.assertEqual(habit['current_streak'], 2)  # No change
        self.assertEqual(habit['last_completed'], self.today)

    def test_update_habit_streak_invalid_habit_raises_error(self):
        """Test that invalid habit data raises appropriate errors."""
        with self.assertRaises(TypeError):
            pht.update_habit_streak("not a dict", self.today)

        with self.assertRaises(TypeError):
            pht.update_habit_streak({}, "not a date")

    def test_update_habit_streak_missing_fields_raises_error(self):
        """Test that habits missing required fields raise KeyError."""
        incomplete_habit = {'habit': 'Exercise'}

        with self.assertRaises(KeyError):
            pht.update_habit_streak(incomplete_habit, self.today)

    def test_check_streak_break_no_break_yesterday(self):
        """Test that streak is not broken if completed yesterday."""
        habit = pht.create_habit("Exercise")
        habit['current_streak'] = 3
        habit['last_completed'] = self.yesterday

        pht.check_streak_break(habit, self.today)

        self.assertEqual(habit['current_streak'], 3)  # No change

    def test_check_streak_break_after_gap(self):
        """Test that streak is broken after missing multiple days."""
        habit = pht.create_habit("Exercise")
        habit['current_streak'] = 5
        habit['last_completed'] = self.two_days_ago

        pht.check_streak_break(habit, self.today)

        self.assertEqual(habit['current_streak'], 0)

    def test_check_streak_break_never_completed(self):
        """Test streak break check for never-completed habit."""
        habit = pht.create_habit("Exercise")

        pht.check_streak_break(habit, self.today)

        self.assertEqual(habit['current_streak'], 0)

    def test_check_streak_break_invalid_data_raises_error(self):
        """Test that invalid data raises appropriate errors."""
        with self.assertRaises(TypeError):
            pht.check_streak_break("not a dict", self.today)

        with self.assertRaises(TypeError):
            pht.check_streak_break({}, "not a date")


class TestCelebrationMessages(unittest.TestCase):
    """Test celebration message generation."""

    def test_get_streak_message_below_threshold(self):
        """Test that no message is returned for streaks below threshold."""
        self.assertIsNone(pht.get_streak_message(0, "Exercise"))
        self.assertIsNone(pht.get_streak_message(1, "Exercise"))
        self.assertIsNone(pht.get_streak_message(2, "Exercise"))

    def test_get_streak_message_great_threshold(self):
        """Test 'Great!' message for 3-6 day streaks."""
        message = pht.get_streak_message(3, "Exercise")
        self.assertIn("Great!", message)
        self.assertIn("3 day streak", message)
        self.assertIn("Exercise", message)

        message = pht.get_streak_message(6, "Reading")
        self.assertIn("Great!", message)
        self.assertIn("6 day streak", message)

    def test_get_streak_message_amazing_threshold(self):
        """Test 'Amazing!' message for 7+ day streaks."""
        message = pht.get_streak_message(7, "Exercise")
        self.assertIn("Amazing!", message)
        self.assertIn("1 week streak", message)
        self.assertIn("Exercise", message)

        message = pht.get_streak_message(14, "Reading")
        self.assertIn("Amazing!", message)
        self.assertIn("2 weeks streak", message)

        message = pht.get_streak_message(21, "Meditation")
        self.assertIn("Amazing!", message)
        self.assertIn("3 weeks streak", message)

    def test_get_streak_message_invalid_input_raises_error(self):
        """Test that invalid input raises appropriate errors."""
        with self.assertRaises(TypeError):
            pht.get_streak_message("not an int", "Exercise")

        with self.assertRaises(TypeError):
            pht.get_streak_message(5, 123)

        with self.assertRaises(ValueError):
            pht.get_streak_message(-1, "Exercise")

    def test_get_streak_message_empty_habit_name(self):
        """Test message generation with empty habit name."""
        message = pht.get_streak_message(5, "")
        self.assertIn("your habit", message)

        message = pht.get_streak_message(5, "   ")
        self.assertIn("your habit", message)


class TestDataPersistence(BaseHabitTrackerTest):
    """Test data persistence round-trip operations."""

    def test_load_habits_empty_file(self):
        """Test loading habits when no file exists."""
        habits = pht.load_habits()
        self.assertEqual(habits, [])

    def test_save_and_load_habits_round_trip(self):
        """Test complete save and load cycle."""
        # Create test habits
        original_habits = [
            pht.create_habit("Exercise"),
            pht.create_habit("Reading")
        ]

        # Modify some data
        original_habits[0]['total_completed'] = 5
        original_habits[0]['current_streak'] = 3
        original_habits[0]['last_completed'] = datetime.date(2024, 1, 15)

        # Save habits
        pht.save_habits(original_habits)

        # Load habits back
        loaded_habits = pht.load_habits()

        # Verify data integrity
        self.assertEqual(len(loaded_habits), 2)
        self.assertEqual(loaded_habits[0]['habit'], "Exercise")
        self.assertEqual(loaded_habits[0]['total_completed'], 5)
        self.assertEqual(loaded_habits[0]['current_streak'], 3)
        self.assertEqual(loaded_habits[0]['last_completed'], datetime.date(2024, 1, 15))

        self.assertEqual(loaded_habits[1]['habit'], "Reading")
        self.assertEqual(loaded_habits[1]['total_completed'], 0)

    def test_convert_dates_for_serialization(self):
        """Test date object to string conversion for JSON."""
        habits = [
            {
                'habit': 'Exercise',
                'total_completed': 5,
                'current_streak': 3,
                'last_completed': datetime.date(2024, 1, 15)
            },
            {
                'habit': 'Reading',
                'total_completed': 0,
                'current_streak': 0,
                'last_completed': None
            }
        ]

        converted = pht.convert_dates_for_serialization(habits)

        self.assertEqual(converted[0]['last_completed'], '2024-01-15')
        self.assertIsNone(converted[1]['last_completed'])

    def test_convert_date_strings_to_objects(self):
        """Test date string to object conversion from JSON."""
        habits = [
            {
                'habit': 'Exercise',
                'total_completed': 5,
                'current_streak': 3,
                'last_completed': '2024-01-15'
            },
            {
                'habit': 'Reading',
                'total_completed': 0,
                'current_streak': 0,
                'last_completed': None
            }
        ]

        pht.convert_date_strings_to_objects(habits)

        self.assertEqual(habits[0]['last_completed'], datetime.date(2024, 1, 15))
        self.assertIsNone(habits[1]['last_completed'])

    def test_load_habits_corrupted_json(self):
        """Test loading habits with corrupted JSON file."""
        # Create corrupted JSON file
        with open(self.test_habits_file, 'w') as f:
            f.write('{"invalid": json content')

        habits = pht.load_habits()
        self.assertEqual(habits, [])

    def test_load_habits_invalid_data_structure(self):
        """Test loading habits with invalid data structure."""
        # Create file with invalid structure
        with open(self.test_habits_file, 'w') as f:
            json.dump({"not": "a list"}, f)

        habits = pht.load_habits()
        self.assertEqual(habits, [])

    def test_load_habits_missing_required_fields(self):
        """Test loading habits with missing required fields."""
        invalid_habits = [
            {'habit': 'Exercise'},  # Missing total_completed and current_streak
            {'total_completed': 5}  # Missing habit and current_streak
        ]

        with open(self.test_habits_file, 'w') as f:
            json.dump(invalid_habits, f)

        habits = pht.load_habits()
        self.assertEqual(habits, [])


class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios."""

    def test_convert_dates_for_serialization_invalid_input(self):
        """Test error handling in date conversion for serialization."""
        with self.assertRaises(TypeError):
            pht.convert_dates_for_serialization("not a list")

        with self.assertRaises(TypeError):
            pht.convert_dates_for_serialization([{"habit": "test"}, "not a dict"])

    def test_convert_date_strings_to_objects_invalid_input(self):
        """Test error handling in date string conversion."""
        with self.assertRaises(TypeError):
            pht.convert_date_strings_to_objects("not a list")

        with self.assertRaises(TypeError):
            pht.convert_date_strings_to_objects([{"habit": "test"}, "not a dict"])

    def test_convert_date_strings_invalid_date_format(self):
        """Test error handling for invalid date formats."""
        habits = [{'habit': 'Exercise', 'last_completed': 'invalid-date'}]

        with self.assertRaises(ValueError):
            pht.convert_date_strings_to_objects(habits)

    def test_update_habit_streak_invalid_streak_value(self):
        """Test error handling for invalid streak values."""
        habit = {
            'habit': 'Exercise',
            'current_streak': -1,  # Invalid negative streak
            'last_completed': None
        }

        with self.assertRaises(ValueError):
            pht.update_habit_streak(habit, datetime.date.today())

    def test_check_streak_break_invalid_streak_value(self):
        """Test error handling for invalid streak values in break check."""
        habit = {
            'habit': 'Exercise',
            'current_streak': "not an int",  # Invalid type
            'last_completed': None
        }

        with self.assertRaises(ValueError):
            pht.check_streak_break(habit, datetime.date.today())

    @patch('builtins.open', side_effect=OSError("Permission denied"))
    def test_save_habits_file_permission_error(self, mock_file):
        """Test error handling when file cannot be written due to permissions."""
        habits = [pht.create_habit("Exercise")]

        # Should not raise exception, but handle gracefully
        pht.save_habits(habits)  # Should complete without crashing

    def test_load_habits_invalid_date_in_data(self):
        """Test loading habits with invalid date data."""
        # Create temporary file with invalid date
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        invalid_data = [
            {
                'habit': 'Exercise',
                'total_completed': 5,
                'current_streak': 3,
                'last_completed': 'not-a-date'
            }
        ]
        json.dump(invalid_data, temp_file)
        temp_file.close()

        # Temporarily change the habits file path
        original_file = pht.HABITS_FILE
        pht.HABITS_FILE = temp_file.name

        try:
            habits = pht.load_habits()
            self.assertEqual(habits, [])  # Should return empty list on error
        finally:
            pht.HABITS_FILE = original_file
            os.unlink(temp_file.name)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)