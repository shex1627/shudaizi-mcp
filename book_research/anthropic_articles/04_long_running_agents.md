# Effective Harnesses for Long-Running Agents
**Date:** November 26, 2025
**URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Source:** Web-fetched Feb 2026

---

## Core Problem: The Shift-Change Problem

Agents lose memory across context windows — like "engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."

## Two Failure Patterns

1. **Over-ambition**: Agent attempts to implement everything simultaneously, exhausts context mid-task, leaves features half-documented for next session to decipher
2. **Premature completion**: Later instances observe completed features and declare project finished, missing remaining work

## The Two-Agent Solution

### Initializer Agent (First Session)
Establishes infrastructure:
- Creates `init.sh` deployment script
- Generates `claude-progress.txt` activity log
- Produces initial git commit documenting added files
- Sets up the framework for future sessions

### Coding Agent (Subsequent Sessions)
Follows structured protocol:
1. Review git logs and progress files
2. Select one incomplete feature
3. Complete work incrementally
4. Commit changes with descriptive messages

## Environmental Management

### Feature Lists
- Initializer writes comprehensive JSON file listing 200+ features as "failing" tests
- Agents can only modify the `passes` status field
- Editing requirements is prohibited — prevents missed functionality
- **JSON > Markdown** for feature specs: resists accidental modification better

### One Feature Per Session
- Single-feature focus >> comprehensive implementation attempts
- Prevents over-ambition failure pattern
- Clean, committable state at end of each session

### Testing Protocol
- Browser automation (Puppeteer MCP) replaced simple unit tests
- Enables end-to-end validation mimicking actual user workflows
- Agents testing like human users catch issues code-level testing misses

## Session Structure

Every session begins with:
1. Confirm working directory
2. Review progress documentation and git history
3. Identify next priority feature
4. Run basic tests to verify current state

This structured onboarding saves context tokens and prevents redundant troubleshooting.

## State Management

| State Type | Format | Purpose |
|-----------|--------|---------|
| Test results / task status | JSON | Structured, machine-readable |
| Progress notes | Freeform text | General context |
| Checkpoints | Git commits | Restorable snapshots |

## Key Quotable

> "The shift-change problem" — agents losing context across windows is the fundamental challenge of long-running work.

---

## Applicability
- Multi-session agent development
- Long-horizon autonomous task execution
- State persistence patterns
- Agent harness design
