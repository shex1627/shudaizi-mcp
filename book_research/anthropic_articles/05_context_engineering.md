# Effective Context Engineering for AI Agents
**Date:** September 29, 2025
**URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Source:** Web-fetched Feb 2026

---

## Core Thesis

Context engineering is "the set of strategies for curating and maintaining the optimal set of tokens during LLM inference." The goal: **"the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."**

## Why Context Engineering > Prompt Engineering

Prompt engineering focuses on crafting effective instructions. Context engineering addresses the **entire information landscape** — system instructions, tools, external data, message history — the complete token set available during inference.

## The Problem: Context Rot

- Performance degrades as context grows — "context rot"
- Transformer architecture requires n² pairwise token relationships — computational strain at scale
- Models trained on shorter sequences have less experience with longer dependencies
- Performance gradients, not hard cliffs — degradation is gradual

## The Finite Attention Budget

Like human working memory, LLMs have limited capacity. Every token depletes this budget. Curation is essential.

## Anatomy of Effective Context

### System Prompts
- Strike the "right altitude" — specific enough to guide, flexible enough for autonomy
- Avoid two extremes: brittle hardcoded if-else logic vs. vague high-level guidance
- Start minimal, add instructions based on observed failure modes
- Use XML tags or Markdown headers to organize sections
- Best available model + minimal prompt first, then iterate

### Tools
- Self-contained, unambiguous, minimal overlap in functionality
- Token-efficient responses, clear input parameters
- Bloated tool sets "encourage misuse and wasted context"
- Exploit model strengths in parameter design

### Examples
- Diverse, canonical few-shot examples > exhaustive edge cases
- "Examples are the 'pictures' worth a thousand words" for LLMs

## Runtime Context Retrieval

### Just-In-Time Strategies
- Maintain lightweight identifiers (file paths, URLs)
- Dynamically retrieve information via tools during execution
- Mirrors human cognition — external organization systems vs. memorizing everything
- **Progressive disclosure**: agents incrementally discover relevant context through exploration

### Hybrid Approaches
- Pre-load critical data (CLAUDE.md files) + autonomous exploration via tools
- Combine pre-computed retrieval for speed with exploration for flexibility
- Context requirements depend on task characteristics and content dynamism

## Long-Horizon Techniques

### 1. Compaction
- Summarize conversation history when approaching context limits
- Preserve architectural decisions and unresolved issues
- Discard redundant outputs
- Tool result clearing = "safest lightest touch"
- Maximize recall initially, then iterate to improve precision

**Best for:** Extended back-and-forth requiring flow

### 2. Structured Note-Taking
- Agent periodically writes persistent notes outside context window
- Pulled back when needed
- Enables multi-hour coherence across context resets
- Tracks progress, maintains dependencies

**Best for:** Iterative development with clear milestones

### 3. Sub-Agent Architectures
- Specialized agents with clean context windows
- Return condensed summaries (1,000-2,000 tokens)
- Separates detailed search contexts from high-level synthesis

**Best for:** Complex research requiring parallel work

## Selection Guide

| Technique | When to Use |
|-----------|-------------|
| Compaction | Extended back-and-forth, maintaining flow |
| Note-Taking | Iterative development, clear milestones |
| Multi-Agent | Complex research, parallel work |

## Key Quotables

> "The smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

> "Context rot" — performance degrades as context grows.

---

## Applicability
- System prompt design
- Agent context management
- Long-horizon task planning
- RAG and retrieval architecture
- Token budget optimization
