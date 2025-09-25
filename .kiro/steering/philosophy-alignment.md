---
inclusion: always
---

# Philosophy Alignment Rule

## Core Principle
All specifications, design decisions, and implementation tasks MUST align with the project philosophy defined in philosophy.md.

## Philosophy Reference
#[[file:philosophy.md]]

## Alignment Checklist

Before creating or modifying any spec document, verify:

### ✅ Privacy & Control
- [ ] Does this maintain local-only data storage?
- [ ] Does this avoid any cloud services or data transmission?
- [ ] Does this keep the user in complete control of their data?

### ✅ Simplicity & Minimalism
- [ ] Does this add unnecessary complexity?
- [ ] Does this maintain the "simplest possible interface"?
- [ ] Does this avoid feature bloat or distracting elements?

### ✅ Accessibility & Hackability
- [ ] Does this maintain Python standard library only?
- [ ] Does this keep the code readable and modifiable?
- [ ] Does this provide clear extension points?

### ✅ Encouraging & Forgiving
- [ ] Does this celebrate progress appropriately?
- [ ] Does this handle setbacks with encouragement?
- [ ] Does this focus on total completions alongside streaks?

### ✅ Problem Solving Focus
- [ ] Does this solve one of the core problems (Complexity, Privacy, Accessibility, Motivation, Ownership)?
- [ ] Does this avoid creating the problems we're trying to solve?

## Red Flags - Immediately Reject If Present
- Social features or sharing capabilities
- Cloud storage or external services
- Complex UI frameworks or heavy dependencies
- Monetization schemes or subscription models
- Data analytics or user tracking
- Notifications or interruption-based features
- Gamification that creates pressure rather than encouragement

## Decision Framework
When in doubt, ask: "Does this make habit formation simpler, more private, and more under the user's control?"