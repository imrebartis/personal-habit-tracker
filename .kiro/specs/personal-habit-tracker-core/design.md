# Design Document

## Overview

The Personal Habit Tracker follows a simple, functional architecture built around core operations: data persistence, habit management, streak calculation, and user interaction. The design prioritizes simplicity, maintainability, and extensibility while keeping all functionality in a single, self-contained Python module.

**Philosophy Alignment**: All design decisions must align with the project philosophy defined in #[[file:philosophy.md]], prioritizing privacy, simplicity, and user control over feature complexity.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Core Logic      │───▶│  Data Storage   │
│ (CLI/GUI)       │    │  (Functions)     │    │  (JSON File)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   User Output    │
                       │ (Console/GUI)    │
                       └──────────────────┘
```

**Dual Interface Architecture**
- **CLI Interface**: Command-line based interaction (personal_habit_tracker.py)
- **GUI Interface**: Tkinter-based visual interface (gui_habit_tracker.py)
- **Shared Backend**: Both interfaces use identical core logic and data format
- **Launcher**: Interactive interface selection (habit_tracker.py)

### Design Principles

1. **Single Responsibility**: Each function handles one specific aspect of habit tracking
2. **Functional Programming**: Stateless functions that transform data rather than maintaining state
3. **Data-Driven**: All application state stored in simple data structures (lists and dictionaries)
4. **Fail-Safe**: Graceful handling of missing files and invalid input
5. **Extensible**: Clear separation allows for easy feature additions

## Components and Interfaces

### Data Layer

**Habit Data Structure**
```python
{
    'habit': str,              # Habit name
    'total_completed': int,    # Total times completed
    'current_streak': int,     # Current consecutive days
    'last_completed': date     # Last completion date (None if never)
}
```

**Storage Interface**
- `load_habits() -> List[Dict]`: Load habits from JSON with date conversion
- `save_habits(habits: List[Dict]) -> None`: Save habits to JSON with date serialization

### Business Logic Layer

**Habit Management**
- `create_habit(name: str) -> Dict`: Factory function for new habit objects
- `update_habit_streak(habit: Dict, today: date) -> None`: Update streak on completion
- `check_streak_break(habit: Dict, today: date) -> None`: Reset streak on miss

**Streak Calculation Logic**
- Consecutive days: Increment existing streak
- Gap of one day: Reset to 1 (new streak)
- Gap of multiple days: Reset to 0 (broken streak)
- Same day multiple completions: No additional increment

### Presentation Layer

**CLI Interface (personal_habit_tracker.py)**
- `setup_new_habits() -> List[Dict]`: Interactive habit creation workflow (first run only)
- `process_daily_habits(habits: List[Dict]) -> List[str]`: Linear daily check-in workflow
- `display_results(habits: List[Dict], performed_habits: List[str]) -> None`: End-of-session progress display
- **Session-based**: Runs once, processes all habits, saves, then exits
- **Text-based**: Console prompts, text celebrations, command-line error messages
- **Limitation**: No ongoing habit management - habits only created during initial setup

**GUI Interface (gui/gui_habit_tracker.py)**
- `HabitTrackerGUI`: Main tkinter application class with persistent session
- Visual habit completion with buttons (allows multiple completions per day)
- Real-time progress bars and streak indicators with auto-save
- Animated celebration popups for achievements
- **Ongoing habit management dialogs** (add/remove habits anytime)
- **Interactive workflow**: Multiple completions, progress viewing, habit management in one session
- Keyboard navigation and accessibility features
- Dialog-based error handling with graceful fallbacks

**Shared Feedback System**
- `get_streak_message(streak: int, habit_name: str) -> Optional[str]`: Celebration messages
- Immediate feedback on completion/miss
- Progress summary with totals and streaks
- Both interfaces provide identical functionality and data compatibility

### Application Controller

**CLI Main Workflow (personal_habit_tracker.py)**
```python
def main():
    # 1. Parse command line arguments (--gui, --cli)
    # 2. Launch appropriate interface
    # 3. Initialize and welcome user
    # 4. Load existing habits or create new ones
    # 5. Process daily habit completions
    # 6. Save updated data
    # 7. Display results and progress
```

**GUI Main Workflow (gui/gui_habit_tracker.py)**
```python
class HabitTrackerGUI:
    def __init__():
        # 1. Initialize tkinter window and components
        # 2. Load existing habits
        # 3. Create visual interface

    def on_habit_complete():
        # 1. Update habit data (matches CLI behavior)
        # 2. Auto-save progress
        # 3. Refresh display
        # 4. Show celebrations if applicable
```

**Launcher (habit_tracker.py)**
- Interactive interface selection
- Platform-specific launcher scripts
- Graceful fallback from GUI to CLI

## Data Models

### Habit Model

```python
class Habit:
    name: str                    # Human-readable habit name
    total_completed: int         # Lifetime completion count
    current_streak: int          # Current consecutive days
    last_completed: Optional[date]  # Most recent completion date
```

### Application State

**CLI Application State**
The CLI maintains no persistent state between runs. All state is:
- Loaded from `habits_data.json` at startup
- Modified during execution
- Saved back to `habits_data.json` at completion

**GUI Application State**
The GUI maintains minimal runtime state for user interface:
- Habit data loaded from `habits_data.json` at startup
- Session completion tracking (`today_completions`) for display
- Button references (`habit_buttons`) for keyboard navigation
- Auto-save after each habit completion
- Shared data format ensures CLI-GUI compatibility

### Date Handling

- **Runtime**: Python `datetime.date` objects for calculations
- **Storage**: ISO format strings (`YYYY-MM-DD`) in JSON
- **Conversion**: Automatic serialization/deserialization on load/save

## Error Handling

### File System Errors
- **Missing data file**: Gracefully handled by returning empty list
- **Corrupted JSON**: Application will fail fast with clear error message
- **Permission errors**: Standard Python exceptions propagated to user

### Input Validation
- **Habit names**: No validation - accepts any non-empty string
- **Yes/no responses**: Case-insensitive matching, defaults to "no"
- **Date calculations**: Robust handling of edge cases and timezone issues

### Data Integrity
- **Date consistency**: Automatic conversion prevents date format issues
- **Streak calculation**: Defensive programming prevents negative streaks
- **File atomicity**: JSON write operations are atomic at OS level

## Testing Strategy

### Unit Testing Approach

**Core Functions to Test**
1. `create_habit()` - Verify proper initialization
2. `update_habit_streak()` - Test all streak scenarios
3. `check_streak_break()` - Verify streak reset logic
4. `get_streak_message()` - Test celebration thresholds
5. `load_habits()` / `save_habits()` - Data persistence round-trip

**Test Categories**
- **Happy Path**: Normal daily usage patterns
- **Edge Cases**: Same-day completions, date boundaries, leap years
- **Error Conditions**: Missing files, corrupted data, invalid dates
- **Streak Logic**: All combinations of completion patterns

### Integration Testing

**CLI Workflow Testing**
- Complete application runs with various input patterns
- Data persistence across multiple sessions
- First-time setup workflow
- Progress display accuracy

**GUI Integration Testing**
- GUI-backend integration with shared data format
- Interface switching (CLI ↔ GUI) with data compatibility
- Error handling and graceful fallbacks
- Cross-platform GUI functionality

**GUI-Specific Testing**
- Component initialization and layout
- Event handling (button clicks, keyboard navigation)
- Visual updates and real-time progress display
- Dialog functionality (habit management, progress history)
- Accessibility features and keyboard shortcuts
- Celebration animations and user feedback

### Manual Testing

**CLI User Experience Testing**
- Clarity of prompts and messages
- Appropriateness of celebration messages
- Progress display readability
- Error message helpfulness

**GUI User Experience Testing**
- Visual design and layout clarity
- Button responsiveness and feedback
- Progress bar accuracy and visual appeal
- Celebration animation timing and appropriateness
- Dialog usability and workflow
- Keyboard navigation effectiveness

## Performance Considerations

### Scalability
- **Habit Count**: Linear performance, suitable for dozens of habits
- **History Length**: No historical data stored, constant memory usage
- **File I/O**: Single read/write per session, minimal overhead

### Memory Usage
- **Data Structure**: Simple dictionaries and lists, minimal memory footprint
- **Date Objects**: Efficient datetime.date objects for calculations
- **No Caching**: Fresh data load each session prevents stale data issues

### Startup Time
- **Cold Start**: Sub-second startup for typical habit counts
- **File Loading**: JSON parsing is fast for expected data sizes
- **No Dependencies**: No import overhead from external libraries

## Security Considerations

### Data Privacy
- **Local Storage**: All data remains on user's machine
- **No Network**: Zero network communication or data transmission
- **File Permissions**: Relies on OS file system permissions

### Input Safety
- **No Code Execution**: All user input treated as data, not code
- **File Path Safety**: Fixed file name prevents path traversal
- **JSON Safety**: Standard library JSON parser prevents injection

## Current Implementation

### Implemented Features

**Dual Interface System**
- ✅ CLI interface with command-line interaction
- ✅ GUI interface with tkinter (visual habit tracking)
- ✅ Shared backend ensuring perfect compatibility
- ✅ Interactive launcher for interface selection
- ✅ Platform-specific launcher scripts

**GUI Features**
- ✅ Visual habit completion with buttons
- ✅ Multiple completions per day (matches CLI behavior)
- ✅ Real-time progress bars and streak indicators
- ✅ Celebration animations for achievements
- ✅ Habit management dialogs (add/remove habits)
- ✅ Progress history visualization
- ✅ Keyboard navigation and accessibility
- ✅ Auto-save functionality
- ✅ Error handling and robustness
- ✅ Comprehensive test suite

## Extension Points

### Future Enhancements (Philosophy-Compliant)

**Data Model Extensions**
- Add habit categories or tags (simple, local organization)
- Store completion times or notes
- Track habit difficulty or importance

**Streak Logic Variations**
- Configurable streak reset policies (user choice, local settings)
- Weekly or custom period streaks
- Streak recovery mechanisms

**Analytics and Reporting**
- Historical trend analysis
- Completion rate statistics
- Export capabilities (CSV, plain text for user control)

**Integration Possibilities**
- Calendar integration (local only)
- Simple reminder systems (no notifications)
- Health app connectivity (user-controlled)

### Rejected Features (Philosophy Violations)
- Web interface or cloud storage (violates privacy)
- Social sharing or social features (violates privacy)
- Mobile apps with push notifications (violates simplicity)
- Data analytics or user tracking (violates privacy)
- Monetization or subscription models (violates accessibility)