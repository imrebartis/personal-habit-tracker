"""
Integration tests for Personal Habit Tracker workflows.

Tests cover:
- Complete application runs with mock input
- First-time setup workflow
- Daily check-in workflow with various completion patterns
- Data persistence across multiple sessions
- Error recovery scenarios

Philosophy compliance: Tests maintain privacy (local only), simplicity (standard library),
and focus on end-to-end functionality without external dependencies.
"""

import unittest
import datetime
import json
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import the module under test
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import personal_habit_tracker as pht
from tests.test_base import BaseHabitTrackerTest


class TestFirstTimeSetupWorkflow(BaseHabitTrackerTest):
    """Test first-time setup workflow integration."""

    @patch('builtins.input')
    def test_setup_new_habits_workflow(self, mock_input):
        """Test complete first-time setup workflow."""
        # Mock user input for creating habits
        mock_input.side_effect = ['Exercise', 'Read Books', 'Meditate', 'done']

        habits = pht.setup_new_habits()

        # Verify habits were created correctly
        self.assertEqual(len(habits), 3)
        self.assertEqual(habits[0]['habit'], 'Exercise')
        self.assertEqual(habits[1]['habit'], 'Read Books')
        self.assertEqual(habits[2]['habit'], 'Meditate')

        # Verify all habits are initialized properly
        for habit in habits:
            self.assertEqual(habit['total_completed'], 0)
            self.assertEqual(habit['current_streak'], 0)
            self.assertIsNone(habit['last_completed'])

    @patch('builtins.input')
    def test_setup_with_empty_names_and_duplicates(self, mock_input):
        """Test setup workflow handles empty names and duplicates."""
        mock_input.side_effect = [
            '',  # Empty name - should be ignored
            'Exercise',  # Valid name
            '   ',  # Whitespace only - should be ignored
            'exercise',  # Duplicate (case insensitive) - should be rejected
            'Reading',  # Valid name
            'done'
        ]

        with patch('builtins.print') as mock_print:
            habits = pht.setup_new_habits()

        # Should only have 2 valid, unique habits
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0]['habit'], 'Exercise')
        self.assertEqual(habits[1]['habit'], 'Reading')

        # Verify appropriate warnings were printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertTrue(any('cannot be empty' in call for call in print_calls))
        self.assertTrue(any('already have a habit' in call for call in print_calls))

    @patch('builtins.input')
    @patch('sys.exit')
    def test_setup_no_habits_created_exits(self, mock_exit, mock_input):
        """Test that setup exits if no habits are created."""
        mock_input.side_effect = ['done']  # User immediately says done

        pht.setup_new_habits()

        # Should call sys.exit(0) when no habits created
        mock_exit.assert_called_with(0)

    @patch('builtins.input', side_effect=EOFError())
    @patch('sys.exit')
    def test_setup_handles_keyboard_interrupt(self, mock_exit, mock_input):
        """Test that setup handles user interruption gracefully."""
        with patch('builtins.print'):  # Suppress print output
            pht.setup_new_habits()

        # Should call sys.exit(0) on interruption
        mock_exit.assert_called_with(0)


class TestDailyCheckInWorkflow(BaseHabitTrackerTest):
    """Test daily check-in workflow integration."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        # Create test habits
        self.test_habits = [
            pht.create_habit("Exercise"),
            pht.create_habit("Reading"),
            pht.create_habit("Meditation")
        ]

    @patch('builtins.input')
    def test_daily_checkin_all_completed(self, mock_input):
        """Test daily check-in when all habits are completed."""
        mock_input.side_effect = ['yes', 'y', '1']  # All habits completed

        with patch('builtins.print') as mock_print:
            performed_habits = pht.process_daily_habits(self.test_habits)

        # Verify all habits were marked as performed
        self.assertEqual(len(performed_habits), 3)
        self.assertIn('Exercise', performed_habits)
        self.assertIn('Reading', performed_habits)
        self.assertIn('Meditation', performed_habits)

        # Verify habits were updated correctly
        for habit in self.test_habits:
            self.assertEqual(habit['total_completed'], 1)
            self.assertEqual(habit['current_streak'], 1)
            self.assertEqual(habit['last_completed'], datetime.date.today())

    @patch('builtins.input')
    def test_daily_checkin_mixed_completion(self, mock_input):
        """Test daily check-in with mixed completion patterns."""
        mock_input.side_effect = ['yes', 'no', 'yes']  # Exercise: yes, Reading: no, Meditation: yes

        performed_habits = pht.process_daily_habits(self.test_habits)

        # Verify correct habits were marked as performed
        self.assertEqual(len(performed_habits), 2)
        self.assertIn('Exercise', performed_habits)
        self.assertNotIn('Reading', performed_habits)
        self.assertIn('Meditation', performed_habits)

        # Verify habit states
        self.assertEqual(self.test_habits[0]['total_completed'], 1)  # Exercise
        self.assertEqual(self.test_habits[1]['total_completed'], 0)  # Reading
        self.assertEqual(self.test_habits[2]['total_completed'], 1)  # Meditation

    @patch('builtins.input')
    def test_daily_checkin_none_completed(self, mock_input):
        """Test daily check-in when no habits are completed."""
        mock_input.side_effect = ['no', 'n', '0']  # All habits not completed

        performed_habits = pht.process_daily_habits(self.test_habits)

        # Verify no habits were performed
        self.assertEqual(len(performed_habits), 0)

        # Verify habits remain unchanged
        for habit in self.test_habits:
            self.assertEqual(habit['total_completed'], 0)
            self.assertEqual(habit['current_streak'], 0)
            self.assertIsNone(habit['last_completed'])

    @patch('builtins.input')
    def test_daily_checkin_invalid_input_handling(self, mock_input):
        """Test daily check-in handles invalid input gracefully."""
        # First habit: invalid inputs then yes, second habit: yes, third habit: invalid then no
        mock_input.side_effect = ['maybe', 'invalid', 'yes', 'yes', 'xyz', 'no']

        with patch('builtins.print') as mock_print:
            performed_habits = pht.process_daily_habits(self.test_habits)

        # Should still process correctly after handling invalid input
        self.assertEqual(len(performed_habits), 2)
        self.assertIn('Exercise', performed_habits)
        self.assertIn('Reading', performed_habits)
        self.assertNotIn('Meditation', performed_habits)


class TestDataPersistenceAcrossSessions(BaseHabitTrackerTest):
    """Test data persistence across multiple application sessions."""

    @patch('builtins.input')
    def test_multi_session_persistence(self, mock_input):
        """Test that data persists correctly across multiple sessions."""
        # Session 1: Create habits and complete some
        mock_input.side_effect = ['Exercise', 'Reading', 'done']
        habits_session1 = pht.setup_new_habits()

        # Complete first habit
        habits_session1[0]['total_completed'] = 1
        habits_session1[0]['current_streak'] = 1
        habits_session1[0]['last_completed'] = datetime.date(2024, 1, 15)

        # Save session 1 data
        pht.save_habits(habits_session1)

        # Session 2: Load data and verify persistence
        habits_session2 = pht.load_habits()

        self.assertEqual(len(habits_session2), 2)
        self.assertEqual(habits_session2[0]['habit'], 'Exercise')
        self.assertEqual(habits_session2[0]['total_completed'], 1)
        self.assertEqual(habits_session2[0]['current_streak'], 1)
        self.assertEqual(habits_session2[0]['last_completed'], datetime.date(2024, 1, 15))

        self.assertEqual(habits_session2[1]['habit'], 'Reading')
        self.assertEqual(habits_session2[1]['total_completed'], 0)
        self.assertEqual(habits_session2[1]['current_streak'], 0)
        self.assertIsNone(habits_session2[1]['last_completed'])

    def test_streak_calculation_across_sessions(self):
        """Test that streak calculations work correctly across sessions."""
        # Create initial habits
        habits = [pht.create_habit("Exercise")]

        # Day 1: Complete habit
        day1 = datetime.date(2024, 1, 15)
        habits[0]['total_completed'] += 1  # Manually increment for test
        pht.update_habit_streak(habits[0], day1)
        pht.save_habits(habits)

        # Day 2: Load and complete again (consecutive)
        habits = pht.load_habits()
        day2 = datetime.date(2024, 1, 16)
        habits[0]['total_completed'] += 1  # Manually increment for test
        pht.update_habit_streak(habits[0], day2)
        self.assertEqual(habits[0]['current_streak'], 2)
        pht.save_habits(habits)

        # Day 4: Load and complete after missing day 3 (streak should reset)
        habits = pht.load_habits()
        day4 = datetime.date(2024, 1, 18)
        habits[0]['total_completed'] += 1  # Manually increment for test
        pht.update_habit_streak(habits[0], day4)
        self.assertEqual(habits[0]['current_streak'], 1)  # Reset to 1
        self.assertEqual(habits[0]['total_completed'], 3)  # But total still increases

    def test_data_corruption_recovery(self):
        """Test recovery from corrupted data files."""
        # Create valid habits first
        habits = [pht.create_habit("Exercise")]
        pht.save_habits(habits)

        # Corrupt the file
        with open(self.test_habits_file, 'w') as f:
            f.write('{"corrupted": json')

        # Loading should return empty list and not crash
        loaded_habits = pht.load_habits()
        self.assertEqual(loaded_habits, [])


class TestCompleteApplicationRuns(BaseHabitTrackerTest):
    """Test complete application runs with various scenarios."""

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_first_run_workflow(self, mock_stdout, mock_input):
        """Test complete application run for first-time user."""
        # Mock input: create habits, then complete some
        mock_input.side_effect = [
            'Exercise', 'Reading', 'done',  # Setup habits
            'yes', 'no'  # Complete Exercise, skip Reading
        ]

        # Run main application
        pht.launch_cli()

        # Verify habits were created and saved
        habits = pht.load_habits()
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0]['habit'], 'Exercise')
        self.assertEqual(habits[0]['total_completed'], 1)
        self.assertEqual(habits[1]['habit'], 'Reading')
        self.assertEqual(habits[1]['total_completed'], 0)

        # Verify output contains expected messages
        output = mock_stdout.getvalue()
        self.assertIn('Welcome to your Personal Habit Tracker!', output)
        self.assertIn('Exercise: 1 times total', output)
        self.assertIn('Reading: 0 times total', output)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_returning_user_workflow(self, mock_stdout, mock_input):
        """Test complete application run for returning user."""
        # Pre-create habits with some history
        existing_habits = [
            {
                'habit': 'Exercise',
                'total_completed': 5,
                'current_streak': 2,
                'last_completed': datetime.date.today() - datetime.timedelta(days=1)
            },
            {
                'habit': 'Reading',
                'total_completed': 3,
                'current_streak': 0,
                'last_completed': datetime.date.today() - datetime.timedelta(days=3)
            }
        ]
        pht.save_habits(existing_habits)

        # Mock input for daily check-in
        mock_input.side_effect = ['yes', 'yes']  # Complete both habits

        # Run main application
        pht.launch_cli()

        # Verify habits were updated correctly
        habits = pht.load_habits()
        self.assertEqual(habits[0]['total_completed'], 6)  # Exercise: 5 + 1
        self.assertEqual(habits[0]['current_streak'], 3)   # Exercise: 2 + 1 (consecutive)
        self.assertEqual(habits[1]['total_completed'], 4)  # Reading: 3 + 1
        self.assertEqual(habits[1]['current_streak'], 1)   # Reading: reset to 1 (gap)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_celebration_messages_in_workflow(self, mock_stdout, mock_input):
        """Test that celebration messages appear in complete workflow."""
        # Pre-create habit with streak just below celebration threshold
        existing_habits = [
            {
                'habit': 'Exercise',
                'total_completed': 6,
                'current_streak': 6,  # Will become 7 (Amazing threshold)
                'last_completed': datetime.date.today() - datetime.timedelta(days=1)
            }
        ]
        pht.save_habits(existing_habits)

        # Mock input to complete the habit
        mock_input.side_effect = ['yes']

        # Run main application
        pht.launch_cli()

        # Verify celebration message appears in output
        output = mock_stdout.getvalue()
        self.assertIn('Amazing!', output)
        self.assertIn('1 week streak', output)

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('sys.exit')
    def test_keyboard_interrupt_handling(self, mock_exit, mock_input):
        """Test that keyboard interrupt is handled gracefully."""
        with patch('builtins.print'):  # Suppress print output
            pht.launch_cli()

        # Should call sys.exit (either 0 for KeyboardInterrupt or 1 for other errors)
        mock_exit.assert_called()


class TestErrorRecoveryScenarios(BaseHabitTrackerTest):
    """Test error recovery scenarios in workflows."""

    @patch('builtins.input')
    def test_recovery_from_corrupted_data_during_workflow(self, mock_input):
        """Test recovery when data file becomes corrupted during workflow."""
        # Create corrupted data file
        with open(self.test_habits_file, 'w') as f:
            f.write('{"invalid": json content')

        # Mock input for creating new habits (should trigger setup)
        mock_input.side_effect = ['Exercise', 'done', 'yes']

        with patch('builtins.print') as mock_print:
            # Should not crash, should start fresh setup
            pht.launch_cli()

        # Verify new habits were created despite corruption
        habits = pht.load_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]['habit'], 'Exercise')

    def test_display_functions_with_invalid_data(self):
        """Test that display functions handle invalid data gracefully."""
        # Test with various invalid data types
        invalid_data_sets = [
            None,
            "not a list",
            [{"invalid": "habit"}, "not a dict"],
            [{"habit": 123, "total_completed": "not int"}]
        ]

        for invalid_data in invalid_data_sets:
            with patch('builtins.print') as mock_print:
                # Should not crash, should handle gracefully
                pht.display_progress_summary(invalid_data)
                pht.display_daily_summary(invalid_data)

        # Verify error messages were printed (not crashing is the main test)
        self.assertTrue(True)  # If we get here, no crashes occurred

    @patch('builtins.input')
    def test_process_habits_with_malformed_data(self, mock_input):
        """Test processing habits when data becomes malformed during execution."""
        # Create habits with some malformed entries
        malformed_habits = [
            pht.create_habit("Valid Habit"),
            {"invalid": "habit structure"},
            None,
            pht.create_habit("Another Valid Habit")
        ]

        mock_input.side_effect = ['yes', 'yes']  # Try to complete valid habits

        with patch('builtins.print') as mock_print:
            performed_habits = pht.process_daily_habits(malformed_habits)

        # Should process valid habits and skip invalid ones
        self.assertEqual(len(performed_habits), 2)
        self.assertIn('Valid Habit', performed_habits)
        self.assertIn('Another Valid Habit', performed_habits)

    @patch('personal_habit_tracker.datetime')
    def test_date_system_error_handling(self, mock_datetime):
        """Test handling of system date errors."""
        # Mock datetime.date.today() to raise an exception
        mock_datetime.date.today.side_effect = Exception("System date error")

        habits = [pht.create_habit("Exercise")]

        with patch('builtins.print') as mock_print:
            performed_habits = pht.process_daily_habits(habits)

        # Should handle gracefully and return empty list
        self.assertEqual(performed_habits, [])


if __name__ == '__main__':
    # Run all integration tests
    unittest.main(verbosity=2)
