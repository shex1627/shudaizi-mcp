# Raising the Bar on SWE-bench Verified
**Date:** January 6, 2025
**URL:** https://www.anthropic.com/engineering/swe-bench-sonnet
**Source:** Web-fetched Feb 2026

---

## Overview

Claude 3.5 Sonnet (upgraded) achieved 49% on SWE-bench Verified, surpassing the prior state-of-the-art of 45%. Demonstrates how effective agent design — combining a model with thoughtfully constructed scaffolding — maximizes coding performance.

## What Is SWE-bench?

- Evaluates models on authentic software engineering tasks from real GitHub issues in Python repos
- Each task: understand code context → make targeted modifications → validate against unit tests
- "Verified" subset: 500 human-reviewed, confirmed-solvable problems
- Measures **entire agent systems**, not isolated models — scaffolding matters hugely

## Agent Architecture

Prioritized minimal, well-designed scaffolding:

- **Bash Tool**: shell command execution with detailed environment constraint instructions
- **Edit Tool**: file viewing, creation, modification via string replacement
- **Flexible Prompt**: outlines suggested steps without rigid workflow constraints

Investment focus: tool interface design — extensive testing to identify misunderstandings, refining descriptions accordingly.

## Results

| Model | Score |
|-------|-------|
| Claude 3.5 Sonnet (new) | **49%** |
| Previous SOTA | 45% |
| Claude 3.5 Sonnet (old) | 33% |
| Claude 3 Opus | 22% |

## Workflow

Model follows exploratory approach:
1. Examine repository structure
2. Reproduce errors through test scripts
3. Modify source code
4. Iterate until tests pass

Improved self-correction compared to earlier versions.

## Challenges

1. **Resource intensity**: successful runs often consumed >100K tokens across hundreds of turns
2. **Grading complexity**: environment setup issues sometimes obscured actual performance
3. **Hidden test limitations**: model can't see final evaluation criteria, sometimes misjudges success
4. **Visual debugging gaps**: lack of image viewing hampered graphics library tasks

## Key Insight

Tool design matters more than prompt optimization for agent performance. The team spent more time refining tool interfaces than the overall system prompt — and this is where the gains came from.

---

## Applicability
- Agent scaffolding design
- Tool interface optimization
- Benchmark methodology
- Agentic coding system architecture
