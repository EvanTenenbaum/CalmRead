# CalmRead Quick Reference Card

## 🚫 NEVER DO

| Action | Why |
|--------|-----|
| Add animations | E-ink incompatible, high arousal |
| Use "amazing", "awesome", "great job" | Excitement violates calm design |
| Add points, stars, badges | Gamification forbidden |
| Use letter names ("Letter M") | Use sounds ("/m/") |
| Add "Next Lesson" prompts | Sessions must end cleanly |
| Use words with untaught graphemes | Strict grapheme control |
| Skip the linter | Always validate before commit |

## ✅ ALWAYS DO

| Action | How |
|--------|-----|
| Focus on sounds | "Learning /m/" not "Meet M" |
| End with "All Done" | Clear, calm endpoint |
| Run linter | `python qa/scripts/lesson_linter.py <file>` |
| Check grapheme constraints | Every word must be validated |
| Use calm language | Supportive but not excited |
| Follow scope sequence | Graphemes in order |
| Log your session | Append to SESSION_LOG.md |

## 📊 Calm Budget Limits

```
Animations per screen:     0
Interactive elements:      2
Colors per screen:         4
Sound effects (non-voice): 0
Steps per lesson:         20
Lesson duration:          15 min
New graphemes/lesson:      2
```

## 🔧 Key Commands

```bash
# Lint single lesson
python qa/scripts/lesson_linter.py curriculum/lessons/lesson_03/lesson.json

# Lint all lessons
python qa/scripts/lesson_linter.py --all curriculum/lessons/

# Check repo status
git status

# Commit changes
git add -A && git commit -m "Description"

# Push to GitHub
git push origin main
```

## 📁 Key Files

| Need | Location |
|------|----------|
| Main agent prompt | `.agent/CLAUDE_PROMPT.md` |
| Task list | `.agent/NEXT_STEPS.md` |
| Session history | `.agent/SESSION_LOG.md` |
| Calm rules | `constitution/calm_design.md` |
| Quantitative limits | `constitution/calm_budget.md` |
| Phonics rules | `constitution/educational.md` |
| Current schema | `schemas/lesson_schema_v2.json` |
| Curriculum plan | `curriculum/scope_sequence_v1.json` |
| Example lesson | `curriculum/lessons/lesson_03/lesson.json` |
| Critical issues | `qa/reports/red_team_qa_report_v1.md` |
| Linter script | `qa/scripts/lesson_linter.py` |

## 🎯 Current Grapheme Progression

| Lesson | New Graphemes | Cumulative |
|--------|---------------|------------|
| 01 | m | m |
| 02 | s, t | m, s, t |
| 03 | a | m, s, t, a |
| 04 | (practice) | m, s, t, a |
| 05 | (review) | m, s, t, a |
| 06 | p | m, s, t, a, p |
| 07 | n | m, s, t, a, p, n |
| 08 | i | m, s, t, a, p, n, i |

## 🔤 Sight Words (Cumulative)

| Lesson | New | Total |
|--------|-----|-------|
| 03+ | the | the |
| 10+ | is | the, is |
| 15+ | was, to | the, is, was, to |

## 📞 Step Types

| Type | Interaction | Purpose |
|------|-------------|---------|
| `introduction` | listen | Welcome, set context |
| `review` | listen | Review prior learning |
| `phonemic_awareness` | listen | Sound identification |
| `explicit_phonics` | listen | Teach grapheme-phoneme |
| `blending_practice` | listen | Model blending |
| `practice` | record | Child practices |
| `sight_word` | listen | Introduce sight word |
| `decodable_read` | listen | Model reading passage |
| `record_read_aloud` | record | Child reads passage |
| `comprehension_prompt` | select | Check understanding |
| `completion` | listen | End lesson |

## 🎨 Color Palette

| Use | Color | Hex |
|-----|-------|-----|
| Background | Warm White | #FAF8F5 |
| Primary Text | Charcoal | #2D3436 |
| Accent | Muted Teal | #5D9A96 |
| Secondary | Soft Gray | #B8C5C3 |

## ⚡ Emergency Fixes

**Linter fails with grapheme error:**
1. Check the word against `allowedGraphemes` in lesson
2. Either remove the word or add missing grapheme to prior lesson

**Linter fails with calm design error:**
1. Search for the forbidden keyword
2. Replace with calm alternative (see constitution/calm_design.md)

**Schema validation fails:**
1. Compare against `schemas/lesson_schema_v2.json`
2. Ensure all required fields present
3. Check data types match
