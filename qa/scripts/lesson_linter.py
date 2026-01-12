#!/usr/bin/env python3
"""
CalmRead Lesson Linter

An automated QA tool that validates lesson.json files against:
1. Schema compliance (basic structure)
2. Grapheme constraints (no banned graphemes in decodable content)
3. Sight word validation (only approved sight words used)
4. Calm design principles (no forbidden keywords)

Usage:
    python lesson_linter.py <path_to_lesson.json>
    python lesson_linter.py --all <path_to_lessons_directory>

Author: Manus AI (as Builder/Operator)
Version: 1.0.0
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

# --- Configuration ---

FORBIDDEN_KEYWORDS = [
    # Gamification
    "points", "score", "level up", "unlock", "achievement", "badge", "reward",
    "coins", "stars", "streak", "bonus", "prize", " win ", "winner", "champion",
    # Excitement / Pressure
    "amazing", "awesome", "fantastic", "incredible", "wow", "hurry", "quick",
    "fast", "time's up", "don't miss", "limited time", "special offer",
    # Comparison
    "best", "better than", "beat", "compete", "leaderboard", "rank",
]

REQUIRED_STEP_TYPES = [
    "review",  # Or introduction for lesson 1
    "explicit_phonics",
    "completion"
]

# --- Linter Classes ---

class LintResult:
    """Represents a single lint finding."""
    def __init__(self, severity: str, category: str, message: str, location: str = ""):
        self.severity = severity  # BLOCKER, CRITICAL, MAJOR, MINOR
        self.category = category
        self.message = message
        self.location = location

    def __str__(self):
        loc = f" at {self.location}" if self.location else ""
        return f"[{self.severity}] {self.category}: {self.message}{loc}"


class LessonLinter:
    """Lints a single lesson.json file."""

    def __init__(self, lesson_data: Dict[str, Any]):
        self.lesson = lesson_data
        self.results: List[LintResult] = []
        self.allowed_graphemes = set()
        self.banned_graphemes = set()
        self.sight_words = set()

    def lint(self) -> List[LintResult]:
        """Run all lint checks."""
        self._extract_constraints()
        self._check_required_fields()
        self._check_grapheme_constraints()
        self._check_word_list()
        self._check_decodable_text()
        self._check_calm_design()
        self._check_step_structure()
        return self.results

    def _extract_constraints(self):
        """Extract grapheme and sight word constraints from lesson."""
        constraints = self.lesson.get("graphemeConstraints", {})
        self.allowed_graphemes = set(g.lower() for g in constraints.get("allowedGraphemes", []))
        self.banned_graphemes = set(g.lower() for g in constraints.get("bannedGraphemes", []))
        self.sight_words = set(w.lower() for w in constraints.get("sightWords", []))

    def _check_required_fields(self):
        """Check for required top-level fields."""
        required = ["lessonId", "version", "title", "steps", "graphemeConstraints"]
        for field in required:
            if field not in self.lesson:
                self.results.append(LintResult(
                    "CRITICAL", "Schema", f"Missing required field: {field}"
                ))

    def _check_grapheme_constraints(self):
        """Check that grapheme constraints are properly defined."""
        if not self.allowed_graphemes:
            self.results.append(LintResult(
                "CRITICAL", "Phonics", "allowedGraphemes is empty or missing"
            ))
        if not self.banned_graphemes:
            self.results.append(LintResult(
                "MAJOR", "Phonics", "bannedGraphemes is empty - this may be intentional for advanced lessons"
            ))

    def _segment_word(self, word: str) -> List[str]:
        """Segment a word into graphemes (simple character-by-character for now)."""
        # TODO: Implement proper grapheme segmentation for digraphs, etc.
        return list(word.lower())

    def _validate_word(self, word: str, location: str) -> bool:
        """Validate a single word against grapheme constraints."""
        word_lower = word.lower()
        
        # Check if it's a sight word
        if word_lower in self.sight_words:
            return True
        
        # Segment and check each grapheme
        graphemes = self._segment_word(word)
        for grapheme in graphemes:
            if grapheme in self.banned_graphemes:
                self.results.append(LintResult(
                    "BLOCKER", "Phonics",
                    f"Word '{word}' contains banned grapheme '{grapheme}'",
                    location
                ))
                return False
            if grapheme not in self.allowed_graphemes and grapheme.isalpha():
                self.results.append(LintResult(
                    "BLOCKER", "Phonics",
                    f"Word '{word}' contains grapheme '{grapheme}' not in allowedGraphemes",
                    location
                ))
                return False
        return True

    def _check_word_list(self):
        """Validate all words in the word list."""
        word_list = self.lesson.get("wordList", [])
        if not word_list:
            # Early lessons may not have words
            return

        for i, word_entry in enumerate(word_list):
            word = word_entry.get("word", "")
            self._validate_word(word, f"wordList[{i}]")
            
            # Check grapheme segmentation matches word
            graphemes = word_entry.get("graphemes", [])
            if graphemes:
                reconstructed = "".join(graphemes)
                if reconstructed.lower() != word.lower():
                    self.results.append(LintResult(
                        "MAJOR", "Phonics",
                        f"Word '{word}' grapheme segmentation '{reconstructed}' doesn't match",
                        f"wordList[{i}]"
                    ))

    def _check_decodable_text(self):
        """Validate all words in decodable text passages."""
        decodable = self.lesson.get("decodableText")
        if not decodable:
            return

        sentences = decodable.get("sentences", [])
        for i, sentence in enumerate(sentences):
            text = sentence.get("text", "")
            # Extract words (simple tokenization)
            words = re.findall(r"[a-zA-Z]+", text)
            for word in words:
                self._validate_word(word, f"decodableText.sentences[{i}]")

    def _check_calm_design(self):
        """Check for forbidden keywords that violate calm design."""
        # Check all text content in the lesson
        text_to_check = []
        
        # Collect all text fields
        text_to_check.append(self.lesson.get("title", ""))
        
        for step in self.lesson.get("steps", []):
            text_to_check.append(step.get("title", ""))
            text_to_check.append(step.get("instruction", ""))
            content = step.get("content", {})
            if isinstance(content, dict):
                text_to_check.append(content.get("displayText", ""))
                text_to_check.append(content.get("completionMessage", ""))

        # Check audio transcripts
        for asset in self.lesson.get("audioAssets", []):
            text_to_check.append(asset.get("transcript", ""))

        # Search for forbidden keywords
        full_text = " ".join(text_to_check).lower()
        for keyword in FORBIDDEN_KEYWORDS:
            if keyword.lower() in full_text:
                self.results.append(LintResult(
                    "CRITICAL", "CalmDesign",
                    f"Forbidden keyword found: '{keyword}'"
                ))

    def _check_step_structure(self):
        """Check that required step types are present."""
        steps = self.lesson.get("steps", [])
        step_types = [s.get("type") for s in steps]
        
        # Check for completion step
        if "completion" not in step_types:
            self.results.append(LintResult(
                "CRITICAL", "Structure",
                "Missing 'completion' step - lessons must have a clear ending"
            ))

        # Check first step is introduction or review
        if steps and steps[0].get("type") not in ["introduction", "review"]:
            self.results.append(LintResult(
                "MAJOR", "Structure",
                f"First step should be 'introduction' or 'review', found '{steps[0].get('type')}'"
            ))


def lint_lesson_file(filepath: str) -> Tuple[List[LintResult], bool]:
    """Lint a single lesson file and return results."""
    try:
        with open(filepath, 'r') as f:
            lesson_data = json.load(f)
    except json.JSONDecodeError as e:
        return [LintResult("BLOCKER", "Schema", f"Invalid JSON: {e}")], False
    except FileNotFoundError:
        return [LintResult("BLOCKER", "File", f"File not found: {filepath}")], False

    linter = LessonLinter(lesson_data)
    results = linter.lint()
    
    # Determine pass/fail
    blockers = [r for r in results if r.severity == "BLOCKER"]
    criticals = [r for r in results if r.severity == "CRITICAL"]
    passed = len(blockers) == 0 and len(criticals) == 0
    
    return results, passed


def print_report(filepath: str, results: List[LintResult], passed: bool):
    """Print a formatted lint report."""
    print(f"\n{'='*60}")
    print(f"LINT REPORT: {filepath}")
    print(f"{'='*60}")
    
    if not results:
        print("✓ No issues found!")
    else:
        # Group by severity
        for severity in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR"]:
            severity_results = [r for r in results if r.severity == severity]
            if severity_results:
                print(f"\n{severity} ({len(severity_results)}):")
                for r in severity_results:
                    print(f"  • {r}")
    
    print(f"\n{'='*60}")
    verdict = "✓ PASS" if passed else "✗ FAIL"
    print(f"VERDICT: {verdict}")
    print(f"{'='*60}\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python lesson_linter.py <path_to_lesson.json>")
        print("       python lesson_linter.py --all <path_to_lessons_directory>")
        sys.exit(1)

    if sys.argv[1] == "--all":
        if len(sys.argv) < 3:
            print("Error: Please provide a lessons directory path")
            sys.exit(1)
        
        lessons_dir = Path(sys.argv[2])
        all_passed = True
        
        for lesson_dir in sorted(lessons_dir.iterdir()):
            if lesson_dir.is_dir():
                lesson_file = lesson_dir / "lesson.json"
                if lesson_file.exists():
                    results, passed = lint_lesson_file(str(lesson_file))
                    print_report(str(lesson_file), results, passed)
                    if not passed:
                        all_passed = False
        
        sys.exit(0 if all_passed else 1)
    else:
        filepath = sys.argv[1]
        results, passed = lint_lesson_file(filepath)
        print_report(filepath, results, passed)
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
