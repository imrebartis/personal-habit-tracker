# Requirements Document

## Introduction

The Personal Habit Tracker is a minimalist command-line application designed to help users build and maintain daily habits through consistent tracking and positive reinforcement. The system prioritizes simplicity, privacy, and user control while providing essential habit formation features like streak tracking and progress monitoring.

**Core Philosophy**: This tool embodies the belief that meaningful change happens through small, consistent daily actions. It intentionally avoids the complexity, social features, and data harvesting found in modern habit apps, focusing instead on what matters most: showing up every day with your data under your complete control.

**Philosophy Reference**: #[[file:philosophy.md]]

## Requirements

### Requirement 1

**User Story:** As a new user, I want to easily set up my initial habits when I first run the application, so that I can start tracking my daily routines immediately.

#### Acceptance Criteria

1. WHEN the application is run for the first time THEN the system SHALL detect no existing data file and prompt for habit creation
2. WHEN prompted for habit creation THEN the system SHALL allow the user to enter multiple habit names interactively
3. WHEN the user types 'done' THEN the system SHALL complete the setup process and save the initial habits
4. WHEN habits are created THEN each habit SHALL be initialized with zero completions and zero streak

### Requirement 2

**User Story:** As a daily user, I want to mark my habits as completed each day, so that I can track my consistency and build positive momentum.

#### Acceptance Criteria

1. WHEN the application runs THEN the system SHALL prompt the user for each habit's completion status for the current day
2. WHEN a user marks a habit as completed THEN the system SHALL increment the total completion count
3. WHEN a user marks a habit as completed THEN the system SHALL provide positive reinforcement feedback
4. WHEN a user marks a habit as not completed THEN the system SHALL provide encouraging feedback
5. WHEN all habits are processed THEN the system SHALL save the updated data to persistent storage

### Requirement 3

**User Story:** As a motivated user, I want to see my current streaks and total progress, so that I can stay motivated and track my long-term consistency.

#### Acceptance Criteria

1. WHEN daily check-in is complete THEN the system SHALL display a summary of all habits with their total completions and current streaks
2. WHEN a habit has a streak of 3 or more days THEN the system SHALL display a "Great!" celebration message
3. WHEN a habit has a streak of 7 or more days THEN the system SHALL display an "Amazing!" celebration message with week count
4. WHEN displaying progress THEN the system SHALL show both total completions and current streak for each habit

### Requirement 4

**User Story:** As a consistent user, I want my streaks to be calculated accurately based on consecutive daily completions, so that I can trust the system to reflect my actual progress.

#### Acceptance Criteria

1. WHEN a habit is completed on consecutive days THEN the system SHALL increment the streak counter
2. WHEN a habit is completed after being completed yesterday THEN the system SHALL increment the existing streak
3. WHEN a habit is completed after missing one or more days THEN the system SHALL reset the streak to 1
4. WHEN a habit is not completed and the last completion was more than one day ago THEN the system SHALL reset the streak to 0
5. WHEN a habit is completed multiple times on the same day THEN the system SHALL not increment the streak beyond the daily completion

### Requirement 5

**User Story:** As a privacy-conscious user, I want my habit data to be stored locally on my machine, so that my personal growth information remains private and under my control.

#### Acceptance Criteria

1. WHEN the application saves data THEN the system SHALL store all information in a local JSON file
2. WHEN the application loads data THEN the system SHALL read from the local JSON file only
3. WHEN the application processes dates THEN the system SHALL handle date conversion between storage format and runtime objects correctly
4. WHEN no internet connection is available THEN the system SHALL continue to function normally
5. WHEN the data file exists THEN the system SHALL load existing habits and their progress

### Requirement 6

**User Story:** As a developer user, I want the application to be simple and hackable, so that I can customize and extend it according to my specific needs.

#### Acceptance Criteria

1. WHEN examining the codebase THEN the system SHALL use only Python standard library dependencies
2. WHEN running the application THEN the system SHALL work on any system with Python 3.6 or higher
3. WHEN reviewing the code THEN the system SHALL have clear function separation and documentation
4. WHEN modifying the code THEN the system SHALL maintain backward compatibility with existing data files
5. WHEN extending functionality THEN the system SHALL provide clear extension points through modular design