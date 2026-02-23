---
name: security-audit
description: >
  Security audit using Web Application Hacker's Handbook, LLM Security Playbook, and related books.
  Use when auditing code or systems for security vulnerabilities, including LLM-specific risks.
---

## When to Activate

- User asks for a security review or audit
- User is implementing authentication, authorization, or input validation
- User is building LLM-powered features and needs security guidance
- User asks about specific vulnerability classes (injection, XSS, CSRF, etc.)

## Procedure

1. Read `knowledge/checklists/security_audit.md`
2. Assess the system against relevant checklist phases
3. For items needing deeper context, read the cited book file
4. Present findings organized by severity: **Critical** → **High** → **Medium** → **Low**
5. For each finding: describe the risk, cite the source, suggest a fix
6. If LLM components are present, always check the LLM-specific risks phase

## Always-Apply Principles

- All input is untrusted until validated on the server [07: Web App Hackers Handbook]
- Client-side controls are not controls — they are suggestions [07]
- Think like an attacker: "Map, Probe, Exploit" [07]
- LLM output is untrusted input — validate before acting on it [08: LLM Security Playbook]
- Defense in depth: no single control should be the only barrier [07]
- Blast radius analysis: "what's the worst that can happen if this is compromised?" [08]

## Deep-Dive References

- Web vulnerabilities & methodology: `book_research/07_web_application_hackers_handbook.md`
- LLM-specific risks: `book_research/08_llm_security_playbook.md`
- Data protection & encryption: `book_research/01_designing_data_intensive_applications.md`
- Production resilience: `book_research/17_release_it.md`
- API security patterns: `book_research/20_api_design_patterns.md`
- Agent sandboxing: `book_research/anthropic_articles/14_sandboxing.md`
