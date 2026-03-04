# Operational Readiness Review

**Frameworks applied:** [17] Release It!, [18] Observability Engineering, [19] SRE, [32] DevOps Handbook
**Checklist source:** knowledge/checklists/observability.md, knowledge/checklists/devops.md
**Verdict: Low-Medium for current use; Not ready for HTTP/multi-user deployment** — The system operates without logging, error tracking, or deployment automation. For a single-developer local tool with stdio transport, this is acceptable. For any HTTP exposure or shared team use, these gaps become blockers.

---

## Scope Definition

Operational readiness criteria must be calibrated to deployment mode:

| Mode | Expected scale | Operational bar required |
|------|---------------|------------------------|
| **Current: stdio, solo dev** | 1 user, local machine | Low — git history as audit trail; manual recovery |
| **Near-term: HTTP + Cloudflare Tunnel** | 1-10 users, network-accessible | Medium — auth, logging, error recovery |
| **Hypothetical: hosted/SaaS** | Many users | High — full observability stack, deployment pipeline, SLA |

The review below assesses the current state and flags what changes by deployment mode.

---

## Observability Assessment [18]

### Structured Logging

**Current state:** No logging is implemented anywhere in the MCP server. `server.py`, `tools.py`, `book_loader.py`, `knowledge_manager.py`, and `routing.py` have no `import logging` and no log calls.

**Impact in stdio mode:** Silent failures are the primary risk. If `get_book_knowledge("99", "key_ideas")` is called with an invalid book ID, the response is the string `"Book '99' not found."` — returned as a normal text response. The agent may or may not handle this correctly. There is no server-side record that the failure occurred.

**Impact in HTTP mode:** An operator has no way to know how many tool calls are being made, which tools are failing, or what the response latency distribution looks like. Debugging a production issue requires re-creating the scenario manually.

**Minimum viable logging for stdio mode:**
```python
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger("shudaizi")

# In call_tool:
start = time.perf_counter()
result = ...   # existing dispatch
duration_ms = (time.perf_counter() - start) * 1000
logger.info(f"tool={name} status={'error' if 'not found' in result else 'ok'} duration_ms={duration_ms:.1f}")
```

This adds ~5 lines per tool call and gives the minimum needed to diagnose silent failures.

**What observability looks like in a healthy system [18]:**
- Every tool call logged: tool name, arguments summary (not full content), duration, outcome
- Write tool calls logged with additional detail: what was written, what files were modified
- Error events logged with stack traces, not just error strings

### Distributed Tracing

Not applicable for a single-process local tool. If the system ever moves to an architecture where the MCP server calls external services (e.g., semantic search, external book sources), distributed tracing would become relevant.

### Metrics

**Current state:** No metrics collected. No Prometheus endpoint, no counter of tool calls, no histogram of response sizes.

**What would be useful:**
- Tool call count by tool name (which tools are actually used?)
- Response size distribution (are responses hitting the token budget?)
- Error rate by tool name
- Write operation count (how often is the knowledge base being modified?)

These metrics would also provide evidence for the product's usage claims — currently there is no data on which checklists are most used.

### Alerting

Not applicable for a local single-user tool. In HTTP mode, alerting on error rate or response latency would be the minimum.

---

## Error Handling Assessment [17]

### Current Error Handling Patterns

**Pattern 1: Return error string as normal text content**
```python
# book_loader.py
return f"Book '{book_id}' not found."
# tools.py
return [TextContent(type="text", text=content)]
```
This is the dominant error pattern. The agent receives a successful MCP response (HTTP 200 / stdio success) with error text embedded. The agent must string-match to detect failure. This is the "errors as values" anti-pattern for a system designed for machine consumption.

**Pattern 2: Return error dict embedded in result**
```python
# knowledge_manager.py
if "error" in result:
    return [TextContent(type="text", text=f"Error: {result['error']}")]
```
Same problem — the error is distinguishable by the string prefix "Error: " but not by MCP response type.

**Pattern 3: No error handling**
```python
# routing.py
return self._routing_data  # crashes if JSON is malformed
```
If `routing.json` is corrupted (malformed JSON from a crash during write), the server crashes with an unhandled exception on the next read operation. No try/catch, no fallback.

**What Release It! says about stability patterns [17]:** All external calls and resource acquisitions need explicit failure handling. File reads are "external calls" in the sense that the filesystem can fail (disk full, permission denied, malformed file). The system should fail gracefully with meaningful error messages rather than crashing the MCP server process.

**Recommended approach:** Use MCP protocol error responses for tool-level failures:
```python
from mcp.types import McpError, ErrorCode

# Instead of:
return [TextContent(type="text", text="Book '99' not found.")]

# Use:
raise McpError(ErrorCode.INVALID_REQUEST, "Book '99' not found in knowledge base.")
```

This allows agents to programmatically detect failure vs. success and handle accordingly.

### Circuit Breakers and Timeouts

Not applicable — there are no network calls or slow external resources in the read path. All I/O is local filesystem, which is fast and bounded.

**Exception:** Checklist and book files can be large. A `get_book_knowledge("01", "full")` call reads DDIA (250+ lines, ~15K tokens). No timeout exists on this read, but for local filesystem this is effectively instantaneous.

### Steady State [17]

**The system reaches steady state without human intervention** — there are no background processes, no caches to warm, no cleanup jobs. Each tool call is stateless (except write operations). ✓

**Exception:** The `router.reload()` call in `list_available_knowledge` re-reads JSON from disk on every call. This is correct for freshness but means every `list_available_knowledge` call has a file I/O cost. For a local tool this is fast; for an HTTP-exposed server handling many requests, this could be optimized with a TTL cache.

---

## Resilience Assessment [17]

### Failure Mode Analysis

| Component | Failure Scenario | Current Behavior | Desired Behavior |
|-----------|-----------------|------------------|-----------------|
| `routing.json` | Malformed JSON | Server crash (unhandled json.JSONDecodeError) | Return cached last-known-good; log error |
| `book_index.json` | Malformed JSON | Server crash | Same |
| Checklist file | Missing at call time | Returns "Checklist 'X' not found." as text | Return MCP error response |
| Book file | Missing at call time | Returns "Book 'X' not found." as text | Return MCP error response |
| Write operation | Disk full | Unhandled OSError; may corrupt files | Catch, return MCP error, no file modification |
| `add_knowledge_source` | Duplicate book_id | Overwrites existing entry in book_index.json | Check for existing ID, return error |

**Most critical gap:** Malformed JSON crashing the server. If `routing.json` is corrupted during a write (process killed, disk full, filesystem error), the next startup will crash before serving any tool calls. The server has no mechanism to detect or recover from this.

**Recommended mitigation:** Wrap JSON loads in try/except and return a diagnostic error response:
```python
def _load_json(self, path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to load {path}: {e}")
        return {}  # degrade gracefully
```

---

## DevOps & Deployment Assessment [32]

### Deployment Pipeline

**Current state:** There is no CI/CD pipeline. The project has no `.github/workflows/`, no `Makefile` targets for test, and no automated release process.

**Impact for current use:** A solo developer can run tests manually. Risk: tests are not run consistently; regressions may go undetected for days.

**Minimum viable CI (GitHub Actions example):**
```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -e mcp_server[test]
      - run: pytest tests/test_level1_integrity.py tests/test_level2_mcp_protocol.py -v
```

L3 (LLM eval) should not run in CI by default (requires API key, is slow, costs money) but should be runnable on-demand.

### Version Management

**Current state:** No version number. `pyproject.toml` may have a version, but the knowledge base itself has no version. There is no changelog.

**Impact:** When the MCP server is installed (`pip install -e .`) and the knowledge base is updated, there is no way for a user to know what changed between their installed version and the current knowledge base state.

### Installation & Configuration

The installation path is documented in the README:
1. `cd mcp_server && pip install -e .` — installs the MCP server
2. Add JSON config to `~/.claude/settings.json` — configures the MCP client

**Concerns:**
- The `PROJECT_ROOT` resolution (`Path(__file__).resolve().parent.parent.parent.parent`) means the MCP server must be run from the repository directory. If installed globally via pip (not editable install), the server cannot find the `book_research/` and `knowledge/` directories. This is a significant installation footprint problem for users who want a "proper" install.
- No `--knowledge-path` flag to override the project root. If the user wants to store their knowledge base elsewhere, they cannot.

**Recommendation:** Add a `SHUDAIZI_KNOWLEDGE_PATH` environment variable as the canonical way to specify the knowledge base location. This would allow proper pip install + custom knowledge base location:
```python
PROJECT_ROOT = Path(os.environ.get("SHUDAIZI_KNOWLEDGE_PATH",
    Path(__file__).resolve().parent.parent.parent.parent))
```

---

## Backup & Recovery Assessment

**Current state:** No backup mechanism. The knowledge base is a set of files in a git-able directory structure. Recovery depends on git being used.

**Implicit recovery mechanism:** If the project is under git version control (which it appears to be — there is a `.github/` directory implied by the docs), then `git checkout` is the recovery mechanism for corrupted files.

**Risk:** This is not documented. A user who is not aware that git history is their backup mechanism may not commit regularly and will lose knowledge additions if files are corrupted.

**Recommendation:** Add a note to CONTRIBUTING.md: "Commit your knowledge base additions to git immediately after making them — git history is your recovery mechanism."

---

## Summary

| Operational Concern | Current State | Priority | Mode |
|--------------------|---------------|----------|------|
| Structured logging | ✗ None | **High** | Both |
| Error distinction (text vs. MCP error) | ✗ All text | High | Both |
| JSON load error handling | ✗ Crashes server | **High** | Both |
| Write operation error handling | ⚠ Partial | High | Both |
| Atomic JSON writes | ✗ Missing | Medium | Both |
| HTTP authentication | ✗ Missing | **Critical** | HTTP only |
| CI/CD pipeline | ✗ Missing | Medium | Both |
| SHUDAIZI_KNOWLEDGE_PATH env var | ✗ Missing | High | Both |
| Version tracking / changelog | ✗ Missing | Low | Both |
| Metrics collection | ✗ Missing | Low | Both |
| Alerting | Not applicable | — | stdio |
| Distributed tracing | Not applicable | — | stdio |
| Circuit breakers | Not applicable | — | stdio |
| Steady state self-management | ✓ Good | — | Both |
| Zero infrastructure | ✓ Excellent | — | Both |
