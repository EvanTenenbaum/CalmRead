# CalmRead Next Steps

**Last Updated:** January 11, 2026  
**Status:** Active Development

---

## 🔴 Priority 1: Critical Fixes (BLOCKING)

These must be completed before any new feature work.

### 1.1 Refactor Lesson Language to Sound-Focused
**Status:** Not Started  
**Effort:** 2-3 hours  
**Files to modify:**
- `curriculum/lessons/lesson_01/lesson.json`
- `curriculum/lessons/lesson_02/lesson.json`

**Changes required:**
```
BEFORE: "title": "Meet the Letter M"
AFTER:  "title": "Learning the /m/ Sound"

BEFORE: "instruction": "This is the letter M."
AFTER:  "instruction": "This is the sound /m/."
```

**Validation:** Run linter after changes. All lessons must pass.

### 1.2 Migrate Lessons to Schema v2
**Status:** Not Started  
**Effort:** 1-2 hours  

Review each lesson against `schemas/lesson_schema_v2.json` and ensure compliance. The v2 schema is simpler and more flexible.

### 1.3 Remove "a" from Sight Words
**Status:** Not Started  
**Effort:** 30 minutes  

The word "a" is decodable (short vowel sound). It should not be classified as a sight word. Update:
- `curriculum/scope_sequence_v1.json`
- Any lessons that list "a" as a sight word

---

## 🟡 Priority 2: Android App Development

### 2.1 Create LessonPlayer Activity
**Status:** Not Started  
**Effort:** 4-6 hours  
**Location:** `app/android/app/src/main/java/com/calmread/lesson/`

**Requirements:**
- Parse `lesson.json` from assets
- Manage step progression (current step, next step)
- Handle different step types
- No scrolling — page-based navigation only

**Suggested structure:**
```kotlin
class LessonPlayer : AppCompatActivity() {
    private var currentLesson: Lesson? = null
    private var currentStepIndex: Int = 0
    
    fun loadLesson(lessonId: String)
    fun renderCurrentStep()
    fun advanceToNextStep()
    fun handleUserAction(action: String)
}
```

### 2.2 Implement Step Renderers
**Status:** Not Started  
**Effort:** 6-8 hours  

Create a renderer for each step type:

| Step Type | Priority | Complexity |
|-----------|----------|------------|
| `explicit_phonics` | HIGH | Low |
| `completion` | HIGH | Low |
| `blending_practice` | HIGH | Medium |
| `decodable_read` | HIGH | Medium |
| `record_read_aloud` | MEDIUM | High |
| `comprehension_prompt` | MEDIUM | Medium |
| `review` | LOW | Low |

### 2.3 Implement Audio Playback
**Status:** Partial (AudioPlayer.kt exists but incomplete)  
**Effort:** 2-3 hours  

**Requirements:**
- Play MP3 files from lesson assets
- Support sequential playback (instruction → prompt)
- Handle playback completion callbacks

### 2.4 Implement Recording
**Status:** Partial (AudioRecorder.kt exists but incomplete)  
**Effort:** 3-4 hours  

**Requirements:**
- Record child's voice during `record_read_aloud` steps
- Save recordings locally (no upload)
- Playback for "Listen and Compare" feature

---

## 🟢 Priority 3: Content Expansion

### 3.1 Generate Lessons 06-10
**Status:** Not Started  
**Effort:** 4-5 hours  

Follow `curriculum/scope_sequence_v1.json` for specifications:
- Lesson 06: Introduce P (/p/)
- Lesson 07: Introduce N (/n/)
- Lesson 08: Introduce I (/ɪ/) — second vowel
- Lesson 09: Short I Practice
- Lesson 10: Short I Review

**Process for each:**
1. Extract spec from scope_sequence_v1.json
2. Generate lesson.json following schema v2
3. Run linter
4. Fix issues
5. Commit

### 3.2 Generate Audio Assets for Lessons 01-05
**Status:** Not Started  
**Effort:** 2-3 hours  

Follow `pipelines/audio_asset_pipeline.md`:
1. Extract transcripts from each lesson
2. Generate TTS audio using recommended voice
3. Save to `curriculum/lessons/lesson_XX/audio/`
4. Update lesson.json with correct paths

### 3.3 Create Decodable Reader Library
**Status:** Not Started  
**Effort:** 3-4 hours  

Create additional short decodable passages that can be used for practice:
- Location: `curriculum/decodable_texts/`
- Organized by grapheme set (e.g., `msta_texts.json`)
- Each text validated against grapheme constraints

---

## 🔵 Priority 4: Infrastructure & Tooling

### 4.1 Automate Pipeline Orchestration
**Status:** Not Started  
**Effort:** 4-5 hours  

Create a master script that:
1. Reads scope_sequence_v1.json
2. Identifies lessons needing generation
3. Generates lesson content (via LLM API)
4. Runs linter automatically
5. Reports results

**Location:** `scripts/generate_lesson.py`

### 4.2 Extend Linter Capabilities
**Status:** Partial  
**Effort:** 2-3 hours  

Add checks for:
- [ ] Word count in instructions (max 25)
- [ ] Step count per lesson (max 20)
- [ ] Comprehension question count (max 3)
- [ ] New grapheme count (max 2)
- [ ] Estimated duration calculation

### 4.3 Create Lesson Diff Tool
**Status:** Not Started  
**Effort:** 2 hours  

Tool to compare two lesson versions and highlight changes:
```bash
python scripts/lesson_diff.py lesson_03_v1.json lesson_03_v2.json
```

---

## 🟣 Priority 5: Beta Preparation

### 5.1 Build Debug APK
**Status:** Not Started  
**Effort:** 1-2 hours  

Configure Gradle for debug build targeting BOOX Go Color 7:
- Target SDK: 30+
- E-ink refresh optimization
- Large touch targets (56dp minimum)

### 5.2 Create Beta Test Script
**Status:** Partial (session_protocol.md exists)  
**Effort:** 1 hour  

Finalize the step-by-step script for conducting beta sessions with children.

### 5.3 Prepare Feedback Forms
**Status:** Partial (feedback_log.md exists)  
**Effort:** 1 hour  

Create structured observation forms for beta testers (parents/teachers).

---

## Completed Tasks

| Task | Completed | Notes |
|------|-----------|-------|
| Create repository structure | 2026-01-11 | Full scaffold created |
| Write constitution documents | 2026-01-11 | 3 constitutions + calm budget |
| Create lesson schema | 2026-01-11 | v1 and v2 created |
| Generate lessons 01-05 | 2026-01-11 | All pass linter |
| Create automated linter | 2026-01-11 | Python script working |
| Red Team QA review | 2026-01-11 | Report in qa/reports/ |
| Create Android scaffold | 2026-01-11 | Basic structure only |

---

## Notes for Next Agent

- The project is at a critical inflection point — the foundation is solid but needs refinement before scaling
- Focus on the sound-focused language refactor FIRST — it's a philosophical issue that affects everything
- The Android app needs significant work — the scaffold is just a starting point
- Always run the linter before committing any lesson changes
- When in doubt, refer to the constitutions — they are the source of truth
