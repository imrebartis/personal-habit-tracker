# Philosophy Compliance Check

Use this template when creating or reviewing any spec document.

## Philosophy Reference
Review: #[[file:philosophy.md]]

## Compliance Questions

### Privacy & Control ✅
- Does this feature keep all data local?
- Does this avoid any external dependencies or services?
- Does this maintain user ownership of their data?

### Simplicity & Minimalism ✅
- Is this the simplest solution to the problem?
- Does this avoid unnecessary complexity?
- Does this maintain the "distraction-free" principle?

### Accessibility & Hackability ✅
- Can this run on any system with Python?
- Is the code readable and modifiable?
- Are there clear extension points?

### Encouraging & Forgiving ✅
- Does this celebrate progress appropriately?
- Does this handle failures with encouragement?
- Does this avoid creating pressure or guilt?

### Problem-Solving Focus ✅
- Which core problem does this solve? (Complexity/Privacy/Accessibility/Motivation/Ownership)
- Does this avoid creating the problems we're solving?

## Red Flag Check ❌
Reject immediately if any of these are present:
- [ ] Social features
- [ ] Cloud storage
- [ ] Heavy dependencies
- [ ] Monetization elements
- [ ] User tracking
- [ ] Interruption-based features

## Approval
- [ ] All philosophy principles maintained
- [ ] No red flags present
- [ ] Aligns with project vision