# Beyond Permission Prompts: Claude Code Sandboxing
**Date:** October 20, 2025
**URL:** https://www.anthropic.com/engineering/claude-code-sandboxing
**Source:** Web-fetched Feb 2026

---

## Core Innovation

Dual-boundary sandboxing for Claude Code that "safely reduces permission prompts by 84%" while enhancing security.

## The Two-Boundary System

### 1. Filesystem Isolation
- Claude can only access/modify specific directories
- Prevents prompt-injected instances from tampering with sensitive system files
- Without this: agents could escape sandbox constraints entirely

### 2. Network Isolation
- Connections restricted to approved servers through a proxy service
- Blocks data exfiltration and malware downloads
- Without this: compromised agents could steal SSH keys

**Both boundaries are essential**: "Effective sandboxing requires *both* filesystem and network isolation."

| Missing Boundary | Risk |
|-----------------|------|
| No network isolation | SSH key theft, data exfiltration |
| No filesystem isolation | Sandbox escape |

## Implementation

- Uses **OS-level primitives**: Linux bubblewrap, macOS seatbelt
- Enforced at kernel level
- Covers not just direct Claude interactions but also spawned scripts and subprocesses
- No userspace escape possible

## Features

### Sandboxed Bash Tool (Research Preview)
- Autonomous command execution within defined limits
- No permission prompts needed within sandbox boundaries
- 84% fewer permission interruptions

### Claude Code on the Web
- Runs sessions in isolated cloud sandboxes
- Custom proxy handles git credentials separately
- Credential separation prevents compromise exposure

## Open Source

Anthropic open-sourced the sandbox runtime to encourage broader adoption across the agent development community.

## Key Insight

The dual-boundary approach enables a much better UX (fewer permission prompts) while improving security. It's not a tradeoff — both get better simultaneously.

---

## Applicability
- Agent security architecture
- Sandboxing design patterns
- Development environment security
- Permission model design
