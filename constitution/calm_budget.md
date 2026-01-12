# Calm Budget: Quantitative Design Constraints

**Version:** 1.0.0  
**Last Updated:** January 11, 2026  
**Status:** ACTIVE  
**Authority:** System Architect

## Purpose

The Calm Design Constitution defines *what* is forbidden. This document defines *how much* is allowed. By setting explicit, measurable limits on UI elements, we create a proactive defense against "calm creep"—the gradual introduction of features that erode the calm experience.

**Principle:** If you cannot measure it, you cannot enforce it.

## The Calm Budget

Every screen, lesson, and session has a "Calm Budget." If any limit is exceeded, the content or feature is automatically rejected.

### Per-Screen Limits

| Element | Maximum Allowed | Rationale |
| :--- | :--- | :--- |
| **Animations** | 0 | E-ink incompatible; high arousal |
| **Decorative Images** | 1 | Focus on text; reduce distraction |
| **Interactive Elements** | 2 | One primary action, one secondary (e.g., back) |
| **Distinct Colors** | 4 | Muted palette; e-ink optimization |
| **Sound Effects (non-voice)** | 0 | Reduce arousal; focus on narration |
| **Text Font Sizes** | 2 | Consistency; reduce visual noise |

### Per-Step Limits

| Element | Maximum Allowed | Rationale |
| :--- | :--- | :--- |
| **Words in Instruction** | 25 | Keep instructions concise |
| **Options in Multiple Choice** | 4 | Reduce cognitive load |
| **Recording Duration (seconds)** | 60 | Bounded interaction |

### Per-Lesson Limits

| Element | Maximum Allowed | Rationale |
| :--- | :--- | :--- |
| **Total Steps** | 20 | Bounded session length |
| **Total Duration (minutes)** | 15 | Prevent extended screen time |
| **Comprehension Questions** | 3 | Focus on reading, not testing |
| **New Graphemes Introduced** | 2 | Systematic progression |
| **New Sight Words Introduced** | 3 | Avoid overwhelming memory |

### Per-Session Limits

| Element | Maximum Allowed | Rationale |
| :--- | :--- | :--- |
| **Consecutive Lessons** | 1 (no autoplay) | Deliberate action required |
| **Total Active Time (minutes)** | 20 | Parental control; healthy limits |

## Forbidden Elements (Budget = 0)

These elements have a budget of zero. Any occurrence is a violation.

| Element | Reason |
| :--- | :--- |
| Confetti / Fireworks | High arousal |
| Bouncing / Shaking UI | High arousal |
| Countdown Timers | Time pressure |
| Streak Counters | Fear of loss |
| Point / Coin Displays | Gamification |
| Star Ratings | Variable reward |
| "Next Lesson" Auto-Prompt | Unbounded sessions |
| Background Music | Cognitive load |
| Notification Badges | Interruption |

## Measurement & Enforcement

### Automated Checks

The QA Linter (`qa/scripts/lesson_linter.py`) will be extended to automatically check:

*   Word count in instruction fields
*   Number of steps per lesson
*   Number of options in comprehension questions
*   Presence of forbidden keywords

### Manual Review Checklist

For elements that cannot be automatically checked (e.g., animations in code), the QA/Red Team must verify:

- [ ] Screen has ≤ 2 interactive elements
- [ ] Screen uses ≤ 4 distinct colors
- [ ] No animations are present
- [ ] No sound effects (other than voice) are present

## Budget Overruns

If a legitimate need arises to exceed a budget limit, the following process applies:

1.  **Document the Need:** Write a clear justification for why the limit must be exceeded.
2.  **Propose an Alternative:** Explore if the goal can be achieved within the budget.
3.  **Seek Approval:** The System Architect must approve any budget exception.
4.  **Log the Exception:** Record the exception in the lesson's metadata and the project changelog.

**Budget exceptions should be rare.** Frequent exceptions indicate the budget itself needs revision, not that exceptions should become routine.

## Changelog

| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0.0 | 2026-01-11 | Initial calm budget definition |
