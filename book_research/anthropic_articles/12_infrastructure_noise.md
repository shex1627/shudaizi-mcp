# Quantifying Infrastructure Noise in Agentic Coding Evals
**Date:** February 2026
**URL:** https://www.anthropic.com/engineering/infrastructure-noise
**Source:** Web-fetched Feb 2026

---

## Core Finding

Infrastructure configuration alone can produce **6 percentage point differences** on benchmarks — often exceeding leaderboard margins between top models.

## The Problem

- Static benchmarks score model output directly — runtime doesn't factor in
- Agentic coding evaluations are different: the runtime is "an integral component of the problem-solving process"
- Resource allocation becomes a hidden variable affecting results
- Different models favor different strategies (heavyweight dependencies vs. minimal implementations)

## Research Findings

Testing six configurations from strict (1x specs) to uncapped resources:

| Metric | Tight Config | Uncapped Config |
|--------|-------------|-----------------|
| Infrastructure errors | 5.8% | 0.5% |
| Total score impact | — | +6 percentage points |

**Critical threshold**: ~3x resource multiplier, where "additional resources start actively helping the agent solve problems it couldn't solve before."

## Why It Matters

Resource limits effectively change **what the benchmark measures** rather than purely assessing model capability. A model that installs heavyweight dependencies may fail under tight limits but succeed with more resources — and vice versa.

## Recommendations

1. **Specify dual parameters**: guaranteed allocation + hard kill thresholds (not single resource values)
2. **Calibrate with headroom**: ~3x baseline specs eliminates transient failure spikes while maintaining meaningful constraints
3. **Document methodology**: publish enforcement details alongside scores
4. **Apply skepticism**: leaderboard differences below 3% warrant scrutiny without transparent configuration

## Key Quotable

> "A few-point lead might signal a real capability gap—or it might just be a bigger VM."

> "Leaderboard differences below 3 percentage points deserve skepticism until the eval configuration is documented and matched."

---

## Applicability
- Benchmark design and interpretation
- Infrastructure configuration for AI evals
- Leaderboard analysis
- Reproducible evaluation methodology
