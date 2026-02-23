# Desktop Extensions: One-Click MCP Installation
**Date:** June 26, 2025
**URL:** https://www.anthropic.com/engineering/desktop-extensions
**Source:** Web-fetched Feb 2026

---

## Overview

Desktop Extensions (`.mcpb` files) eliminate friction from MCP server installation. One-click install: download, double-click, done.

## The Problem

Traditional MCP installation required:
- External runtimes (Node.js, Python)
- Manual JSON configuration editing
- Complex dependency resolution
- GitHub searches for server discovery
- Manual reinstallation for updates

## Technical Architecture

A `.mcpb` file is a ZIP archive containing:

```
extension.mcpb/
├── manifest.json    (required — metadata and configuration)
├── server/          (MCP implementation)
├── dependencies/    (bundled packages)
└── icon.png         (optional)
```

### Manifest
Defines human-readable info, feature declarations, user configuration requirements, runtime specs.

### Template Literals for Dynamic Values
- `${__dirname}` — extension installation directory
- `${user_config.key}` — user-provided settings
- `${HOME}`, `${TEMP}` — system environment variables

## Key Features

### Built-in Runtime
- Claude Desktop includes Node.js runtime
- Eliminates external dependency requirements
- Automatic updates when new versions release

### Secure Storage
- OS keychain storage for sensitive data (API keys)
- No plaintext credential storage

## Development Workflow

```bash
npx @anthropic-ai/mcpb init     # Generate manifest template interactively
npx @anthropic-ai/mcpb pack     # Validate and create .mcpb archive
```

## Open Ecosystem

- Complete MCPB specification open-sourced
- Packaging tools and reference implementations available
- Designed for universal adoption across AI desktop apps, not just Claude

---

## Applicability
- MCP server distribution
- Developer tooling for AI ecosystems
- Plugin/extension architecture design
- One-click deployment patterns
