# Audio Asset Generation Pipeline

**Version:** 1.0.0  
**Last Updated:** January 11, 2026

## Overview

This pipeline defines the process for generating all audio assets required for CalmRead lessons. It ensures consistency in voice, tone, and quality across all narration, prompts, and word pronunciations.

## Pipeline Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  lesson.json    │────▶│  Extract Audio  │────▶│  Audio Script   │
│  (approved)     │     │  Transcripts    │     │  Document       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Audio Files    │◀────│  TTS Generation │◀────│  Voice Profile  │
│  (.mp3)         │     │  (API Call)     │     │  Selection      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│  Audio QA       │────▶│  Lesson Bundle  │
│  (Human Review) │     │  (Complete)     │
└─────────────────┘     └─────────────────┘
```

## Voice Profile Specification

All CalmRead audio must adhere to a consistent voice profile to maintain the calm, predictable experience.

### Primary Narrator Voice

| Attribute | Specification | Rationale |
| :--- | :--- | :--- |
| **Gender** | Neutral or Female | Research suggests calming effect |
| **Tone** | Warm, Calm, Supportive | Low arousal principle |
| **Pace** | Slow to Moderate (120-140 WPM) | Allows processing time |
| **Pitch** | Mid-range, Consistent | Predictability |
| **Emotion** | Gentle Encouragement | No excitement, no pressure |
| **Accent** | Standard American English | Clarity for target audience |

### Forbidden Voice Characteristics

*   Excited or enthusiastic tone
*   High pitch or squeaky voice
*   Fast-paced delivery
*   Dramatic pauses or emphasis
*   Sing-song or overly melodic intonation
*   Robotic or monotone delivery

### TTS Provider Recommendations

| Provider | Recommended Voice | Notes |
| :--- | :--- | :--- |
| **Google Cloud TTS** | `en-US-Neural2-C` (Female) | High quality, natural |
| **Amazon Polly** | `Joanna` (Neural) | Good for long narration |
| **ElevenLabs** | Custom Clone (if available) | Best quality, higher cost |
| **OpenAI TTS** | `nova` or `shimmer` | Good balance of quality/cost |

## Audio Types & Specifications

### 1. Instruction Audio

*   **Purpose:** Narrate lesson instructions and explanations.
*   **Format:** MP3, 128kbps, 44.1kHz
*   **Duration:** 2-10 seconds typical
*   **Naming:** `instruction_{step_id}.mp3`

**Example Transcript:**
> "This is the letter M. It makes the sound /m/. Watch and listen."

### 2. Prompt Audio

*   **Purpose:** Prompt the child for an action (e.g., "Now you try").
*   **Format:** MP3, 128kbps, 44.1kHz
*   **Duration:** 1-5 seconds typical
*   **Naming:** `prompt_{step_id}.mp3`

**Example Transcript:**
> "Now you try. Say /m/."

### 3. Word Pronunciation Audio

*   **Purpose:** Model correct pronunciation of individual words.
*   **Format:** MP3, 128kbps, 44.1kHz
*   **Duration:** 0.5-2 seconds
*   **Naming:** `word_{word}.mp3`

**Example:** `word_mat.mp3` containing the pronunciation of "mat"

### 4. Phoneme Audio

*   **Purpose:** Model isolated phoneme sounds.
*   **Format:** MP3, 128kbps, 44.1kHz
*   **Duration:** 0.5-1.5 seconds
*   **Naming:** `phoneme_{sound}.mp3` (e.g., `phoneme_m.mp3`)

**Note:** Phoneme audio requires careful production. The sound should be isolated without adding a schwa (e.g., /m/ not /muh/).

### 5. Sentence Audio

*   **Purpose:** Model reading of decodable sentences.
*   **Format:** MP3, 128kbps, 44.1kHz
*   **Duration:** 2-8 seconds
*   **Naming:** `sentence_{index}.mp3`

## Generation Process

### Step 1: Extract Transcripts

Run the transcript extraction script on an approved `lesson.json`:

```bash
python scripts/extract_audio_transcripts.py curriculum/lessons/lesson_03/lesson.json
```

**Output:** `lesson_03_audio_scripts.md`

### Step 2: Review & Edit Transcripts

A human reviewer should:

1.  Check transcripts for calm, appropriate language.
2.  Ensure phoneme representations are correct (e.g., `/m/` not `m`).
3.  Add pronunciation guides for any ambiguous words.
4.  Verify word pronunciations match the target accent.

### Step 3: Generate Audio via TTS API

Use the audio generation script:

```bash
python scripts/generate_audio.py lesson_03_audio_scripts.md --output curriculum/lessons/lesson_03/audio/
```

**Script Parameters:**

| Parameter | Description |
| :--- | :--- |
| `--voice` | TTS voice ID (default: configured in settings) |
| `--speed` | Speech rate multiplier (default: 0.9) |
| `--output` | Output directory for audio files |

### Step 4: Audio QA Review

A human reviewer must listen to each generated audio file and verify:

- [ ] Voice matches the specified profile (calm, warm, slow)
- [ ] Pronunciation is correct
- [ ] No artifacts or glitches
- [ ] Volume is consistent across all files
- [ ] Duration matches expected range

### Step 5: Integrate into Lesson Bundle

Move approved audio files to the lesson directory:

```
curriculum/lessons/lesson_03/
├── lesson.json
├── audio/
│   ├── instruction_step_01.mp3
│   ├── instruction_step_02.mp3
│   ├── prompt_step_04.mp3
│   ├── word_mat.mp3
│   ├── word_sat.mp3
│   ├── phoneme_m.mp3
│   └── ...
```

Update `lesson.json` to reference the correct audio paths.

## Prompt Template for TTS

When using an LLM to prepare transcripts for TTS, use this prompt:

```
You are preparing audio transcripts for a children's reading app.

VOICE REQUIREMENTS:
- Tone: Calm, warm, supportive
- Pace: Slow (120-140 words per minute)
- No excitement, no pressure
- Clear pronunciation

TRANSCRIPT TO PREPARE:
[Paste transcript here]

OUTPUT:
1. Cleaned transcript (remove any non-spoken elements)
2. Pronunciation guide for any unusual words
3. Suggested pauses (marked with "...")
```

## Quality Checklist

Before marking audio generation complete:

- [ ] All audio assets listed in `lesson.json` exist
- [ ] All audio files play without errors
- [ ] Volume is normalized across all files
- [ ] Voice is consistent (same voice for all files in lesson)
- [ ] Phoneme pronunciations are isolated (no added schwa)
- [ ] Pace is slow and calm
- [ ] No forbidden characteristics detected

## Error Handling

| Error | Resolution |
| :--- | :--- |
| TTS API failure | Retry with exponential backoff; fall back to alternative provider |
| Poor pronunciation | Manually edit transcript with phonetic spelling; regenerate |
| Inconsistent volume | Apply audio normalization in post-processing |
| Voice sounds excited | Adjust TTS parameters (lower pitch, slower speed); regenerate |

## Changelog

| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0.0 | 2026-01-11 | Initial pipeline definition |
