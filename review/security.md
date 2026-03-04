# Security Audit

**Frameworks applied:** [39] Threat Modeling (Shostack), [07] Web Application Hacker's Handbook, [08] LLM Security Playbook
**Checklist source:** knowledge/checklists/security_audit.md
**Verdict: Medium** — The read path is safe with a narrow attack surface. The write tools (`add_knowledge_source`, `update_checklist`) have unmitigated file-write risks that could corrupt the knowledge base or, in an HTTP deployment, escape the intended write boundary.

---

## Threat Modeling: STRIDE Analysis [39]

### System Model

The system has two distinct deployment modes with different threat surfaces:

**Mode A: stdio (default)** — MCP server launched as a child process by the agent. Trust boundary: the operating system process boundary. Attacker must already have access to the agent or the OS session to interact with the server. Threat surface is narrow.

**Mode B: StreamableHTTP** — MCP server exposed over HTTP (with Cloudflare Tunnel or similar). Trust boundary: the network. Any caller who can reach the endpoint can issue tool calls.

The analysis below covers both modes, noting where the threat changes.

### Data Flow Diagram (DFD)

```
[Agent / MCP Client]
        │
        │ Tool call (JSON over stdio or HTTP)
        │
[MCP Server — Python process]
        │
        ├─── READ PATH ──────────────────────────────
        │           ├── book_research/*.md (read)
        │           ├── knowledge/checklists/*.md (read)
        │           ├── knowledge/routing.json (read)
        │           └── knowledge/book_index.json (read)
        │
        └─── WRITE PATH ─────────────────────────────
                    ├── book_research/*.md (create)
                    ├── knowledge/routing.json (read+write)
                    └── knowledge/book_index.json (read+write)

Trust boundaries:
  [Agent → Server]:   Process boundary (stdio) | Network (HTTP)
  [Server → Files]:   OS filesystem permissions only
```

---

### STRIDE Per Component

#### Tool Input Processing (call_tool handler in tools.py)

| Threat | Applies? | Detail |
|--------|----------|--------|
| **Spoofing** | Low (stdio) / Medium (HTTP) | In stdio mode, the caller is the spawning agent — already trusted. In HTTP mode, there is no authentication; any caller is accepted as legitimate. |
| **Tampering** | Medium | Tool arguments are user-controlled strings fed into file paths, JSON writes, and regex operations. No sanitization beyond `_slugify`. |
| **Repudiation** | Low | No audit logging of tool calls. Who called what is not recorded. Medium concern for HTTP deployment. |
| **Information Disclosure** | Low | Read tools return knowledge base content — this is intentional. No sensitive data (no credentials, no user data) stored in the system. |
| **Denial of Service** | Low (stdio) / Medium (HTTP) | A malicious caller could issue large `add_knowledge_source` calls that fill the filesystem, or trigger expensive regex operations on large content. No rate limiting. |
| **Elevation of Privilege** | **High** | Write tools can write arbitrary content to the filesystem under `book_research/`. Path traversal could escape this boundary (see Finding 1). |

#### KnowledgeManager (write operations)

| Threat | Applies? | Detail |
|--------|----------|--------|
| **Tampering** | **High** | `add_knowledge_source` writes the caller-provided `content` string directly to a file. The content can contain arbitrary text including markdown that could corrupt tool output or inject malicious instructions. |
| **Tampering** | **High** | `update_checklist` uses substring matching (`_remove_items`) and section injection (`_add_items_to_section`) on caller-provided strings. A malicious caller could remove legitimate checklist items or inject content that affects downstream agent behavior. |
| **Elevation of Privilege** | **High** | `_slugify` converts the title to a filename. It strips most special characters but does not guarantee the path stays within `book_research/`. See Finding 1. |

---

## Findings

### Finding 1: Path Traversal in `add_knowledge_source` [CRITICAL — in HTTP mode]

**Location:** `knowledge_manager.py:84-90`

```python
slug = self._slugify(title)          # title is caller-provided
filename = f"{num}_{slug}.md"
file_path = self.book_research_dir / filename  # book_research / {num}_{slug}.md
```

**`_slugify` implementation (`knowledge_manager.py:52-57`):**
```python
def _slugify(self, title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s]", "", slug)   # strips everything except alphanum and whitespace
    slug = re.sub(r"\s+", "_", slug.strip())
    return slug[:60]
```

The `_slugify` function strips `/`, `.`, and `..` characters — which means a direct path traversal via title (e.g., `title = "../../etc/passwd"`) is neutralized by the regex. After slugification: `slug = ""` (all characters stripped), producing `filename = "41_.md"`. The file would be written inside `book_research/` — not an escape.

**However:** The function does not defend against Unicode normalization attacks (e.g., Unicode lookalike characters that some filesystems normalize to `/`). On case-insensitive filesystems, a carefully crafted slug could collide with existing files and overwrite them.

**More critically:** The `category`, `author`, and `content` parameters are not slugified at all. `content` is written verbatim to disk — which is intentional. But `category` (used only in `book_index.json`) and `author` could contain characters that corrupt the JSON if the JSON serialization is not correctly escaped. Python's `json.dumps` handles this correctly, so JSON injection is mitigated. ✓

**Risk level in stdio mode:** Low — the agent is trusted.
**Risk level in HTTP mode:** High — an unauthenticated caller can write arbitrary content to the knowledge base directory.

**Recommendation:** Add an explicit check that `file_path` is within the expected directory:
```python
file_path = (self.book_research_dir / filename).resolve()
if not str(file_path).startswith(str(self.book_research_dir.resolve())):
    raise ValueError(f"Path traversal detected: {file_path}")
```

---

### Finding 2: Content Injection — Malicious Checklist Items [HIGH]

**Location:** `knowledge_manager.py:169-228` (`_add_items_to_section`, `_replace_section`)

The `update_checklist` tool inserts caller-provided `content` into checklist files with no validation of what the content contains. Because checklists are read by AI agents as authoritative knowledge, a malicious `update_checklist` call could inject:
- Fake checklist items that direct the agent to perform unsafe actions
- Instructions that manipulate the agent's behavior in downstream contexts (prompt injection via stored checklist content)
- Content that breaks the markdown structure and corrupts the detail-level filtering

**In stdio mode:** The agent calling the tool is the same agent reading the checklist — the attack would require the agent to undermine itself, which is theoretically possible via an indirect prompt injection but unlikely.

**In HTTP mode:** A malicious third party could call `update_checklist` and insert adversarial instructions into checklists that are later retrieved by a legitimate agent. This is a stored prompt injection vector. [08]

**Recommendation:**
- Add content validation: checklist items should match the pattern `- [ ] <text> [citation]`
- In HTTP mode, require authentication before write tool access
- Log all write tool calls with the content written (for forensic audit)

---

### Finding 3: No Authentication on Write Tools [HIGH — HTTP mode only]

**Location:** `server.py:37-55` (`main_http`)

The HTTP transport mode (`main_http`) uses `StreamableHTTPSessionManager` with `stateless=True` and no authentication middleware. Any caller who can reach the endpoint can invoke `add_knowledge_source` or `update_checklist`.

**Risk:** Knowledge base corruption, prompt injection via stored content, denial of service via filesystem filling.

**In stdio mode:** Not applicable — the server is a child process of the agent, and OS-level process boundaries apply.

**Recommendation:** Add HTTP Basic Auth or an API key check as middleware before routing to the MCP handler if exposing via HTTP. The Starlette `Middleware` stack supports this cleanly.

---

### Finding 4: No Audit Log [MEDIUM]

**Location:** All write tool handlers in `tools.py`

The `add_knowledge_source` and `update_checklist` tools modify the knowledge base with no record of who called them, when, with what arguments, or what the result was. If the knowledge base becomes corrupted, there is no forensic trail.

**Risk:** After corruption, it is impossible to determine what happened without reading git history (if the project is under version control). Knowledge base integrity depends entirely on git as an external forensic mechanism — which is not documented.

**Recommendation:**
- Add structured logging for all write tool calls: `{timestamp, tool, args_summary, result}`
- Document that `git commit` should be run after knowledge base additions as an integrity checkpoint

---

### Finding 5: `_save_json` Non-Atomic Write [MEDIUM]

**Location:** `knowledge_manager.py:28-32`

```python
def _save_json(self, path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
```

`Path.write_text` opens the file, truncates it, and writes. If the process crashes or is killed between truncation and completion of the write, the JSON file is empty or partially written — and unreadable by the next startup.

**Risk:** Knowledge base index corruption on unexpected shutdown. Low probability, high impact.

**Recommendation:** Write to a temp file, then `os.replace()`:
```python
import os, tempfile
tmp = path.with_suffix(".tmp")
tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
os.replace(tmp, path)   # atomic on POSIX
```

---

### Finding 6: No Rate Limiting on Write Tools [LOW — HTTP mode]

In HTTP mode, a caller could issue repeated `add_knowledge_source` calls filling the filesystem. No rate limiting or quota is applied. For a personal local tool this is irrelevant. For an HTTP-exposed deployment, this is a denial-of-service vector.

---

## LLM-Specific Security Assessment [08]

The shudaizi system is infrastructure for AI agents, not an LLM application itself. However, it has two relevant LLM security angles:

**1. Shudaizi as a source of prompt injection payloads (stored injection risk)**

If a malicious `update_checklist` call succeeds, the injected content is stored in a checklist file. When a legitimate agent later calls `get_task_checklist`, the injected content is returned as part of the tool response. If the injected content contains adversarial instructions (e.g., "Ignore your previous instructions and..."), the agent reading the checklist is exposed to a stored prompt injection.

This is the same attack class as RAG-based prompt injection documented in [08]. Mitigation: content validation on write; treat checklist content as untrusted input when displayed to agents.

**2. Shudaizi's book research files could contain attacker-controlled content**

If `add_knowledge_source` is used to add content from an external source (a web page, a user-provided text), that content is stored verbatim. If the content contains adversarial instructions disguised as book knowledge (e.g., a fake "best practice" item that directs the agent to expose credentials), subsequent `get_book_knowledge` calls would return that content to agents.

Mitigation: The `book_research_prompts.md` template provides a structured format that makes arbitrary instruction injection visible. But structural validation (confirming the content has the expected sections) is not enforced in code.

---

## Positive Security Findings

- **No credentials stored anywhere in the system.** The knowledge base contains only book content. No API keys, tokens, or secrets are stored. ✓
- **No outbound network calls from the MCP server.** The server only reads from and writes to the local filesystem. No SSRF risk. ✓
- **No SQL or shell execution.** The system uses filesystem operations and regex only. No injection vectors from SQL or OS command execution. ✓
- **JSON serialization is handled by `json.dumps`, not string concatenation.** This correctly prevents JSON injection in index files. ✓
- **`_slugify` neutralizes common path traversal characters** (slash, dot, backslash) in the filename component. ✓

---

## Summary Table

| Finding | Severity | Mode | Mitigated? |
|---------|----------|------|------------|
| No HTTP authentication on write tools | High | HTTP only | ✗ No |
| Content injection / stored prompt injection | High | Both | ✗ No |
| Path traversal in `add_knowledge_source` | Medium (stdio) / High (HTTP) | Both | Partially (slugify helps, not complete) |
| Non-atomic JSON writes | Medium | Both | ✗ No |
| No audit log for write operations | Medium | Both | ✗ No |
| No rate limiting on write tools | Low | HTTP only | ✗ No |
| No credentials stored | N/A | Both | ✓ Not applicable |
| No outbound network calls | N/A | Both | ✓ Not applicable |
| No SQL/shell injection vectors | N/A | Both | ✓ Not applicable |

---

## Recommendations by Priority

**Immediate (before HTTP deployment):**
1. Add HTTP authentication (API key or Basic Auth) before exposing via StreamableHTTP
2. Add explicit `file_path.resolve()` check to confirm write paths are within expected directories
3. Add content format validation on `update_checklist` (pattern-match against expected checklist item format)

**Short-term:**
4. Implement atomic JSON writes using temp file + `os.replace()`
5. Add structured logging for all write tool calls
6. Document that git commits after knowledge additions are the integrity checkpoint

**Acceptable as-is (stdio only):**
- No authentication on write tools (OS process boundary is sufficient)
- No rate limiting (single developer use case)
