# Personal Habit Tracker

A minimalist command-line habit tracker that puts you in complete control of your personal growth journey. No accounts, no subscriptions, no data harvesting - just you, your habits, and your progress.

## Philosophy

This tool embodies the belief that meaningful change happens through small, consistent daily actions. It's designed for people who want a simple, distraction-free way to build habits without the complexity and privacy concerns of modern apps.

**Built for**: Beginners, minimalists, developers, and privacy-conscious individuals who believe in consistency over complexity.

## Why This Tracker?

- **Privacy First**: Your data stays on your machine - no cloud, no tracking
- **Distraction-Free**: No notifications, social features, or monetization schemes
- **Accessible**: Runs anywhere Python does - no smartphone required
- **Forgiving**: Celebrates progress while being understanding about setbacks
- **Hackable**: Simple Python code you can customize and extend

## Features

### Core Features (Both Interfaces)
- **Interactive Habit Creation**: Set up new habits on first run
- **Daily Check-ins**: Mark habits as completed each day
- **Streak Tracking**: Automatic streak calculation with smart reset logic
- **Progress Monitoring**: View total completions and current streaks
- **Celebration Messages**: Get motivational feedback for maintaining streaks
- **Persistent Storage**: Habits and progress saved locally in JSON format

### GUI-Specific Features
- **Visual Progress Bars**: See your streaks represented graphically
- **Real-time Updates**: Progress updates immediately as you complete habits
- **Celebration Animations**: Animated popups for streak achievements
- **Multiple Daily Completions**: Click "Complete" button multiple times per day
- **Session Tracking**: Shows how many times you've completed each habit today
- **Ongoing Habit Management**: Add/remove habits anytime through "Manage Habits" dialog
- **Keyboard Navigation**: Full keyboard accessibility with shortcuts
- **Mouse Interaction**: Click "Complete" buttons to mark habits done
- **Tooltips**: Hover information for progress indicators
- **Modular Architecture**: Clean separation between main window, dialogs, and reusable widgets

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

#### Option 1: Simple Download
1. Clone or download this repository
2. No additional dependencies required - uses only Python standard library

#### Option 2: Proper Python Package (Optional)
```bash
# Clone the repository
git clone <repository-url>
cd personal-habit-tracker

# Install as a package (optional)
pip install -e .

# Run from anywhere
personal-habit-tracker
```

### Usage

The Personal Habit Tracker offers both CLI and GUI interfaces:

#### Quick Start (Interactive Launcher)

**Cross-platform Python launcher:**
```bash
python habit_tracker.py
```

**Platform-specific launchers:**
```bash
# Windows
habit-tracker.bat

# Unix/Linux/macOS
./habit-tracker.sh
```

All launchers show an interactive menu to choose between CLI and GUI interfaces.

#### Direct Interface Launch
```bash
# CLI interface (default)
python personal_habit_tracker.py

# GUI interface
python personal_habit_tracker.py --gui

# Explicit CLI
python personal_habit_tracker.py --cli

# Alternative GUI launch
python -m gui.gui_habit_tracker
```

#### Interface Comparison

**CLI Interface** (Command Line):
- Text-based interaction
- Works on any system with Python
- Minimal resource usage
- Perfect for terminal users and automation
- **Habit management**: Only during initial setup (first run)

**GUI Interface** (Graphical):
- Visual interface with completion buttons and progress bars
- Mouse and keyboard interaction
- Real-time progress updates with visual streak indicators
- Celebration animations for achievements
- **Multiple completions per day** (same as CLI - click "Complete" multiple times)
- **Habit management**: Add/remove habits anytime via "Manage Habits" button
- Requires tkinter (included with most Python installations)

Both interfaces share the same data file (`habits_data.json`) and are fully compatible.

#### GUI Keyboard Shortcuts
- **Ctrl+M**: Manage habits (add/remove)
- **Ctrl+H**: View progress history
- **F1**: Show help dialog
- **Tab/Shift+Tab**: Navigate between elements
- **Space/Enter**: Complete selected habit
- **Escape**: Close application

*Note: Progress is saved automatically after each completion - no manual save needed.*

#### Interface Behavioral Differences

While both interfaces share the same data and core functionality, there are some workflow differences:

**Habit Management:**
- **CLI**: Habits can only be added during initial setup (first run). To add new habits later, delete `habits_data.json` and restart.
- **GUI**: Habits can be added or removed anytime using the "Manage Habits" button (Ctrl+M).

**Session Management:**
- **CLI**: Session-based - runs once, processes all habits, then exits
- **GUI**: Persistent - stays open for continuous interaction

**Completion Workflow:**
- **CLI**: Linear - asks about each habit once per session (yes/no prompt)
- **GUI**: Interactive - click "Complete" button multiple times per habit

**Progress Viewing:**
- **CLI**: Shows progress summary at the end of each session
- **GUI**: Real-time progress display + separate "View History" dialog

**Data Persistence:**
- **CLI**: Saves once at the end of the session
- **GUI**: Auto-saves after each habit completion

**Celebrations:**
- **CLI**: Text-based celebration messages in console
- **GUI**: Animated popup windows for achievements

**Error Handling:**
- **CLI**: Text-based error messages, exits on critical errors
- **GUI**: Dialog boxes for errors, graceful fallback options

**Data Compatibility:**
- Both interfaces read and write the same `habits_data.json` format
- You can switch between CLI and GUI at any time without data loss
- All habit data (totals, streaks, dates) is preserved across interfaces

#### First Time Setup

When you run the app for the first time, you'll be prompted to create your habits:

```
No existing habits found. Let's create some!
Enter a habit to track (or type 'done' when finished): yoga
Enter a habit to track (or type 'done' when finished): running
Enter a habit to track (or type 'done' when finished): done
```

#### Daily Check-ins

Each time you run the app, you'll be asked about each habit:

```
Did you complete 'yoga' today? yes/no: yes
Great job! Keep up the streak! 🔥
Did you complete 'running' today? yes/no: no
No worries! Tomorrow is another chance! 🌤️
```

#### Progress Summary

After each session, view your progress:

```
📅 Your Habit Progress:
Yoga: 5 times total, 3 day streak
🔥 Great! 3 day streak for yoga!
Running: 2 times total, 0 day streak
```

## How Streaks Work

- **New Streak**: Starts at 1 when you complete a habit
- **Continuing Streak**: Increases by 1 if you completed the habit yesterday
- **Broken Streak**: Resets to 0 if you miss more than one day
- **Same Day**: Multiple completions on the same day don't increase the streak

## Streak Celebrations

- 🔥 **3+ days**: "Great! X day streak!"
- 🏆 **7+ days**: "Amazing! X week(s) streak!"

## Testing

The project includes a comprehensive test suite to ensure reliability and maintainability.

### Running Tests

Run all tests:
```bash
python -m unittest tests.test_unit tests.test_integration tests.test_gui -v
```

Run only unit tests:
```bash
python -m unittest tests.test_unit -v
```

Run only integration tests:
```bash
python -m unittest tests.test_integration -v
```

Run only GUI tests:
```bash
python -m unittest tests.test_gui -v
```

Run tests with discovery (alternative):
```bash
python -m unittest discover tests -v
```

### Test Coverage

- **Unit Tests** (33 tests): Core function testing including habit creation, streak calculation, data persistence, celebration messages, and error handling
- **Integration Tests** (19 tests): End-to-end workflow testing including first-time setup, daily check-ins, multi-session persistence, and error recovery
- **GUI Tests** (21 tests): GUI component testing including initialization, event handling, backend integration, accessibility, and error handling

All tests use only Python standard library (unittest, mock) and maintain the project's philosophy of simplicity and privacy.

### Test Structure

The test suite uses a shared base class (`tests/test_base.py`) to eliminate code duplication:
- `BaseHabitTrackerTest`: Common setup/teardown for file-based tests
- Maintains DRY principles while keeping tests maintainable
- All test classes inherit from this base for consistent temporary file handling

### Git Hooks & Quality Assurance

The project includes simple Git hooks to maintain code quality without external dependencies:

#### Pre-push Hook
A Git pre-push hook automatically runs tests before allowing pushes:
- Located at `.git/hooks/pre-push`
- Prevents pushing if tests fail
- Uses only standard Git functionality and Python

#### Manual Test & Push
For manual control, use the provided batch script:
```bash
test-and-push
```

This script runs tests and only pushes if all tests pass, giving you explicit control over the process.

## Development Status

This project follows a spec-driven development approach with Python best practices. Current implementation status:

✅ **Core Features Complete**
- Data persistence layer with JSON storage
- Streak calculation engine with smart logic
- User interaction and feedback system (CLI)
- Progress display and reporting
- Main application workflow
- **GUI Interface with tkinter** (✅ **NEW**)
  - Visual habit tracking with checkboxes
  - Real-time progress bars and streak indicators
  - Celebration animations for achievements
  - Habit management dialogs
  - Keyboard navigation and accessibility
  - Error handling and robustness
  - Comprehensive GUI test suite
- Comprehensive docstrings and type hints
- Modern Python packaging (`pyproject.toml`)
- Proper project metadata and licensing
- Code structure optimization and refactoring
- Error handling and robustness improvements
- Comprehensive test suite (unit, integration, and GUI tests)

📋 **Planned Enhancements** (Philosophy-Compliant)
- Data export capabilities (CSV, plain text for user control)
- Habit categories and tags (simple, local organization)
- Configurable streak reset policies (user choice, local settings)
- Enhanced celebration messages and progress views

## File Structure

```
personal-habit-tracker/
├── .kiro/                          # Kiro IDE configuration
│   ├── specs/personal-habit-tracker-core/   # Development specifications
│   │   ├── requirements.md         # Feature requirements (philosophy-aligned)
│   │   ├── design.md              # System design (philosophy-aligned)
│   │   └── tasks.md               # Implementation tasks (philosophy-aligned)
│   ├── steering/                   # Automatic governance rules
│   │   └── philosophy-alignment.md # Philosophy compliance enforcement
│   ├── templates/                  # Development templates
│   │   └── spec-philosophy-check.md # Philosophy review checklist
│   ├── hooks/                      # Automated workflows
│   │   └── philosophy-review.md    # Philosophy alignment verification
│   └── docs/                       # Internal development docs (gitignored)
├── tests/                          # Test suite
│   ├── __init__.py                # Test package initialization
│   ├── test_unit.py               # Unit tests for core functions (33 tests)
│   ├── test_integration.py        # Integration tests for workflows (19 tests)
│   └── test_gui.py                # GUI test suite (21 tests)
├── gui/                            # GUI application package
│   ├── __init__.py                # GUI package initialization
│   ├── gui_habit_tracker.py       # Main GUI entry point and error handling
│   ├── main_window.py             # Primary application window and core functionality
│   ├── widgets.py                 # Reusable UI components
│   ├── dialogs.py                 # Modal dialog windows (habit management, history)
│   └── gui_design_wireframes.md   # GUI design specifications
├── personal_habit_tracker.py      # Main CLI application
├── habit_tracker.py               # Interactive launcher
├── habit-tracker.bat              # Windows launcher script
├── habit-tracker.sh               # Unix/Linux/macOS launcher script
├── habits_data.json               # Your habit data (auto-created, gitignored)
├── philosophy.md                  # Project vision and philosophy (📍 North Star)
├── pyproject.toml                 # Modern Python packaging configuration
├── requirements.txt               # Dependencies (documents zero dependencies)
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history and release notes
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Data Storage

Your habits are stored in `habits_data.json` with the following structure. This file is automatically created on first run and is gitignored to keep your personal data private:

```json
[
  {
    "habit": "yoga",
    "total_completed": 2,
    "current_streak": 2,
    "last_completed": "2025-09-24"
  }
]
```

## Philosophy-Driven Development

This project maintains strict alignment with its core philosophy through automated governance:

### Philosophy Enforcement
- **Steering Rules**: Automatic philosophy compliance checking for all spec changes
- **Red Flag System**: Immediate rejection of features that violate core principles
- **Template-Based Reviews**: Systematic verification against philosophy.md
- **File References**: Direct links between specs and philosophy for traceability

### Development Workflow
This project uses [spec-kit](https://github.com/github/spec-kit) for structured development:

1. **Philosophy** → **Requirements** → **Design** → **Implementation Tasks**
2. All decisions filtered through philosophy alignment checklist
3. View the complete development plan in `.kiro/specs/personal-habit-tracker-core/`
4. Track progress through the task checklist in `tasks.md`

### Governance Structure
```
philosophy.md (North Star)
    ↓
.kiro/steering/philosophy-alignment.md (Enforcement)
    ↓
.kiro/specs/ (Technical Implementation)
    ↓
habit_tracker.py (Code)
```

## Philosophy Compliance

All development follows strict philosophy alignment:

### ✅ **Maintained Principles**
- **Privacy**: Local-only data storage, no cloud services
- **Simplicity**: Python standard library only, minimal complexity
- **Control**: User owns all data and code
- **Accessibility**: Runs anywhere Python does
- **Encouragement**: Celebrates progress, forgives setbacks

### 🚫 **Rejected Features** (Red Flags)
- Social features or sharing capabilities
- Cloud storage or external services
- Complex UI frameworks or heavy dependencies
- Monetization schemes or subscription models
- Data analytics or user tracking
- Notifications or interruption-based features

## Next Steps

To continue development, check the remaining tasks in `.kiro/specs/personal-habit-tracker-core/tasks.md`.

- **Future Features**: data export, habit organization (all philosophy-compliant)

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

### Contribution Guidelines
1. **Philosophy First**: All contributions must align with `philosophy.md`
2. **Use the Template**: Apply `.kiro/templates/spec-philosophy-check.md` for new features
3. **Respect Red Flags**: Avoid features listed in the rejection criteria
4. **Maintain Simplicity**: Keep the codebase minimal and hackable
5. **Preserve Privacy**: Ensure all data remains local and under user control

When in doubt, ask: *"Does this make habit formation simpler, more private, and more under the user's control?"*

## License

This project is open source and available under the MIT License.