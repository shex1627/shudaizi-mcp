# Testing & Evaluation Guide

## Quick Start

```bash
# Run all deterministic tests (L1 + L2 + L3A) — no API key needed
pytest tests/ -v

# Run LLM eval with A/B comparison — requires ANTHROPIC_API_KEY in .env
python tests/run_llm_eval.py --compare
```

## Three Test Levels

### Level 1: Structural Integrity (`test_level1_integrity.py`)

Validates the knowledge system's files, references, and data consistency. Catches broken file paths, invalid JSON, missing checklists, and content quality regressions.

| Test Class | What it checks |
|---|---|
| `TestFileIntegrity` | Every file referenced in `book_index.json` and `routing.json` exists on disk |
| `TestCrossReferences` | All source IDs in routing resolve, skills match checklists, citation IDs are valid |
| `TestBookLoader` | All 16 checklists load at all 3 detail levels, all 33 books + 21 articles parse |
| `TestTaskRouter` | Task listing, book/article lookup, reload, format methods |
| `TestKnowledgeManager` | Write operations (add source, update checklist) on a temp copy |
| `TestContentQuality` | Frontmatter present, sufficient checklist items, all items cite sources, books have key sections |

**When to run**: After editing any checklist, book research file, `routing.json`, or `book_index.json`.

### Level 2: MCP Protocol (`test_level2_mcp_protocol.py`)

Tests the MCP server through the actual protocol layer — tool schemas, dispatch, response formats.

| Test Class | What it checks |
|---|---|
| `TestToolListing` | 5 tools registered, correct names, valid schemas, required fields |
| `TestReadToolCalls` | All 3 read tools return correct `TextContent`, detail level ordering, focus filtering |
| `TestToolDispatch` | Unknown tool handling, exhaustive calls to all 16 tasks / 33 books / 21 articles |

**When to run**: After editing any file in `mcp_server/src/`.

### Level 3A: Checklist Coverage Eval (`test_level3a_eval.py` + `run_llm_eval.py`)

Evaluates whether shudaizi checklists help agents catch known issues in code. Two components:

1. **Deterministic pytest suite** (`test_level3a_eval.py`) — verifies checklists contain the right keywords to guide an agent toward each seeded issue. No LLM needed.

2. **LLM eval script** (`run_llm_eval.py`) — sends code + checklist to Claude, grades whether the response identifies the seeded issue, computes pass@k and pass^k across multiple trials.

**When to run**: After adding/modifying checklists or eval fixtures.

## Eval Fixtures

Each fixture is a directory in `tests/eval_fixtures/` containing:
- A code file (`code.py`, `code.js`, etc.) with a seeded issue
- A `ground_truth.json` defining what should be found

### Fixture Tiers

Fixtures are categorized by detection difficulty — how much domain knowledge the model needs beyond common sense.

#### Tier A: Obvious Bugs

Issues the model catches reliably **without** a checklist. These serve as regression tests — if they start failing, something is fundamentally wrong.

| Fixture | Task Type | Issue |
|---|---|---|
| `security_sql_injection` | security_audit | f-string SQL query — textbook OWASP vulnerability |
| `security_plaintext_password` | security_audit | Password stored without hashing — every tutorial covers this |
| `security_idor` | security_audit | No ownership check on resource access — standard OWASP Top 10 |
| `security_llm_innerhtml` | security_audit | LLM output piped to innerHTML — well-known XSS vector |
| `code_review_blocking_async` | code_review | `requests.get()` inside `async def` — common Python gotcha |
| `code_review_cqs_violation` | code_review | Function mutates state AND returns value — widely taught principle |
| `arch_missing_timeout` | architecture_review | HTTP client with no timeout — standard reliability advice |
| `arch_naive_retry` | architecture_review | Retry loop with no backoff — common interview topic |

**How to identify**: Run `--compare` — if baseline pass^k is 100%, it's Tier A.

#### Tier B: Structural Smells

Issues that require **book-level knowledge** or specific named concepts. The model catches these inconsistently without a checklist but reliably with one. **This is where shudaizi proves its value.**

| Fixture | Task Type | Issue | Source Concept |
|---|---|---|---|
| `code_review_shallow_module` | code_review | Three-layer pass-through wrappers adding no logic | "Deep modules" — Philosophy of SW Design [06] |
| `code_review_info_leakage` | code_review | Same date-parsing logic duplicated in 3 modules | "Information leakage" — Philosophy of SW Design [06] |
| `arch_shared_database` | architecture_review | Two services sharing one DB, querying each other's tables | "Distributed monolith" — SW Architecture: Hard Parts [03] |
| `arch_unbounded_query` | architecture_review | Every query fetches full result sets, no LIMIT/pagination | Unbounded queries — DDIA [01] |

**How to identify**: Run `--compare` — if baseline shows any FAIL trials while the checklist version is 100%, it's Tier B.

#### Proactive Fixtures (Tier B variant)

These fixtures test whether the checklist helps the agent **write better code**, not just review existing code. Instead of a `code.py` with a seeded bug, they contain a `prompt.md` with a code-writing task. The ground truth keywords check the *generated* code for expected patterns.

| Fixture | Task Type | What Should Be Generated | Source Concept |
|---|---|---|---|
| `code_review_proactive_sequential_io` | code_review | Concurrent execution of 3 independent API calls + timeouts | Phase 8: Implementation Patterns [22] |

Proactive fixtures use `"eval_mode": "proactive"` in `ground_truth.json`. The LLM eval script automatically switches to a generation prompt ("write production code") instead of a review prompt.

#### Tier C: Multi-File Architecture (not yet built)

Issues requiring cross-file context and architectural reasoning: temporal decomposition, architecture sinkholes, missing fitness functions. These would need multi-file fixtures and are the next frontier.

### Adding a New Fixture

1. Create a directory in `tests/eval_fixtures/`:
   ```
   # Reactive fixture (review existing code):
   tests/eval_fixtures/my_new_fixture/
     code.py              # Code sample with a seeded issue
     ground_truth.json    # Expected findings

   # Proactive fixture (test code generation):
   tests/eval_fixtures/my_proactive_fixture/
     prompt.md            # Code-writing task description
     ground_truth.json    # Expected patterns in generated code
   ```

2. Define `ground_truth.json`:
   ```json
   {
     "task_type": "code_review",
     "detail_level": "standard",
     "focus": "",
     "eval_mode": "reactive",
     "description": "Human-readable description of the seeded issue.",
     "expected_findings": [
       {
         "id": "finding_name",
         "keywords": ["keyword1", "keyword2", "keyword3"]
       }
     ],
     "false_positive_keywords": []
   }
   ```

   For proactive fixtures, set `"eval_mode": "proactive"`. The LLM eval will use a generation prompt instead of a review prompt.

3. Run deterministic tests first:
   ```bash
   pytest tests/test_level3a_eval.py -v -k my_new_fixture
   ```

4. Then run LLM eval:
   ```bash
   python tests/run_llm_eval.py --fixture my_new_fixture --compare
   ```

**Ground truth guidelines** (from [a11] Demystifying Evals):
- Each finding needs **at least 2 keywords** — a single keyword is too brittle
- Keywords should be partial stems where possible (`"sanitiz"` matches "sanitize", "sanitization", "sanitized")
- The task should be **unambiguous** — two experts should agree on pass/fail
- Favor **outcome keywords** over path keywords — check whether the issue was identified, not which specific term was used

## LLM Eval Script

```bash
# Default: 3 trials per fixture, Sonnet
python tests/run_llm_eval.py

# A/B comparison — the most useful mode
python tests/run_llm_eval.py --compare

# More trials for statistical significance
python tests/run_llm_eval.py --compare --trials 5

# Single fixture
python tests/run_llm_eval.py --fixture code_review_shallow_module --compare --trials 10

# Different model
python tests/run_llm_eval.py --model claude-haiku-4-5-20251001 --compare

# Baseline only (no checklist)
python tests/run_llm_eval.py --no-checklist
```

### Interpreting Results

The script reports two metrics per fixture (from [a11] Demystifying Evals):

| Metric | Measures | Formula |
|---|---|---|
| **Pass@k** | Capability — "can it do this at all?" | P(at least 1 success in k trials) |
| **Pass^k** | Reliability — "can it do this every time?" | P(all k trials succeed) |

**Example**: 75% per-trial rate with k=3:
- Pass@3 = 98% (almost certainly catches it at least once)
- Pass^3 = 42% (only consistent less than half the time)

**What to look for in `--compare` output:**
- **Delta = 0%** on a fixture → Tier A (saturated). The checklist doesn't help because the model already knows this.
- **Delta > 0%** → Tier B. The checklist is adding value. The higher the delta, the more the checklist matters.
- **Delta < 0%** → The checklist might be introducing noise or the sample size is too small. Run with `--trials 10` to verify.

### Saturation and Fixture Lifecycle

Per [a11]: "Monitor saturation — refresh capability evals, retire saturated tasks to regression suites."

- When a Tier B fixture reaches 100% pass^k **without** a checklist across 10+ trials, it has been **saturated** — the model has internalized this knowledge. Reclassify it as Tier A.
- When all fixtures are saturated, add harder ones (Tier C) or the eval loses diagnostic value.
- Keep Tier A fixtures as regression tests — they're cheap to run and catch fundamental breakage.
