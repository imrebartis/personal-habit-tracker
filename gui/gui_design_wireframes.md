# GUI Design Wireframes and Layout

## Design Philosophy Alignment

The GUI interface maintains strict alignment with the project philosophy:
- **Simplicity**: Clean, minimal interface with no distracting elements
- **Privacy**: All data remains local, no network features
- **Standard Library Only**: Uses only tkinter (included with Python)
- **Distraction-Free**: Focus on habit completion, not gamification
- **User Control**: Clear, intuitive controls with keyboard navigation

## Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Personal Habit Tracker                                   [X]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📝 Today's Habits                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [✓ Complete] Drink 8 glasses of water [15 total] [3 streak] │
│  │ [✓ Complete] Exercise for 30 minutes  [8 total]  [0 streak] │
│  │ [✓ Complete] Read for 20 minutes      [22 total] [7 streak] │
│  │ [✓ Complete] Meditate                 [5 total]  [2 streak] │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🎉 Celebrations                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🏆 Amazing! 1 week streak for Read for 20 minutes!  │   │
│  │ 🔥 Great! 3 day streak for Drink 8 glasses of water!│   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Manage Habits]  [View History]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Habit Management Window

```
┌─────────────────────────────────────────────────────────────┐
│ Manage Habits                                            [X]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Current Habits:                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • Drink 8 glasses of water              [Remove]    │   │
│  │ • Exercise for 30 minutes               [Remove]    │   │
│  │ • Read for 20 minutes                   [Remove]    │   │
│  │ • Meditate                              [Remove]    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Add New Habit:                                             │
│  ┌─────────────────────────────────────┐ [Add Habit]       │
│  │ Enter habit name...                 │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  [Close]                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Progress History Window

```
┌─────────────────────────────────────────────────────────────┐
│ Progress History                                         [X]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Overall Progress                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Drink 8 glasses of water:                           │   │
│  │ ████████████████████░░░░░░░░ 15 total, 3 day streak │   │
│  │                                                     │   │
│  │ Exercise for 30 minutes:                            │   │
│  │ ████████░░░░░░░░░░░░░░░░░░░░ 8 total, 0 day streak  │   │
│  │                                                     │   │
│  │ Read for 20 minutes:                                │   │
│  │ ████████████████████████████ 22 total, 7 day streak│   │
│  │                                                     │   │
│  │ Meditate:                                           │   │
│  │ █████░░░░░░░░░░░░░░░░░░░░░░░░ 5 total, 2 day streak │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Close]                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Design Specifications

### Color Scheme
- **Background**: Light gray (#F5F5F5) - easy on eyes
- **Text**: Dark gray (#333333) - high contrast, readable
- **Checkboxes**: Green when checked (#4CAF50), gray when unchecked
- **Buttons**: Light blue (#E3F2FD) with dark blue text (#1976D2)
- **Celebration Messages**: Warm colors (gold #FFD700, orange #FF9800)
- **Progress Bars**: Green gradient (#4CAF50 to #81C784)

### Typography
- **Font**: System default (Segoe UI on Windows, SF Pro on macOS, Ubuntu on Linux)
- **Sizes**:
  - Title: 14pt bold
  - Habit names: 11pt regular
  - Progress info: 9pt regular
  - Buttons: 10pt regular

### Layout Principles
- **Spacing**: Consistent 10px padding throughout
- **Grouping**: Related elements grouped with subtle borders
- **Hierarchy**: Clear visual hierarchy with size and spacing
- **Accessibility**: High contrast, keyboard navigation, clear focus indicators

### Interactive Elements
- **Checkboxes**: Large, easy to click (20x20px minimum)
- **Buttons**: Consistent size, clear labels, keyboard accessible
- **Input Fields**: Clear placeholder text, validation feedback
- **Focus Indicators**: Clear blue outline for keyboard navigation

### Window Behavior
- **Main Window**: Resizable, minimum 600x400px
- **Modal Windows**: Fixed size, centered on parent
- **Closing**: Proper cleanup, save data before exit
- **Keyboard Shortcuts**:
  - Ctrl+M: Manage habits
  - Ctrl+H: View history
  - Escape: Close modal windows
  - Space/Enter: Toggle checkboxes

### Error Handling UI
- **Data Errors**: Non-intrusive status messages at bottom
- **File Errors**: Modal dialog with clear explanation and options
- **Input Validation**: Inline feedback with helpful messages
- **Graceful Degradation**: Fallback to CLI mode if GUI fails

## User Experience Flow

### First Time User
1. GUI launches with empty habit list
2. "Get Started" button opens habit management
3. User adds habits one by one
4. Returns to main window with new habits ready

### Daily User
1. GUI launches showing today's habits
2. User checks off completed habits
3. Celebration messages appear immediately
4. Progress updates in real-time
5. Save button confirms data persistence

### Habit Management
1. User clicks "Manage Habits" button
2. Modal window shows current habits
3. User can add/remove habits
4. Changes reflected immediately in main window
5. Data saved automatically

This design maintains the philosophy of simplicity while providing an intuitive, distraction-free interface for habit tracking.

## Interface Behavioral Differences

**Habit Management:**
- **CLI**: Habits can only be added during initial setup (first run)
- **GUI**: Habits can be added/removed anytime via "Manage Habits" button

**Session Management:**
- **CLI**: Session-based workflow (run → complete habits → save → exit)
- **GUI**: Persistent workflow (stay open for continuous interaction)

**Completion Method:**
- **CLI**: Linear prompts - asks about each habit once per session (yes/no)
- **GUI**: Interactive buttons - click "Complete" multiple times per habit

**Progress Display:**
- **CLI**: Summary shown at end of session
- **GUI**: Real-time updates + separate history dialog

**Data Persistence:**
- **CLI**: Saves once at session end
- **GUI**: Auto-saves after each completion

**Celebrations:**
- **CLI**: Text messages in console
- **GUI**: Animated popup windows

Both interfaces maintain full data compatibility and share the same `habits_data.json` file.