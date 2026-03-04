# Knowledge Base Quality Review

**Frameworks applied:** [37] Pyramid Principle (structure quality), [40] Working Backwards (customer value), [29] Inspired (opportunity assessment), [34] LLM-as-Judge (evaluation methodology)
**Verdict: Strong** — Broad, well-curated coverage across 40 books and 21 articles. The research files are consistently structured and citation-quality. Six critical gaps: (1) checklists not updated for books 35-40, (2) some task types thin on primary sources, (3) freshness dates not maintained, (4) some checklist frontmatter stale relative to routing.json.

---

## Coverage Assessment

### Domain Coverage Map

| Domain | Books | Primary Coverage | Gap Assessment |
|--------|-------|-----------------|----------------|
| Architecture & System Design | 01, 02, 03, 04, 05, 06, 36, 38 | Excellent — DDIA + Clean Arch + Hard Parts + DDD + EIP | No major gaps |
| Security | 07, 08, 39 | Good — Web Hacker's Handbook + LLM Security + Threat Modeling | No major gaps for current scope |
| AI/ML Engineering | 09, 10, 11, 33, a01-a21 | Excellent — strongest domain; 21 Anthropic articles | Well-covered |
| Testing | 12, 13, 34 | Good — Unit Testing + GOOS + LLM-as-Judge | Missing: integration testing, property-based testing |
| Code Quality | 14, 15, 16 | Good — Pragmatic Programmer + Clean Code + Refactoring | Missing: Working Effectively with Legacy Code |
| Operations & Reliability | 17, 18, 19, 32 | Excellent — Release It! + Observability + SRE + DevOps | No major gaps |
| API & Data | 20, 21, 22 | Good — API Design Patterns + DB Internals + Python Concurrency | Thin: only 1 primary for api_design |
| UX & Design | 23, 24, 25 | Good — DOET + Don't Make Me Think + Laws of UX | Adequate for current scope |
| Data Visualization | 26, 27, 28 | Good — 3 dedicated books | Niche; adequate |
| Product & Process | 29, 30, 31, 35, 40 | Strong — Inspired + Shape Up + Cont. Discovery + Agenda Mover + Working Backwards | Well-rounded |
| Technical Communication | 37 | Good — Pyramid Principle is the canonical text | Only one book; adequate |
| Leadership/Org | 35 | Adequate — Agenda Mover covers execution | Missing: Team Topologies, Accelerate |

### Task Type Coverage Depth

| Task Type | Primary Sources | Assessment |
|-----------|----------------|------------|
| `architecture_review` | 01, 02, 03, 04, 05, 06, 36 | Excellent — 7 primary sources |
| `security_audit` | 07, 08, 39 | Good — 3 primary sources; STRIDE and LLM attack surface covered |
| `ai_ml_design` | 09, 10, 11 | Good — 3 primary + 21 Anthropic articles |
| `agent_design` | 33 | **Thin** — only 1 primary source despite 21 Anthropic articles in secondary |
| `api_design` | 20 | **Thin** — only 1 primary source; API Design Patterns is solid but singular |
| `code_review` | 06, 14, 15, 16 | Good — 4 primary sources |
| `test_strategy` | 12, 13 | Adequate — 2 primary; Unit Testing + GOOS are the right books |
| `refactoring` | 16, 06, 15 | Adequate — 3 primary |
| `feature_design` | 06, 29, 30, 31, 36, 40 | Excellent — 6 primary sources including DDD + Working Backwards |
| `product_doc` | 29, 30, 31, 37, 40 | Excellent — 5 primary sources |
| `observability` | 18, 17, 19 | Good — 3 primary |
| `devops` | 32, 17, 19 | Good — 3 primary |
| `ux_review` | 23, 24, 25 | Good — 3 dedicated UX books |
| `data_viz_review` | 26, 27, 28 | Good — 3 dedicated visualization books |
| `presentation` | 26, 37 | Adequate — 2 primary |
| `bug_fix` | 16, 14, 17 | Adequate — 3 primary |

**Critical gaps:**
- `agent_design` has 1 primary source (book 33) and 21 Anthropic articles in secondary. The Anthropic articles (a01-a10) are arguably more primary than secondary for agent design. The routing treats them asymmetrically.
- `api_design` depends on a single primary source (book 20). Adding a second primary (e.g., a REST API design book, or promoting EIP [38] or DDD [36] to primary status for API design) would strengthen this task type.

---

## Checklist Freshness Assessment

### Critical Issue: Checklists Not Updated for Books 35-40

Six books were added in this knowledge base build session. None have been incorporated into any existing checklists via `update_checklist`. The checklists deliver knowledge to agents — books that exist in `book_research/` but are not referenced in any checklist are invisible in the primary use path.

| Book | Key Concepts Not In Checklists | Affected Task Types |
|------|-------------------------------|---------------------|
| 35 — Agenda Mover | Coalition building, 4-stage execution, 7 objection types | `feature_design`, `product_doc`, `presentation` |
| 36 — Domain-Driven Design | Bounded contexts, ubiquitous language, aggregates, context maps | `architecture_review`, `feature_design`, `api_design`, `code_review`, `refactoring` |
| 37 — Pyramid Principle | SCQA, MECE, message headlines, "so what?" test | `product_doc`, `presentation` |
| 38 — Enterprise Integration Patterns | Outbox pattern, competing consumers, dead letter, saga | `architecture_review`, `api_design`, `bug_fix`, `observability` |
| 39 — Threat Modeling | STRIDE per DFD element, trust boundaries, 4 questions | `security_audit`, `architecture_review`, `feature_design` |
| 40 — Working Backwards | PR/FAQ format, customer quote test, six-pager, Type 1/2 decisions | `feature_design`, `product_doc`, `api_design`, `architecture_review` |

**Impact:** An agent calling `get_task_checklist("architecture_review")` gets excellent content from books 01-06 and 17-19, but gets nothing from DDD [36], EIP [38], or Threat Modeling [39] — even though those books have significant architecture review content and are listed as primary/secondary sources in routing.json.

**Recommended action:** Use `update_checklist` to add the highest-value items from each new book into the relevant checklists. Priority order:
1. DDD [36] → `architecture_review` (bounded contexts, context map)
2. EIP [38] → `architecture_review` (messaging patterns, outbox, saga)
3. Threat Modeling [39] → `security_audit` (STRIDE, DFD trust boundaries)
4. Working Backwards [40] → `feature_design` and `product_doc` (PR/FAQ, customer quote test)
5. Pyramid Principle [37] → `product_doc` and `presentation` (SCQA, MECE, message headlines)
6. Agenda Mover [35] → `feature_design` (political empathy, coalition building)

### Checklist Frontmatter Staleness

The checklist frontmatter lists `primary_sources` and `secondary_sources`. These were correct at build time but have not been updated as routing.json evolved:

- `architecture_review.md` frontmatter: `primary_sources: ["01", "02", "03", "04", "05", "06"]` — missing "36" (DDD now in primary in routing.json)
- `security_audit.md` frontmatter: `primary_sources: ["07", "08"]` — missing "39" (Threat Modeling now in primary in routing.json)
- `feature_design.md` frontmatter: not checked, but likely similar drift

The frontmatter is used by the MCP server for `list_available_knowledge` task display (showing primary sources). Stale frontmatter misleads agents about which sources are relevant.

---

## Book Research File Quality Assessment

### Structural Consistency

All book research files follow the standard template:
- Header (title, skill category, relevance statement)
- What This Book Is About
- Key Ideas & Mental Models
- Patterns & Approaches Introduced
- Tradeoffs & Tensions
- What to Watch Out For
- Applicability by Task Type
- Relationship to Other Books
- Freshness Assessment
- Key Framings Worth Preserving

**Sample quality check — most recently added books (35-40):**

| Book | Completeness | Applicability Sections | Cross-References | Freshness |
|------|-------------|----------------------|-----------------|-----------|
| 35 — Agenda Mover | Complete | feature_design, product_doc, presentation | Complements [29], [37] | 2016 — assessed as still relevant |
| 36 — DDD | Complete | architecture_review, feature_design, api_design, code_review, refactoring | Complements [01], [02], [04], [05] | 2003 — classic, assessed as evergreen |
| 37 — Pyramid Principle | Complete | product_doc, presentation, architecture review | Complements [26], [35] | 1987 — assessed as evergreen |
| 38 — EIP | Complete | architecture_review, api_design, feature_design, bug_fix | Complements [01], [02], [05] | 2003 — classic, assessed as largely evergreen |
| 39 — Threat Modeling | Complete | security_audit, architecture_review, feature_design | Complements [07], [08] | 2014 — assessed as current |
| 40 — Working Backwards | Complete | product_doc, feature_design, api_design, architecture_review | Complements [29], [37], [35] | 2021 — current |

All six new books are structurally complete and high-quality. ✓

### Cross-Reference Quality

The "Relationship to Other Books" section in each book file provides forward references. These are useful for drill-down navigation. Assessing cross-reference completeness:

**Well-connected books:**
- Working Backwards [40] references Inspired [29], Pyramid Principle [37], Agenda Mover [35], DDD [36] — very well-integrated
- DDD [36] references DDIA [01], Clean Architecture [02][04], Microservices [05] — correctly placed in the architecture cluster
- EIP [38] references DDIA [01], Microservices [05], Release It! [17] — correctly placed

**Missing cross-references:**
- Threat Modeling [39] should cross-reference Web Hacker's Handbook [07] more explicitly; currently complementary mention only
- Pyramid Principle [37] should reference Working Backwards [40] (six-pager = pyramid applied); currently does not because [40] was added after [37]
- Agenda Mover [35] does not reference Working Backwards [40] (both cover stakeholder alignment); similarly missing

These missing cross-references are expected (they're among the most recently added books) and can be updated incrementally.

---

## Pyramid Principle Quality Assessment [37]

Evaluating each book research file's argument structure:

**Are the Key Ideas sections top-down?** Generally yes — the most important conceptual models are listed first, with supporting detail below. The architecture books tend to lead with the core thesis before enumerable patterns. ✓

**Are the Applicability sections MECE?**
The Applicability by Task Type sections in each book are organized by task type slug (matching the routing.json task types). This is MECE relative to the task taxonomy — each task type gets its own subsection, they don't overlap. ✓

**Are Key Framings genuinely quotable?**
Yes — the "Key Framings Worth Preserving" sections contain the most pithy, agent-ready formulations of each book's core ideas. These are the highest-value content for token-constrained agent use. ✓ Good curation.

**"So what?" test on each book:**
The Freshness Assessment section in each book file addresses this directly: "Still relevant?" with a "Bottom line:" verdict. This answers the agent's implicit question about whether to trust this source. ✓

---

## LLM-as-Judge Quality Assessment [34]

The knowledge base can be evaluated with the same framework used in the test suite:

**Capability test (would a model armed with this checklist identify a seeded issue?):**
The eval fixtures in `tests/eval_fixtures/` test specific issues (SQL injection, shallow modules, missing timeouts). The architecture_review and security_audit checklists are calibrated to catch these. Based on the eval system's design (Pass@k measurement), this is the right frame.

**Reliability test (does the model consistently use the checklist items?):**
The activation eval fixtures test whether models proactively invoke the tools. 4 activation fixtures is a thin coverage — it tests "do models call the tool at all?" but not "do models use the right parts of the tool response?"

**Knowledge gap assessment:**
The six unchecked books (35-40) represent a capability gap that the eval system would currently miss — there are no fixtures that would surface DDD bounded context knowledge, EIP messaging patterns, or Working Backwards PR/FAQ application.

---

## Identified Coverage Gaps (Priority-Ordered)

**Gap 1 (Critical):** Checklists not updated for books 35-40.
*Impact:* 6 books with significant knowledge are inaccessible through the primary delivery path.
*Fix:* `update_checklist` calls for each relevant task type.

**Gap 2 (High):** `agent_design` task type has only 1 primary book.
*Impact:* Agents doing agent design get one book and 21 secondary articles; the checklist may not be as comprehensive as other task types.
*Fix:* Promote key Anthropic articles (a01, a02, a03) to effective "primary" status in the checklist, or add a second primary book source.

**Gap 3 (High):** `api_design` has 1 primary source.
*Impact:* The API design task type is the most common engineering task and is underserved by a single primary book.
*Fix:* Consider promoting EIP [38] and/or DDD [36] to primary for api_design, or adding a dedicated REST/HTTP API design book (e.g., RESTful Web Services by Richardson & Ruby).

**Gap 4 (Medium):** Checklist frontmatter source lists are stale.
*Impact:* `list_available_knowledge` shows incorrect primary sources for affected task types.
*Fix:* Sync checklist frontmatter primary_sources and secondary_sources with routing.json for all checklists.

**Gap 5 (Medium):** No book on team structure or software organization.
*Impact:* Architecture reviews may not surface org-alignment concerns (Conway's Law is mentioned in checklists but has no primary book source).
*Fix:* Consider adding Team Topologies (Skelton & Pais) or Accelerate (Forsgren et al.) — both were in the original recommendation list with ★★★☆☆ durability ratings.

**Gap 6 (Low):** No book on performance engineering.
*Impact:* Performance review is not a named task type; performance concerns are scattered across architecture and observability checklists.
*Fix:* Could be addressed by adding Systems Performance (Gregg) as a secondary source for architecture_review and observability.

---

## Freshness Monitoring

The system has a `refresh_checklists.py` script for staleness detection (compares file mtimes). However:
- The script has not been run recently (last `updated` dates in checklist frontmatter are 2026-02-22)
- Books 35-40 have no corresponding checklist items to compare against
- The version tracking in checklist frontmatter (all at `version: 1`) has not been bumped

**Recommendation:** After incorporating books 35-40 into checklists, run `refresh_checklists.py` and establish a cadence (monthly or after each batch of book additions) for freshness checks.
