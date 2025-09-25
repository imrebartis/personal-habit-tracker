# Design Document

## Overview

The Personal Habit Tracker follows a simple, functional architecture built around core operations: data persistence, habit management, streak calculation, and user interaction. The design prioritizes simplicity, maintainability, and extensibility while keeping all functionality in a single, self-contained Python module.

**Philosophy Alignment**: All design decisions must align with the project philosophy defined in #[[file:philosophy.md]], prioritizing privacy, simplicity, and user control over feature complexity.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Core Logic      │───▶│  Data Storage   │
│   (CLI)         │    │  (Functions)     │    │  (JSON File)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   User Output    │
                       │   (Console)      │
                       └──────────────────┘
```

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

**User Interaction**
- `setup_new_habits() -> List[Dict]`: Interactive habit creation workflow
- `process_daily_habits(habits: List[Dict]) -> List[str]`: Daily check-in workflow
- `display_results(habits: List[Dict], performed_habits: List[str]) -> None`: Progress display

**Feedback System**
- `get_streak_message(streak: int, habit_name: str) -> Optional[str]`: Celebration messages
- Immediate feedback on completion/miss
- Progress summary with totals and streaks

### Application Controller

**Main Workflow**
```python
def main():
    # 1. Initialize and welcome user
    # 2. Load existing habits or create new ones
    # 3. Process daily habit completions
    # 4. Save updated data
    # 5. Display results and progress
```

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

The application maintains no persistent state between runs. All state is:
- Loaded from `habits_data.json` at startup
- Modified during execution
- Saved back to `habits_data.json` at completion

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

**Workflow Testing**
- Complete application runs with various input patterns
- Data persistence across multiple sessions
- First-time setup workflow
- Progress display accuracy

### Manual Testing

**User Experience Testing**
- Clarity of prompts and messages
- Appropriateness of celebration messages
- Progress display readability
- Error message helpfulness

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

## Extension Points

### Future Enhancements

**Data Model Extensions**
- Add habit categories or tags
- Store completion times or notes
- Track habit difficulty or importance

**Streak Logic Variations**
- Configurable streak reset policies
- Weekly or custom period streaks
- Streak recovery mechanisms

**User Interface Options**
- GUI implementation with tkinter
- Web interface for remote access
- Mobile app integration

**Analytics and Reporting**
- Historical trend analysis
- Completion rate statistics
- Export capabilities for external analysis

**Integration Possibilities**
- Calendar integration
- Reminder systems
- Health app connectivity
- Social sharing (optional)