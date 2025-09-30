"""Base test class with common setup and teardown for habit tracker tests."""

import os
import tempfile
import unittest
import personal_habit_tracker as pht


class BaseHabitTrackerTest(unittest.TestCase):
    """Base test class with common setup and teardown for file-based tests."""

    def setUp(self):
        """Set up test fixtures with temporary file."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_habits_file = pht.HABITS_FILE
        self.test_habits_file = os.path.join(self.temp_dir, "test_habits.json")
        pht.HABITS_FILE = self.test_habits_file

    def tearDown(self):
        """Clean up test fixtures."""
        pht.HABITS_FILE = self.original_habits_file
        # Clean up temp directory
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)