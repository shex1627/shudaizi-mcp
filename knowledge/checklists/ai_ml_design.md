---
task: ai_ml_design
description: Design AI/ML systems, LLM applications, or agent architectures
primary_sources: ["09", "10", "11"]
secondary_sources: ["01", "08"]
anthropic_articles: ["a01", "a02", "a03", "a04", "a05", "a06", "a07", "a08", "a09", "a10"]
version: 1
updated: 2026-02-22
---

# AI/ML System Design Checklist

## Phase 1: Problem Framing & Approach Selection

- [ ] Confirm the task actually benefits from AI/ML — rule-based or deterministic approaches may suffice [09]
- [ ] Align the ML objective function with the business metric — optimizing the wrong proxy (e.g., CTR instead of satisfaction) causes systemic harm [10]
- [ ] Apply the Prompt-RAG-Finetune decision ladder: start with prompting, escalate to RAG only when external knowledge is needed, fine-tune only when behavior must change [09]
- [ ] Use the simplest viable pattern: single LLM call before workflow, workflow before autonomous agent [a01]
- [ ] For agent architectures, select the right workflow pattern — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, or autonomous agent — based on task structure [a01]
- [ ] Define evaluation criteria and build evals before building the feature — eval-driven development is the AI equivalent of TDD [09]

## Phase 2: Data & Context Architecture

- [ ] Treat data quality as the primary bottleneck — more effort on data curation than model architecture [10][09]
- [ ] Design for natural labels where possible — structure product interactions so user behavior implicitly labels predictions [10]
- [ ] For RAG systems, choose chunking strategy based on retrieval precision needs: fixed-size, semantic, or document-structure-aware [09][11]
- [ ] Evaluate retrieval and generation separately — retrieval quality is the ceiling for RAG quality [09]
- [ ] Implement hybrid search (dense vector + sparse keyword) for better retrieval coverage [09][11]
- [ ] Curate context for signal density: the smallest set of high-signal tokens, not maximum context stuffing [a05]
- [ ] For long-horizon tasks, choose a context management strategy: compaction, structured note-taking, or sub-agent architectures [a05]
- [ ] Validate documents before ingestion into vector stores — poisoned documents enable indirect prompt injection [08]
- [ ] Verify the data model matches access patterns: relational for joins, document for aggregates, graph for relationships [01]

## Phase 3: Model & Pipeline Design

- [ ] Design the system as a compound AI system with multiple steps: retrieval, re-ranking, prompt assembly, LLM call, output parsing, validation, fallback [09]
- [ ] Separate the Feature Pipeline (data collection, chunking, embedding), Training Pipeline (fine-tuning, evaluation), and Inference Pipeline (retrieval, generation, serving) [11]
- [ ] Treat the model as a component, not the product — design for model-portability from day one [09]
- [ ] For fine-tuning, verify the decision is justified: consistent style requirements, domain-specific reasoning, or cost reduction via smaller models [09][11]
- [ ] Implement model routing — direct simple queries to smaller/cheaper models, complex queries to larger ones [09]
- [ ] For agent systems, design tools that are self-contained, unambiguous, and have minimal overlap [a06][a05]
- [ ] Use prompt-engineered tool descriptions — tool descriptions directly steer agent behavior [a06]

## Phase 4: Security & Trust Boundaries

- [ ] Treat the LLM as sitting on a trust boundary, not inside your trust zone — output is adversary-influenceable [08]
- [ ] Treat all LLM output as untrusted: validate before passing to SQL, shell, HTML, APIs, or file operations [08]
- [ ] Implement defense in depth: input filtering, system prompt hardening, output validation, privilege restriction, and monitoring [08]
- [ ] Apply principle of least privilege for tool-using LLMs — the blast radius of a compromised agent equals its permissions [08]
- [ ] Require human-in-the-loop approval for destructive or irreversible actions [08][a01]
- [ ] Implement access controls on the RAG retrieval layer — users should only retrieve documents they are authorized to see [08]
- [ ] Pin model versions in production; verify model provenance when downloading from registries [08]

## Phase 5: Evaluation & Monitoring

- [ ] Build a multi-level eval framework: programmatic evals, heuristic checks, LLM-as-judge, and human evaluation [09]
- [ ] Separate capability evals (can it do the task?), quality evals (how well?), and safety evals (does it avoid harm?) [09]
- [ ] Maintain versioned eval datasets (golden datasets) alongside code — track metrics over time for regression detection [09]
- [ ] Implement four-layer monitoring: operational metrics, ML-specific metrics, business metrics, and data quality metrics [10]
- [ ] Monitor for distribution shift: covariate shift, label shift, and concept drift using statistical tests [10]
- [ ] Log every step of compound AI systems for observability — debug non-deterministic multi-step executions [09][a02]
- [ ] Set cost controls for agentic systems: step limits, budget caps, and timeouts to prevent runaway agent interactions [09]

## Phase 6: Production Readiness

- [ ] Implement inference optimization: KV-cache management, quantization, batching, and semantic caching [09][11]
- [ ] Design for the "demo to production" gap: real users type differently, edge cases multiply, scale requirements emerge [09]
- [ ] Implement graceful degradation — define fallback behavior when the LLM is slow, down, or returns garbage [09]
- [ ] For long-running agents, solve the shift-change problem: structured progress files, one-feature-per-session focus, git checkpoints [a04]
- [ ] Use resume-from-checkpoint rather than restarting failed agents [a02]
- [ ] Implement rainbow deployments for agentic systems — gradual traffic shifts prevent disrupting long-running agents [a02]

---

## Key Questions to Ask

1. "What is the simplest approach that could work — prompting, RAG, fine-tuning, or agent?" — Escalate only when evals prove the simpler approach is insufficient [09]
2. "What happens when the LLM returns wrong, slow, or adversarial output?" — Every LLM call is an opportunity for the system to fail [09][08]
3. "Can we evaluate this? How will we know if it got better or worse?" — If you cannot measure it, you cannot improve it [09]
4. "What is the cost per request, and what happens if an agent loops?" — Multi-step agents can make hundreds of LLM calls; budget accordingly [09][a02]
5. "Is retrieval quality high enough? If not, no amount of generation tuning will help." — Diagnose retrieval before generation [09]
6. "Where are the trust boundaries? What can the LLM access if fully compromised?" — Map the blast radius of prompt injection [08]
7. "Does the team have the operational maturity for this level of complexity?" — Self-hosted models, multi-agent systems, and custom fine-tuning each require significant infrastructure [11][10]
8. "Are we designing tools as if we were designing a UI for the agent?" — Agent-computer interface design deserves the same rigor as human-computer interface design [a01][a06]

---

## Anti-Patterns to Flag

| Anti-Pattern | Signal | Source |
|---|---|---|
| **Eval debt** | Shipping LLM features without automated evaluation — regressions go undetected | [09] |
| **Premature complexity** | Building RAG pipelines or fine-tuning before exhausting what good prompting can do | [09][a01] |
| **Context stuffing** | Filling the context window with everything available instead of curating for signal density | [a05] |
| **Tool sprawl** | Dozens of overlapping tools that confuse the agent and waste context tokens | [a06][a07] |
| **Trusted LLM output** | Passing LLM output directly to SQL, shell, eval(), or innerHTML without validation | [08] |
| **Excessive agency** | Granting broad permissions without matching security controls — the highest-impact incident type | [08] |
| **Model marriage** | Building product identity around a specific model instead of designing for model-portability | [09] |
| **Over-ambitious agents** | Agents attempting everything in one session, exhausting context mid-task | [a04] |
| **Ignoring retrieval quality** | Tuning generation when the real problem is retrieving wrong or irrelevant documents | [09][11] |
| **Silent ML degradation** | No monitoring for distribution shift or prediction quality — models degrade invisibly | [10] |
| **Demo-quality shipping** | Assuming demo performance predicts production performance across real user inputs | [09] |
| **Feedback loop blindness** | Not asking whether the model's output influences its future training data | [10] |
