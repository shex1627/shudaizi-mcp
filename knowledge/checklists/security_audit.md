---
task: security_audit
description: Audit system or code for security vulnerabilities and risks
primary_sources: ["07", "08"]
secondary_sources: ["01", "17", "20"]
anthropic_articles: ["a14"]
version: 1
updated: 2026-02-22
---

# Security Audit Checklist

## Phase 1: Attack Surface Mapping

- [ ] Enumerate all input surfaces: form fields, HTTP headers (Host, Referer, User-Agent, Cookie), URL path/query params, JSON/XML bodies, file uploads, WebSocket messages [07]
- [ ] Identify every trust boundary where data crosses domains (user-to-server, server-to-database, server-to-third-party API, front-end-to-back-end) [07]
- [ ] Map all integration points -- each external call (HTTP, RPC, DB query, message queue) is a potential failure and attack vector [17]
- [ ] Inventory all API endpoints, including unlinked/undocumented ones; forced browsing targets endpoints without authorization regardless of discoverability [07]
- [ ] Document the technology stack per component to understand framework-specific vulnerability classes [07]
- [ ] For LLM-integrated systems: map every data channel reaching the model (user prompts, RAG documents, tool outputs, system context) [08]

## Phase 2: Authentication and Session Management

- [ ] Verify passwords are hashed with a strong adaptive algorithm (bcrypt/scrypt/argon2), never stored in plaintext [07]
- [ ] Confirm session tokens use cryptographically secure random generators (CSPRNG) with sufficient entropy [07]
- [ ] Verify session IDs are regenerated after authentication state changes (login, privilege escalation) [07]
- [ ] Check for credential enumeration: error messages and response times must be identical for valid vs. invalid usernames [07]
- [ ] Confirm MFA is available for high-value accounts and sensitive operations [07]
- [ ] Validate rate limiting and account lockout on login endpoints to prevent brute force [07]
- [ ] Ensure session expiry and idle timeouts are enforced server-side [07]
- [ ] For APIs: verify OAuth token validation includes audience, issuer, expiry, and signature checks [07] [20]

## Phase 3: Authorization and Access Control

- [ ] Confirm server-side authorization checks exist on every endpoint -- not just authenticated, but authorized for the specific resource [07]
- [ ] Test for vertical privilege escalation: can a regular user access admin functions? [07]
- [ ] Test for horizontal privilege escalation (IDOR): can user A access user B's resources by changing an ID? [07]
- [ ] Verify client-side controls (hidden fields, disabled buttons, JS validation) are duplicated server-side [07]
- [ ] Check that API responses return only fields the caller is authorized to see -- no over-fetching of sensitive data [20]
- [ ] For LLM tool-calling: verify each tool has minimum permissions, separate service accounts, and rate limits [08]
- [ ] Require human-in-the-loop approval for destructive or irreversible LLM-initiated actions [08]

## Phase 4: Input Validation and Injection

- [ ] Confirm all database queries use parameterized queries/prepared statements -- never string concatenation [07]
- [ ] Verify OS command execution uses language-native APIs, not shell calls; if unavoidable, strict allowlisting [07]
- [ ] Check for XXE: external entity processing disabled in all XML parsers [07]
- [ ] Validate that input filtering uses allowlisting (define what is permitted), not blacklisting [07]
- [ ] Check for second-order injection: data stored safely but later used unsafely in a different context [07]
- [ ] Test for mass assignment / parameter pollution: extra parameters binding to internal model fields (e.g., `isAdmin=true`) [07]
- [ ] Verify output encoding is context-aware: HTML body, HTML attribute, JavaScript, URL, CSS each need different encoding [07]
- [ ] For LLM systems: never pass LLM output directly to SQL, shell commands, `eval()`, `innerHTML`, or API calls with elevated permissions [08]

## Phase 5: Data Protection

- [ ] Verify sensitive data at rest is encrypted; encryption keys are managed separately from data [01]
- [ ] Confirm transport-layer encryption (TLS) for all data in transit, including internal service-to-service calls [01]
- [ ] Check that error messages do not leak stack traces, SQL queries, file paths, or server versions [07]
- [ ] Verify debug interfaces (`/debug`, `/console`, `/phpinfo`) are removed or gated behind auth and IP restriction [07]
- [ ] Confirm `.git/`, backup files, and source code are inaccessible from the web [07]
- [ ] Strip or genericize server version headers in HTTP responses [07]
- [ ] For LLM systems: never put secrets or API keys in system prompts -- assume prompts will be extracted [08]
- [ ] Audit logging: log authentication events, authorization failures, and all state-changing operations for forensics [01] [17]

## Phase 6: LLM-Specific Risks

- [ ] Test for direct prompt injection: "Ignore previous instructions" variants, role-play jailbreaks, encoding-based evasion [08]
- [ ] Test for indirect prompt injection via RAG: adversarial content in knowledge base documents that hijacks model behavior [08]
- [ ] Validate LLM output with strict schema validation before downstream use; reject malformed responses [08]
- [ ] Verify system prompt hardening: critical instructions at start and end, explicit delimiters, anti-extraction instructions [08]
- [ ] Assess the agency-risk level: read-only (low), constrained actions (medium), autonomous agent (high) -- match controls to level [08]
- [ ] Pin model versions in production; verify model provenance with checksums when downloading [08]
- [ ] Monitor for output anomalies: topic shifts, unusual tool call sequences, system prompt extraction attempts [08]

## Phase 7: Infrastructure and Production Security

- [ ] Verify every outbound call has both connection and response timeouts configured [17]
- [ ] Confirm circuit breakers are in place at integration points with meaningful fallback behavior [17]
- [ ] Check for unbounded result sets: all queries must paginate with server-enforced limits [17] [20]
- [ ] Ensure resource pools (thread pools, connection pools, queues) are bounded to prevent exhaustion [17]
- [ ] Verify back-pressure mechanisms: bounded queues, HTTP 429 responses, load shedding for overload [17]
- [ ] For agent sandboxing: enforce dual-boundary isolation -- filesystem restriction AND network restriction at OS/kernel level [a14]
- [ ] Separate credentials for agent-initiated actions from system-initiated actions to contain compromise [a14] [08]
- [ ] Validate CORS configuration: no wildcard origins with credentials, explicit allowlisted origins only [07]
- [ ] Confirm CSP headers are set to mitigate XSS; use `frame-ancestors` to prevent clickjacking [07]

## Key Questions to Ask

1. "What is the blast radius if this component is fully compromised?" -- determines permission scoping [08] [17]
2. "What happens when this dependency is slow, down, or returns garbage?" -- every integration point [17]
3. "Can steps be skipped, reordered, or repeated in this workflow?" -- logic flaw detection [07]
4. "Is this defense actually tested, or just structurally present?" -- presence of a validation function is not evidence of security [07]
5. "What data crosses this trust boundary, and how is it validated on both sides?" -- trust boundary analysis [07]
6. "If the LLM is fully compromised via prompt injection, what can it access?" -- agent permission audit [08]
7. "Does each layer of defense work as if it were the only defense?" -- defense in depth validation [07]
8. "What grows without bound, and how is it cleaned up?" -- steady-state analysis [17]

## Common Vulnerabilities to Check

| Vulnerability | Detection Method | Source |
|---|---|---|
| SQL / NoSQL Injection | Trace all query construction for string concatenation | [07] |
| XSS (Reflected, Stored, DOM) | Check all output rendering for context-aware encoding; search for `innerHTML`, `v-html`, `dangerouslySetInnerHTML` | [07] |
| Broken Access Control (IDOR) | Attempt accessing resources by changing IDs with different user sessions | [07] |
| CSRF | Verify anti-CSRF tokens and SameSite cookie attributes on state-changing operations | [07] |
| SSRF | Check if user-controlled URLs are fetched server-side without allowlisting | [07] |
| Insecure Deserialization | Search for deserialization of untrusted data (Java ObjectInputStream, Python pickle, etc.) | [07] |
| Prompt Injection | Attempt instruction override, jailbreaks, and system prompt extraction against LLM endpoints | [08] |
| Insecure LLM Output Handling | Trace LLM output to all downstream consumers (DB, shell, renderer, API) | [08] |
| Excessive LLM Agency | Audit all tools/functions available to the LLM and their permission levels | [08] |
| Cascading Failure | Map failure propagation paths through integration points; verify timeout + circuit breaker coverage | [17] |
| Unbounded Resource Consumption | Check for missing pagination, unbounded queues, and missing rate limits on API and LLM endpoints | [17] [20] [08] |
