"""
Comprehensive test suite for GUI habit tracker.

Tests GUI component initialization, event handling, backend integration,
accessibility features, and error handling scenarios.
"""

import unittest
import tkinter as tk
from tkinter import ttk
import datetime
import tempfile
import os
import json
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the GUI application components
from gui.main_window import HabitTrackerGUI
from gui.dialogs import HabitManagementDialog, ProgressHistoryDialog
from personal_habit_tracker import create_habit, HABITS_FILE


class TestGUIInitialization(unittest.TestCase):
    """Test GUI component initialization and layout."""

    def setUp(self):
        """Set up test environment."""
        self.test_habits = [
            create_habit("Test Habit 1"),
            create_habit("Test Habit 2")
        ]

    def tearDown(self):
        """Clean up after tests."""
        # Clean up any test files
        if os.path.exists(HABITS_FILE):
            try:
                os.remove(HABITS_FILE)
            except:
                pass

    def test_gui_initialization(self):
        """Test basic GUI initialization."""
        try:
            # Mock the load_habits to return test data
            with patch('gui.main_window.load_habits', return_value=self.test_habits):
                app = HabitTrackerGUI()

                # Test window properties
                self.assertIsInstance(app.root, tk.Tk)
                self.assertEqual(app.root.title(), "Personal Habit Tracker")
                self.assertFalse(app.is_closing)

                # Test data initialization
                self.assertEqual(len(app.habits), 2)
                self.assertIsInstance(app.habit_buttons, dict)
                self.assertIsInstance(app.today_completions, dict)

                # Clean up
                app.root.destroy()

        except Exception as e:
            self.fail(f"GUI initialization failed: {e}")

    def test_window_configuration(self):
        """Test window configuration and styling."""
        with patch('gui.main_window.load_habits', return_value=[]):
            app = HabitTrackerGUI()

            # Test window properties
            self.assertTrue(app.root.winfo_width() >= 500)
            self.assertTrue(app.root.winfo_height() >= 400)

            # Test background color
            self.assertEqual(app.root.cget('bg'), '#F5F5F5')

            # Clean up
            app.root.destroy()

    def test_widget_creation(self):
        """Test that all required widgets are created."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits):
            app = HabitTrackerGUI()

            # Test main frame exists
            main_frames = [w for w in app.root.winfo_children() if isinstance(w, ttk.Frame)]
            self.assertTrue(len(main_frames) > 0)

            # Test status variable exists
            self.assertIsInstance(app.status_var, tk.StringVar)

            # Clean up
            app.root.destroy()


class TestGUIEventHandling(unittest.TestCase):
    """Test GUI event handling and user interactions."""

    def setUp(self):
        """Set up test environment."""
        self.test_habits = [
            {
                'habit': 'Test Habit',
                'total_completed': 5,
                'current_streak': 2,
                'last_completed': datetime.date.today() - datetime.timedelta(days=1)
            }
        ]

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(HABITS_FILE):
            try:
                os.remove(HABITS_FILE)
            except:
                pass

    def test_habit_toggle_completion(self):
        """Test habit completion button functionality."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits.copy()):
            with patch('gui.main_window.save_habits') as mock_save:
                app = HabitTrackerGUI()

                # Simulate habit completion (button click)
                app.on_habit_complete(0)

                # Check that habit was updated
                habit = app.habits[0]
                self.assertEqual(habit['total_completed'], 6)
                self.assertEqual(habit['current_streak'], 3)
                self.assertEqual(habit['last_completed'], datetime.date.today())

                # Check that save was called
                mock_save.assert_called()

                # Clean up
                app.root.destroy()

    def test_multiple_completions_per_day(self):
        """Test multiple completions of the same habit in one day (matches CLI behavior)."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits.copy()):
            with patch('gui.main_window.save_habits') as mock_save:
                app = HabitTrackerGUI()

                # Complete the same habit multiple times
                app.on_habit_complete(0)  # First completion
                app.on_habit_complete(0)  # Second completion
                app.on_habit_complete(0)  # Third completion

                # Check that habit was incremented each time
                habit = app.habits[0]
                self.assertEqual(habit['total_completed'], 8)  # 5 + 3 completions
                self.assertEqual(habit['current_streak'], 3)  # Streak should be 3 (yesterday + today)
                self.assertEqual(habit['last_completed'], datetime.date.today())

                # Check today's completion count
                self.assertEqual(app.get_today_completions(habit), 3)

                # Check that save was called
                mock_save.assert_called()

                # Clean up
                app.root.destroy()

    def test_auto_save_functionality(self):
        """Test automatic save functionality during habit completion."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits.copy()):
            with patch('gui.main_window.save_habits') as mock_save:
                app = HabitTrackerGUI()

                # Complete a habit (should trigger auto-save)
                app.on_habit_complete(0)

                # Check that save was called automatically
                mock_save.assert_called()

                # Clean up
                app.root.destroy()


class TestGUIBackendIntegration(unittest.TestCase):
    """Test GUI integration with existing backend functions."""

    def setUp(self):
        """Set up test environment."""
        self.test_habits = [
            create_habit("Integration Test Habit")
        ]

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(HABITS_FILE):
            try:
                os.remove(HABITS_FILE)
            except:
                pass

    def test_data_format_compatibility(self):
        """Test that GUI maintains CLI data format compatibility."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits):
            app = HabitTrackerGUI()

            # Verify data format
            for habit in app.habits:
                self.assertIn('habit', habit)
                self.assertIn('total_completed', habit)
                self.assertIn('current_streak', habit)
                self.assertIn('last_completed', habit)

                # Check data types
                self.assertIsInstance(habit['habit'], str)
                self.assertIsInstance(habit['total_completed'], int)
                self.assertIsInstance(habit['current_streak'], int)

            # Clean up
            app.root.destroy()

    def test_cli_compatibility_enforcement(self):
        """Test CLI compatibility enforcement."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits):
            app = HabitTrackerGUI()

            # Test ensure_cli_compatibility
            app.ensure_cli_compatibility()

            # Verify all habits have required fields
            for habit in app.habits:
                self.assertTrue(habit['total_completed'] >= 0)
                self.assertTrue(habit['current_streak'] >= 0)
                self.assertTrue(len(habit['habit']) > 0)

            # Clean up
            app.root.destroy()

    def test_celebration_message_integration(self):
        """Test integration with celebration message system."""
        # Create habit with good streak (6 days, will become 7 after toggle)
        streak_habit = create_habit("Streak Test")
        streak_habit['current_streak'] = 6
        streak_habit['last_completed'] = datetime.date.today() - datetime.timedelta(days=1)

        with patch('gui.main_window.load_habits', return_value=[streak_habit]):
            app = HabitTrackerGUI()

            # Test celebration popup (mock it to avoid actual popup)
            with patch.object(app, 'show_celebration_popup') as mock_popup:
                # Complete habit to trigger celebration
                app.on_habit_complete(0)

                # Should trigger celebration for 7-day streak (amazing threshold)
                mock_popup.assert_called()

            # Clean up
            app.root.destroy()


class TestHabitManagementDialog(unittest.TestCase):
    """Test habit management dialog functionality."""

    def setUp(self):
        """Set up test environment."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide test window
        self.test_habits = [create_habit("Existing Habit")]
        self.callback_called = False

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def callback_mock(self):
        """Mock callback function."""
        self.callback_called = True

    def test_dialog_initialization(self):
        """Test habit management dialog initialization."""
        dialog = HabitManagementDialog(self.root, self.test_habits, self.callback_mock)

        # Test dialog properties
        self.assertIsInstance(dialog.dialog, tk.Toplevel)
        self.assertEqual(dialog.habits, self.test_habits)

        # Clean up
        dialog.dialog.destroy()

    def test_habit_name_validation(self):
        """Test habit name validation."""
        dialog = HabitManagementDialog(self.root, self.test_habits, self.callback_mock)

        # Test valid names
        self.assertIsNone(dialog.validate_habit_name("Valid Habit"))
        self.assertIsNone(dialog.validate_habit_name("Exercise 30min"))

        # Test invalid names
        self.assertIsNotNone(dialog.validate_habit_name(""))  # Empty
        self.assertIsNotNone(dialog.validate_habit_name("A"))  # Too short
        self.assertIsNotNone(dialog.validate_habit_name("A" * 101))  # Too long
        self.assertIsNotNone(dialog.validate_habit_name("Test<>"))  # Invalid chars
        self.assertIsNotNone(dialog.validate_habit_name("   "))  # Only whitespace

        # Clean up
        dialog.dialog.destroy()

    def test_add_habit_functionality(self):
        """Test adding new habits."""
        dialog = HabitManagementDialog(self.root, self.test_habits, self.callback_mock)

        # Set up new habit name
        dialog.new_habit_var.set("New Test Habit")

        # Add habit
        dialog.add_habit()

        # Check that habit was added
        self.assertEqual(len(self.test_habits), 2)
        self.assertEqual(self.test_habits[1]['habit'], "New Test Habit")
        self.assertTrue(self.callback_called)

        # Clean up
        dialog.dialog.destroy()

    def test_duplicate_habit_prevention(self):
        """Test prevention of duplicate habits."""
        dialog = HabitManagementDialog(self.root, self.test_habits, self.callback_mock)

        # Try to add duplicate
        dialog.new_habit_var.set("Existing Habit")

        with patch('tkinter.messagebox.showwarning') as mock_warning:
            dialog.add_habit()

            # Should show warning and not add habit
            mock_warning.assert_called()
            self.assertEqual(len(self.test_habits), 1)

        # Clean up
        dialog.dialog.destroy()


class TestProgressHistoryDialog(unittest.TestCase):
    """Test progress history dialog functionality."""

    def setUp(self):
        """Set up test environment."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide test window
        self.test_habits = [
            {
                'habit': 'Test Habit 1',
                'total_completed': 15,
                'current_streak': 5,
                'last_completed': datetime.date.today()
            },
            {
                'habit': 'Test Habit 2',
                'total_completed': 8,
                'current_streak': 0,
                'last_completed': None
            }
        ]

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_dialog_initialization(self):
        """Test progress history dialog initialization."""
        dialog = ProgressHistoryDialog(self.root, self.test_habits)

        # Test dialog properties
        self.assertIsInstance(dialog.dialog, tk.Toplevel)
        self.assertEqual(dialog.habits, self.test_habits)

        # Clean up
        dialog.dialog.destroy()

    def test_progress_display(self):
        """Test progress display functionality."""
        dialog = ProgressHistoryDialog(self.root, self.test_habits)

        # Test that progress rows are created
        # This is a basic test since we can't easily inspect the visual elements
        self.assertIsNotNone(dialog.dialog)

        # Clean up
        dialog.dialog.destroy()


class TestGUIAccessibility(unittest.TestCase):
    """Test GUI accessibility features."""

    def setUp(self):
        """Set up test environment."""
        self.test_habits = [create_habit("Accessibility Test")]

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(HABITS_FILE):
            try:
                os.remove(HABITS_FILE)
            except:
                pass

    def test_keyboard_navigation_setup(self):
        """Test keyboard navigation setup."""
        with patch('gui.main_window.load_habits', return_value=self.test_habits):
            app = HabitTrackerGUI()

            # Test that focusable widgets list exists
            self.assertIsInstance(app.focusable_widgets, list)

            # Test keyboard bindings exist
            bindings = app.root.bind()
            self.assertIn('<Control-Key-m>', bindings)
            self.assertIn('<Control-Key-h>', bindings)
            self.assertIn('<Key-F1>', bindings)

            # Clean up
            app.root.destroy()

    def test_help_functionality(self):
        """Test help dialog functionality."""
        with patch('gui.main_window.load_habits', return_value=[]):
            app = HabitTrackerGUI()

            # Test help dialog (mock messagebox to avoid actual popup)
            with patch('tkinter.messagebox.showinfo') as mock_info:
                app.show_help()
                mock_info.assert_called()

            # Clean up
            app.root.destroy()


class TestGUIErrorHandling(unittest.TestCase):
    """Test GUI error handling and edge cases."""

    def setUp(self):
        """Set up test environment."""
        pass

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(HABITS_FILE):
            try:
                os.remove(HABITS_FILE)
            except:
                pass

    def test_load_data_error_handling(self):
        """Test error handling during data loading."""
        # Mock load_habits to raise an exception
        with patch('gui.main_window.load_habits', side_effect=Exception("Test error")):
            with patch('tkinter.messagebox.showerror') as mock_error:
                app = HabitTrackerGUI()

                # Should handle error gracefully
                mock_error.assert_called()

                # Clean up
                app.root.destroy()

    def test_save_error_handling(self):
        """Test error handling during save operations."""
        with patch('gui.main_window.load_habits', return_value=[]):
            app = HabitTrackerGUI()

            # Mock save_habits to raise an exception
            with patch('gui.main_window.save_habits', side_effect=Exception("Save error")):
                with patch('tkinter.messagebox.showerror') as mock_error:
                    app.save_progress()

                    # Should handle error gracefully
                    mock_error.assert_called()

            # Clean up
            app.root.destroy()

    def test_habit_completion_error_handling(self):
        """Test error handling during habit completion."""
        test_habit = create_habit("Error Test")

        with patch('gui.main_window.load_habits', return_value=[test_habit]):
            app = HabitTrackerGUI()

            # Mock update_habit_streak to raise an exception
            with patch('gui.main_window.update_habit_streak', side_effect=Exception("Update error")):
                with patch('tkinter.messagebox.showerror') as mock_error:
                    app.on_habit_complete(0)

                    # Should handle error gracefully
                    mock_error.assert_called()

            # Clean up
            app.root.destroy()

    def test_window_closing_error_handling(self):
        """Test error handling during window closing."""
        with patch('gui.main_window.load_habits', return_value=[]):
            app = HabitTrackerGUI()

            # Mock save_habits to raise an exception
            with patch('gui.main_window.save_habits', side_effect=Exception("Close error")):
                with patch('tkinter.messagebox.askyesnocancel', return_value=True) as mock_dialog:
                    app.on_closing()

                    # Should show error dialog
                    mock_dialog.assert_called()

            # Note: Don't clean up here as on_closing destroys the window


def run_gui_tests():
    """Run all GUI tests."""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestGUIInitialization,
        TestGUIEventHandling,
        TestGUIBackendIntegration,
        TestHabitManagementDialog,
        TestProgressHistoryDialog,
        TestGUIAccessibility,
        TestGUIErrorHandling
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    # Check if tkinter is available before running tests
    try:
        import tkinter
        success = run_gui_tests()
        sys.exit(0 if success else 1)
    except ImportError:
        print("❌ Skipping GUI tests: tkinter not available")
        sys.exit(0)
