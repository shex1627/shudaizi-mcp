# Designing AI-Resistant Technical Evaluations
**Date:** January 21, 2026
**URL:** https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
**Source:** Web-fetched Feb 2026

---

## Core Problem

Anthropic's performance engineering take-home required 3 redesigns since early 2024 because successive Claude models defeated each iteration. "Each new Claude model has forced us to redesign the test."

## Version 1: Original Design

Python simulator for a fake accelerator resembling TPUs. Candidates optimize code for a parallel tree traversal, progressing through:
- Serial implementations
- Multicore parallelism
- SIMD vectorization
- VLIW instruction packing

Design principles:
- Representative of actual performance engineering work
- High signal with many demonstration opportunities
- No specialized domain knowledge required
- Genuinely engaging

Successfully hired dozens of engineers over 18 months from ~1,000 candidates.

## Version 2: Claude Opus 4 Breaks It

Opus 4 outperformed most human applicants within the time limit. Solution:
- Used Claude itself to identify where the model struggled
- Reset problem's starting point at the struggle point
- Eliminated multicore optimization
- Added new machine features
- Shortened time from 4 to 2 hours

## Version 3: Claude Opus 4.5 Breaks It Again

Opus 4.5 systematically solved Version 2 within 90 minutes. When told achievable cycle counts, it discovered clever workarounds for memory bandwidth bottlenecks that most humans couldn't identify.

## Version 4: Novelty Over Realism

Embraced constraint puzzles inspired by Zachtronics games:
- Deliberately unusual instruction set
- Requires creative, nonconventional programming
- Trades "the realism and varied depth of the original" for out-of-distribution problems

## Key Findings

| Problem Type | AI Resistance | Realism |
|-------------|--------------|---------|
| Knowledge-based | Fails fastest (sufficient training data) | High |
| Realistic work | Falls quickly as models improve | High |
| Out-of-distribution | Persists longer | Low |
| Novel constraint puzzles | Most resistant | Low |

- Human advantage persists at **unlimited time horizons** on **novel** problems
- **Prioritize novelty over realism** for AI-resistant design
- Include multiple independent sub-problems

## The Fundamental Tension

> "The original worked because it resembled real work. The replacement works because it simulates novel work."

Banning AI assistance contradicts real-world work conditions, yet raising the bar to "substantially outperform Claude" risks making evaluations unhelpfully difficult.

## Key Quotable

> "It's always been hard to design interviews that represent the job, but now it's harder than ever."

---

## Applicability
- Technical hiring evaluation design
- AI capability benchmarking
- Assessment methodology in the age of AI
- Understanding AI vs. human cognitive strengths
