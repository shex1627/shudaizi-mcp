# A Postmortem of Three Recent Issues
**Date:** September 17, 2025
**URL:** https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
**Source:** Web-fetched Feb 2026

---

## Overview

Three overlapping infrastructure bugs between August-September 2025 caused intermittent Claude response degradation. Anthropic states: "We never reduce model quality due to demand, time of day, or server load."

## The Three Issues

### 1. Context Window Routing Error (Aug 5 – Sep 18)
- Requests incorrectly sent to servers configured for 1M token context window
- Initial impact: 0.8% of Sonnet 4 requests
- Load balancing adjustment on Aug 29 worsened to **16%** by Aug 31
- ~30% of Claude Code users experienced at least one misrouted message

### 2. Output Corruption (Aug 25 – Sep 2)
- TPU server misconfiguration caused token generation errors
- System occasionally assigned high probability to wrong tokens
- Symptoms: Thai/Chinese characters in English responses, syntax errors in code
- Affected Opus and Sonnet models before rollback

### 3. XLA Compiler Bug (Aug 25 – Sep 12)
- Token selection code change exposed deeper compiler issue
- **Root cause**: Mixed precision arithmetic — operations in bf16 (16-bit) vs. fp32 (32-bit) disagreed on token rankings
- "Approximate top-k" bug sometimes returned completely wrong results for specific configurations
- Only certain batch sizes triggered failures — extremely hard to diagnose

## Why Detection Was Hard

- **Eval gaps**: "The evaluations we ran simply didn't capture the degradation users were reporting"
- **Privacy constraints**: Prevented engineer access to unreported user interactions
- **Overlapping symptoms**: Three bugs produced "different symptoms on different platforms at different rates"
- **Noisy baselines**: Confusing, contradictory reports that appeared random

## Lessons & Organizational Changes

1. **More sensitive evals** differentiating working vs. broken implementations
2. **Continuous production monitoring** — not just pre-deployment testing
3. **Better debugging infrastructure** for community feedback while protecting privacy
4. **User feedback integration** — user reports proved crucial; patterns across use cases helped isolate root causes

## Key Insight

Pre-deployment testing is necessary but insufficient. Production monitoring and user feedback loops are essential for catching issues that evals miss.

---

## Applicability
- Production incident management
- Evaluation design gaps
- ML infrastructure debugging
- User feedback integration patterns
