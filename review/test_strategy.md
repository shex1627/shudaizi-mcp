# Test Strategy Review

**Frameworks applied:** [12] Unit Testing (Khorikov), [13] GOOS, [34] LLM-as-Judge Evaluation
**Checklist source:** knowledge/checklists/test_strategy.md
**Verdict: Good** — The 3-level test architecture is sound and correctly designed. The eval system (LLM-as-judge with Pass@k) is the right framework for this kind of tool. Gaps: write tool error cases untested, activation fixture set is thin, reliability (Pass^k) metrics not collected in practice.

---

## Test Architecture Overview

```
Level 1: Structural Integrity       (pytest, no LLM)
  test_level1_integrity.py
  — File existence, JSON validity, cross-reference resolution,
    checklist frontmatter parsing, skill file validation

Level 2: MCP Protocol               (pytest, no LLM, uses real MCP transport)
  test_level2_mcp_protocol.py
  — Tool listing, schema validation, read tool dispatch,
    write tool dispatch, error handling

Level 3: LLM Evaluation             (requires ANTHROPIC_API_KEY)
  run_llm_eval.py + test_level3a_eval.py
  — 27 eval fixtures, LLM-as-judge grading,
    Pass@k (capability) and Pass^k (reliability),
    A/B comparison (with checklist vs. without)
```

The three-level separation is architecturally correct:
- L1 catches structural regressions (broken links, malformed JSON) without LLM cost
- L2 catches integration regressions (MCP protocol, tool dispatch) without LLM cost
- L3 measures actual effectiveness (does the knowledge delivery improve model output?)

---

## Level 1: Structural Integrity

**What it tests:**
- All book research files referenced in `book_index.json` exist on disk
- All routing task types reference valid book IDs that exist in `book_index.json`
- All checklist files parse their frontmatter correctly
- All skill SKILL.md files exist and have valid frontmatter
- JSON files are syntactically valid

**Assessment:** This level is the most important regression safety net. A broken cross-reference (routing.json pointing to a nonexistent book_id) would cause silent `BookNotFound` responses in production. L1 catches this without any LLM cost. ✓

**Coverage gap:** L1 currently validates that referenced book files *exist* but does not validate that referenced book IDs *can be loaded by the SECTION_PATTERNS regex*. A book file with non-standard headings would pass L1 but fail at runtime with "Section not found." [12]

**Coverage gap:** L1 does not validate that checklist frontmatter `primary_sources` and `secondary_sources` lists match `routing.json`. This means the frontmatter drift identified in `knowledge_quality.md` would not be caught automatically.

**Recommendation:** Add two additional L1 checks:
1. For each book ID in routing.json, attempt to extract at least one section via `extract_section` and assert it is non-None
2. For each checklist, assert that frontmatter `primary_sources` matches routing.json's primary_sources for that task type

---

## Level 2: MCP Protocol

**What it tests:**
- Tool listing returns the expected 5 tools
- Each tool has a valid input schema
- Read tools dispatch correctly and return non-empty content
- Write tools dispatch and update the knowledge base
- Unknown tool name returns an error response

**Assessment:** L2 is the integration layer that catches MCP protocol regressions. Testing through the actual MCP transport (not just calling the Python functions directly) is the right approach — it catches encoding, serialization, and transport issues. ✓

**Coverage gap:** L2 tests the *happy path* for write tools. There are no tests for:
- `add_knowledge_source` with a duplicate title (what happens to routing.json?)
- `add_knowledge_source` with an empty `task_types` list (does routing get updated?)
- `update_checklist` with a nonexistent section in `replace_section` (does it create the section? fail silently?)
- `update_checklist` with a malformed content string
- Two concurrent write tool calls (race condition on JSON files)

Given that write tools mutate shared state (the knowledge base), test coverage for error paths is more important here than for read tools. [12]

**Coverage gap:** L2 does not test the `focus` filtering in `get_task_checklist`. The filter_by_focus logic has a fallback ("No sections matching focus found — returning full checklist") but this fallback is not tested.

**Recommendation:** Add error-case L2 tests for write tools and focus filtering edge cases.

---

## Level 3: LLM Evaluation

### Fixture Set Assessment

**27 fixtures across 4 tiers:**

| Tier | Count | Purpose | Assessment |
|------|-------|---------|-----------|
| A — Obvious bugs | 8 | Regression: model without checklist should catch these | Appropriate count for regression tier |
| B — Structural smells | 4 | Primary value: checklists add detection capability here | **Thin** — 4 fixtures for the core value proposition |
| Activation | 4 | Does the model invoke tools proactively? | **Very thin** — 4 scenarios for proactive behavior |
| Qualitative | 3 | Open-ended reasoning quality | Appropriate |

**Tier B is the most important and least covered.** These are the fixtures that test the core claim: "checklists from the knowledge base help the model catch issues it would otherwise miss." 4 fixtures is not enough to have statistical confidence in the A/B comparison results.

**Activation fixtures are particularly thin.** The 4 activation scenarios (`activation_arch_gateway`, `activation_code_review_async`, `activation_security_auth`, `activation_test_design`) test that the model proactively invokes tools. This is the fundamental usefulness claim of the tool: that agents will call `get_task_checklist` without being prompted to. More activation scenarios, across more task types, would give more confidence in this behavior.

### Pass@k vs. Pass^k [34]

The eval system computes both:
- **Pass@k (capability)**: At least one of k runs detects the issue → measures maximum capability
- **Pass^k (reliability)**: All k of k runs detect the issue → measures consistency

**Assessment:** Implementing both metrics is the correct design [34]. However, the practical question is: what value of k is used? If k=1 (single run), Pass@1 and Pass^1 are identical and tell you nothing about reliability. The value of Pass^k becomes meaningful only with k ≥ 3.

The README says "Computes Pass@k (capability) and Pass^k (reliability)" but does not specify the default k value. If k=1 is the default, the reliability metric is not being used.

**Recommendation:** Run eval with k=3 as the default for reliability measurement. Document the k value in the README and report both metrics side by side in the eval output.

### A/B Comparison Design

The A/B comparison (with checklist vs. without) is the most valuable eval: it directly measures whether the knowledge delivery improves model output. This is correctly implemented as the `--compare` flag in `run_llm_eval.py`. ✓

**Concern:** The A/B comparison is not run automatically — it requires `--compare` to be specified. The nightly/CI run should always include the A/B comparison for Tier B fixtures, since those are the primary signal for the tool's core value. [13]

### LLM-as-Judge Quality [34]

The `llm_judge.py` grader evaluates responses against the seeded issue. Key concerns for judge quality:

**Position bias:** Is the judge equally likely to identify a found vs. not-found issue regardless of where in the response it appears? The grader should explicitly instruct the judge to look at the entire response, not just the first few sentences. [34]

**Verbosity bias:** The judge may rate more verbose responses higher regardless of correctness. Explicitly instructing the judge to evaluate accuracy over comprehensiveness mitigates this. [34]

**Self-serving bias:** The judge in the comparison condition has seen the checklist. If the judge model is the same as the response model, it may be biased toward responses that follow the checklist format. Using a different model for judging than for evaluation mitigates this. [34]

These concerns are documented in the PROACTIVE_TESTING_RESEARCH.md in the tests directory but it's worth confirming the implementation handles them.

---

## Test Philosophy Assessment [12]

Applying Khorikov's unit testing principles:

**What are the tests testing?**
- L1: Structural contracts (file existence, JSON validity, cross-references)
- L2: Integration behavior (MCP protocol, tool dispatch, response format)
- L3: Observable business value (does the tool make models better?)

This is the correct pyramid: L1 and L2 are fast, deterministic, run frequently; L3 is slow, non-deterministic, run less frequently but measures actual value. ✓

**Are tests testing observable behavior, not implementation details?**
L1 and L2 could be implemented to test internal Python functions (BookLoader methods, KnowledgeManager methods) rather than the end-to-end behavior. Testing through the MCP protocol (L2) is the right choice — it tests the system as the agent sees it. ✓

**Do tests have a clear failure mode signal?**
L1 and L2 failures are deterministic and easy to diagnose. L3 failures are probabilistic (a model may correctly catch an issue by chance even without the checklist). The Pass@k metric handles this — a single failure at k=1 is not conclusive, but consistent failure at k=3 is. ✓

**Are tests maintainable?**
Adding a new book to the knowledge base requires: (1) L1 tests to verify the file is indexed and cross-references resolve, and (2) L3 fixtures to test that checklist items from the new book are detectable. Currently, step (2) is not done for books 35-40. New books should come with at least one new eval fixture for their most distinctive concept. [12]

---

## GOOS Principles [13]

Growing Object-Oriented Software Guided by Tests applied to the knowledge system:

**"Only mock types you own":** The L3 eval correctly tests against the real Claude API rather than mocking it. Mocking the LLM would make the test circular (the mock would always behave "correctly"). ✓

**"Listen to the tests":** The activation fixtures reveal whether the tool descriptions are good enough for models to invoke the tools proactively. If activation pass rates are low, this is signal that tool descriptions need improvement — not that the tests are wrong. The tests are giving design feedback. ✓

**"End-to-end tests for integration":** The L2 tests running through the actual MCP transport (not just calling Python directly) are the end-to-end integration tests. ✓

---

## Summary

| Aspect | Status | Priority |
|--------|--------|----------|
| L1: structural integrity | ✓ Good | — |
| L2: MCP protocol happy path | ✓ Good | — |
| L2: write tool error paths | ✗ Missing | **High** |
| L2: focus filter edge cases | ✗ Missing | Medium |
| L3: fixture count for Tier B | ⚠ Thin (4) | **High** |
| L3: activation fixture count | ⚠ Very thin (4) | High |
| L3: k value for Pass^k | ⚠ Unclear | Medium |
| L3: A/B comparison in CI | ⚠ Not automated | Medium |
| L1: section loading validation | ✗ Missing | Medium |
| L1: frontmatter/routing sync | ✗ Missing | Medium |
| New book → new fixture workflow | ✗ No documented process | Low |
