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

- **Interactive Habit Creation**: Set up new habits on first run
- **Daily Check-ins**: Mark habits as completed each day
- **Streak Tracking**: Automatic streak calculation with smart reset logic
- **Progress Monitoring**: View total completions and current streaks
- **Celebration Messages**: Get motivational feedback for maintaining streaks
- **Persistent Storage**: Habits and progress saved locally in JSON format

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

Run the habit tracker:

```bash
python personal_habit_tracker.py
```

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

## Development Status

This project follows a spec-driven development approach with Python best practices. Current implementation status:

✅ **Core Features Complete**
- Data persistence layer with JSON storage
- Streak calculation engine with smart logic
- User interaction and feedback system
- Progress display and reporting
- Main application workflow
- Comprehensive docstrings and type hints
- Modern Python packaging (`pyproject.toml`)
- Proper project metadata and licensing
- Code structure optimization and refactoring
- Error handling and robustness improvements

🚧 **In Progress**
- Comprehensive test suite (unit and integration tests)

📋 **Planned Enhancements** (Philosophy-Compliant)
- GUI with tkinter (optional, standard library)
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
├── habit_tracker.py               # Main application (✅ Core complete)
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

To continue development, check the remaining tasks in `.kiro/specs/personal-habit-tracker-core/tasks.md`:

- **Code Quality**: Optimize structure and readability (Priority)
- **Error Handling**: Improve robustness for edge cases
- **Testing**: Add comprehensive unit and integration tests
- **Future Features**: GUI (tkinter), data export, habit organization (all philosophy-compliant)

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