# CalmRead Agent Prompt for Claude

**Purpose:** This document provides complete context for an AI agent (Claude) to continue development of the CalmRead project. Read this entire document before taking any action.

---

## 🎯 Project Mission

CalmRead is a **calm, offline-first phonics reading app** for children ages 4-6, designed to run on the **BOOX Go Color 7** e-ink tablet. The core philosophy is **anti-screen-time**: we want children to learn to read effectively and then put the device down.

**Key Principles:**
- No gamification, no rewards, no streaks, no points
- No animations (e-ink incompatible and high-arousal)
- No internet connection required (offline-only)
- Systematic, explicit phonics instruction (Orton-Gillingham inspired)
- Calm, predictable, low-arousal experience
- Clear endpoints ("All Done" — no "Next Lesson" prompts)

---

## 📁 Repository Structure

```
CalmRead/
├── .agent/                    # Agent context and prompts (YOU ARE HERE)
│   ├── CLAUDE_PROMPT.md       # This file - main agent instructions
│   ├── NEXT_STEPS.md          # Prioritized task list
│   └── SESSION_LOG.md         # Log of completed work (append to this)
├── constitution/              # Core design principles (READ FIRST)
│   ├── calm_design.md         # Anti-gamification rules
│   ├── calm_budget.md         # Quantitative limits (0 animations, etc.)
│   ├── educational.md         # Phonics methodology
│   └── app_constraints.md     # Technical constraints (offline, e-ink)
├── schemas/                   # Data structure definitions
│   ├── lesson_schema.json     # Original schema (deprecated)
│   ├── lesson_schema_v2.json  # CURRENT simplified schema
│   ├── scope_sequence.json    # Curriculum structure schema
│   └── app_screen_schema.json # UI screen definitions
├── ai_roles/                  # AI role definitions
│   ├── system_architect.md    # Overall design decisions
│   ├── content_generator.md   # Lesson creation
│   ├── qa_red_team.md         # Quality assurance
│   └── builder_operator.md    # Implementation
├── pipelines/                 # Process documentation
│   ├── lesson_generation_pipeline.md
│   ├── audio_asset_pipeline.md
│   ├── curriculum_expansion_pipeline.md
│   └── qa_lint_pipeline.md
├── curriculum/                # Actual content
│   ├── scope_sequence_v1.json # 20-lesson curriculum plan
│   └── lessons/               # Individual lessons
│       ├── lesson_01/lesson.json
│       ├── lesson_02/lesson.json
│       ├── lesson_03/lesson.json
│       ├── lesson_04/lesson.json
│       └── lesson_05/lesson.json
├── qa/                        # Quality assurance
│   ├── scripts/
│   │   └── lesson_linter.py   # Automated validation tool
│   ├── checklists/
│   └── reports/
│       └── red_team_qa_report_v1.md  # Critical issues identified
├── beta/                      # Beta testing materials
├── operations/                # Runbooks and risk management
│   ├── runbook.md
│   └── known_risks.md
└── app/                       # Android application
    └── android/               # Kotlin/Android scaffold
```

---

## 🚨 Critical Issues to Address (from Red Team QA)

These are the highest priority items. Read `qa/reports/red_team_qa_report_v1.md` for full details.

### C-01: Schema Mismatch (CRITICAL)
**Problem:** The original `lesson_schema.json` is over-engineered and doesn't match actual lesson files.
**Solution:** Use `lesson_schema_v2.json` (simplified, flat structure). Migrate existing lessons if needed.

### C-02: Letter Names vs. Sounds (CRITICAL)
**Problem:** Lessons say "Meet the Letter M" instead of "Learning the /m/ Sound"
**Solution:** Refactor all lesson titles and instructions to focus on SOUNDS, not letter names.
**Example Fix:**
- ❌ "Meet the Letter M"
- ✅ "Learning the /m/ Sound"

### C-03: Android Scaffold Incomplete (CRITICAL)
**Problem:** The Android app is a placeholder with `//TODO` everywhere.
**Solution:** Build a functional `LessonPlayer` that can parse `lesson.json` and render steps.

### C-04: Calm Creep Risk (CRITICAL)
**Problem:** No proactive mechanism to prevent gradual erosion of calm principles.
**Solution:** Enforce the Calm Budget (`constitution/calm_budget.md`) — quantitative limits on UI elements.

---

## 🔧 Available Tools

### Automated Linter
Run before committing any lesson changes:
```bash
python qa/scripts/lesson_linter.py curriculum/lessons/lesson_XX/lesson.json
# Or lint all lessons:
python qa/scripts/lesson_linter.py --all curriculum/lessons/
```

The linter checks:
- Schema compliance
- Grapheme constraints (no banned letters in decodable content)
- Sight word validation
- Calm design keywords (no "amazing", "awesome", "points", etc.)

### Audio Generation
Follow `pipelines/audio_asset_pipeline.md` for generating TTS audio.

---

## 📋 Next Steps (Prioritized)

### Phase 1: Immediate Fixes (Do First)
1. **Refactor lesson titles** — Change all "Meet the Letter X" to "Learning the /x/ Sound"
2. **Update lesson instructions** — Focus on sounds throughout
3. **Validate all lessons pass linter** after changes

### Phase 2: Android Development
1. **Create LessonPlayer activity** — Parse and render `lesson.json`
2. **Implement step renderers** for each step type:
   - `explicit_phonics` — Show letter, play sound
   - `blending_practice` — Show segmented word, blend audio
   - `decodable_read` — Show passage with line highlighting
   - `record_read_aloud` — Record child's voice
   - `comprehension_prompt` — Multiple choice question
3. **Implement AudioPlayer** — Play lesson audio files
4. **Implement progress persistence** — Track completed lessons (local storage only)

### Phase 3: Content Expansion
1. **Generate lessons 06-10** — Follow scope_sequence_v1.json
2. **Generate audio assets** — Use audio_asset_pipeline.md
3. **QA each lesson** — Run linter + manual review

### Phase 4: Beta Preparation
1. **Build APK** for BOOX Go Color 7
2. **Create beta test protocol** — See beta/session_protocol.md
3. **Prepare feedback collection** — See beta/feedback_log.md

---

## 🎨 Design Constraints Quick Reference

### Calm Budget (Hard Limits)
| Element | Maximum |
|---------|---------|
| Animations per screen | 0 |
| Interactive elements per screen | 2 |
| Distinct colors per screen | 4 |
| Sound effects (non-voice) | 0 |
| Steps per lesson | 20 |
| Lesson duration | 15 min |
| New graphemes per lesson | 2 |

### Forbidden Keywords
Never use these in any user-facing text:
- Gamification: points, score, level up, unlock, achievement, badge, reward, coins, stars, streak, bonus, prize, win, winner, champion
- Excitement: amazing, awesome, fantastic, incredible, wow, hurry, quick, fast
- Pressure: time's up, don't miss, limited time

### Allowed Interaction Types
- `listen` — Child listens, taps to continue
- `record` — Child records audio
- `select` — Child selects from options (max 4)

---

## 📚 Phonics Curriculum Logic

### Grapheme Introduction Order (Scope & Sequence v1)
1. Lesson 01: m (/m/)
2. Lesson 02: s (/s/), t (/t/)
3. Lesson 03: a (/æ/) — First CVC words: mat, sat, at
4. Lesson 04-05: Short A practice and review
5. Lesson 06: p (/p/)
6. Lesson 07: n (/n/)
7. Lesson 08: i (/ɪ/) — Second vowel
8. ... continues through lesson 20

### Grapheme Constraint Rules
- **allowedGraphemes:** Cumulative list of all graphemes taught so far
- **bannedGraphemes:** All graphemes NOT yet taught
- **sightWords:** High-frequency irregular words (the, was, of, etc.)
- **CRITICAL:** Every word in decodable text must use ONLY allowed graphemes OR be a sight word

### Sight Words (Cumulative)
- Lesson 03+: "the"
- Lesson 05+: "a" (as article, though also decodable)
- Add sparingly — these are exceptions, not the rule

---

## 🔄 Workflow for Adding a New Lesson

1. **Check scope_sequence_v1.json** for the lesson specification
2. **Create directory:** `curriculum/lessons/lesson_XX/`
3. **Generate lesson.json** following `lesson_schema_v2.json`
4. **Run linter:** `python qa/scripts/lesson_linter.py curriculum/lessons/lesson_XX/lesson.json`
5. **Fix any issues** until linter passes
6. **Generate audio scripts** (extract from lesson.json)
7. **Generate audio files** using TTS (see audio_asset_pipeline.md)
8. **Manual QA review** using checklists in `qa/checklists/`
9. **Commit and push**

---

## 🤖 AI Role Switching

When working on this project, adopt the appropriate role:

### As System Architect (ROLE_A)
- Make high-level design decisions
- Resolve conflicts between constitutions
- Approve schema changes

### As Content Generator (ROLE_B)
- Create lesson content
- Write decodable passages
- Self-validate all output

### As QA/Red Team (ROLE_C)
- Adversarially test content
- Find violations of constitutions
- Challenge assumptions

### As Builder/Operator (ROLE_D)
- Write code
- Build infrastructure
- Deploy and maintain

---

## 📝 Session Logging

After each work session, append to `.agent/SESSION_LOG.md`:

```markdown
## Session: [DATE]

### Completed
- [List of completed tasks]

### Issues Encountered
- [Any problems or blockers]

### Next Session Should
- [Recommended next actions]
```

---

## ⚠️ Common Mistakes to Avoid

1. **Using letter names instead of sounds** — Always /m/, never "the letter M"
2. **Adding animations** — Budget is ZERO, no exceptions
3. **Using excitement language** — No "Great job!", just "All done."
4. **Introducing graphemes out of order** — Follow scope_sequence strictly
5. **Using words with banned graphemes** — Always validate with linter
6. **Adding "Next Lesson" prompts** — Sessions must have clear endpoints
7. **Skipping the linter** — Run it before every commit

---

## 🔗 Key File References

| Need | File |
|------|------|
| Understand calm philosophy | `constitution/calm_design.md` |
| Check quantitative limits | `constitution/calm_budget.md` |
| Understand phonics approach | `constitution/educational.md` |
| See lesson structure | `schemas/lesson_schema_v2.json` |
| See curriculum plan | `curriculum/scope_sequence_v1.json` |
| See example lesson | `curriculum/lessons/lesson_03/lesson.json` |
| Validate a lesson | `qa/scripts/lesson_linter.py` |
| See critical issues | `qa/reports/red_team_qa_report_v1.md` |

---

## 🚀 Getting Started Checklist

- [ ] Read this entire document
- [ ] Read `constitution/calm_design.md`
- [ ] Read `constitution/calm_budget.md`
- [ ] Read `qa/reports/red_team_qa_report_v1.md`
- [ ] Review `curriculum/lessons/lesson_03/lesson.json` as example
- [ ] Run linter on all lessons to verify current state
- [ ] Check `.agent/NEXT_STEPS.md` for prioritized tasks
- [ ] Begin work on highest priority item

---

*This prompt was created on January 11, 2026. Update as the project evolves.*
