# Anthropic Engineering Blog — Article Reference Files

Individual article references from the Anthropic engineering blog, each web-fetched Feb 2026.

## File Index

### Agent Design & Architecture
| # | File | Article | Date |
|---|------|---------|------|
| 01 | [01_building_effective_agents.md](01_building_effective_agents.md) | Building Effective Agents | Dec 2024 |
| 02 | [02_multi_agent_research_system.md](02_multi_agent_research_system.md) | How We Built Our Multi-Agent Research System | Jun 2025 |
| 03 | [03_agent_sdk.md](03_agent_sdk.md) | Building Agents with the Claude Agent SDK | Sep 2025 |
| 04 | [04_long_running_agents.md](04_long_running_agents.md) | Effective Harnesses for Long-Running Agents | Nov 2025 |

### Context Engineering
| # | File | Article | Date |
|---|------|---------|------|
| 05 | [05_context_engineering.md](05_context_engineering.md) | Effective Context Engineering for AI Agents | Sep 2025 |

### Tool Design & MCP
| # | File | Article | Date |
|---|------|---------|------|
| 06 | [06_writing_effective_tools.md](06_writing_effective_tools.md) | Writing Effective Tools for Agents | Sep 2025 |
| 07 | [07_advanced_tool_use.md](07_advanced_tool_use.md) | Introducing Advanced Tool Use | Nov 2025 |
| 08 | [08_code_execution_mcp.md](08_code_execution_mcp.md) | Code Execution with MCP | Nov 2025 |
| 09 | [09_think_tool.md](09_think_tool.md) | The "Think" Tool | Mar 2025 |
| 10 | [10_agent_skills.md](10_agent_skills.md) | Agent Skills | Dec 2025 |
| 19 | [19_desktop_extensions.md](19_desktop_extensions.md) | Desktop Extensions | Jun 2025 |

### Evaluation & Testing
| # | File | Article | Date |
|---|------|---------|------|
| 11 | [11_demystifying_evals.md](11_demystifying_evals.md) | Demystifying Evals for AI Agents | Jan 2026 |
| 12 | [12_infrastructure_noise.md](12_infrastructure_noise.md) | Infrastructure Noise in Evals | Feb 2026 |
| 13 | [13_ai_resistant_evaluations.md](13_ai_resistant_evaluations.md) | AI-Resistant Technical Evaluations | Jan 2026 |

### Production & Security
| # | File | Article | Date |
|---|------|---------|------|
| 14 | [14_sandboxing.md](14_sandboxing.md) | Claude Code Sandboxing | Oct 2025 |
| 15 | [15_postmortem.md](15_postmortem.md) | Postmortem of Three Recent Issues | Sep 2025 |
| 16 | [16_parallel_c_compiler.md](16_parallel_c_compiler.md) | Building a C Compiler with Parallel Claudes | Feb 2026 |

### RAG & Retrieval
| # | File | Article | Date |
|---|------|---------|------|
| 17 | [17_contextual_retrieval.md](17_contextual_retrieval.md) | Introducing Contextual Retrieval | Sep 2024 |

### Benchmarks & Best Practices
| # | File | Article | Date |
|---|------|---------|------|
| 18 | [18_swe_bench.md](18_swe_bench.md) | Raising the Bar on SWE-bench Verified | Jan 2025 |
| 20 | [20_claude_code_best_practices.md](20_claude_code_best_practices.md) | Claude Code Best Practices | Apr 2025 |
| 21 | [21_claude_4_best_practices.md](21_claude_4_best_practices.md) | Claude 4.6 Prompting Best Practices | Docs |

## Key Framings Across All Articles

1. **"Simple, composable patterns rather than complex frameworks"** — agent design philosophy
2. **"Smallest possible set of high-signal tokens"** — context engineering objective
3. **"Tools are a contract between deterministic and non-deterministic systems"** — tool design as new discipline
4. **"ACI deserves same rigor as HCI"** — agent-computer interface design
5. **"Token usage explains 80% of variance"** — multi-agent research quality
6. **"Leaderboard differences below 3% deserve skepticism"** — eval noise
7. **"Teams without evals face reactive loops"** — eval investment case
8. **"The shift-change problem"** — long-running agent memory loss
9. **"Context rot"** — performance degrades as context grows
10. **"Prioritize execution over deliberation"** — Claude 4.6 antidote
