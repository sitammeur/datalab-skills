# AGENTS.md

Guidelines for AI agents working in this repository.

## Repository Overview

This repository contains **Agent Skills** for AI agents following the [Agent Skills specification](https://agentskills.io/specification.md). It focuses on Datalab integration for PDF and image form-filling capabilities.

- **Name**: Datalab Skills
- **GitHub**: https://github.com/sitammeur/datalab-skills
- **Creator**: Sitam Meur
- **License**: MIT

## Repository Structure

```
datalab-skills/
├── skills/                   # Agent Skills
│   └── form-filling/
│       ├── SKILL.md          # frontmatter + instructions
│       ├── references/       # Datalab SDK documentation
│       │   └── api-reference.md
│       └── scripts/          # executable Datalab Python code
│           ├── fill_form.py
│           └── sample_field_data.json
├── LICENSE
└── README.md
```

## Build / Lint / Test Commands

**Not applicable** - This is a content-only repository with no executable code to build.

Verify manually:

- YAML frontmatter is valid
- `name` field matches directory name exactly
- `name` is 1-64 chars, lowercase alphanumeric and hyphens only
- `description` is 1-1024 characters

## Agent Skills Specification

Skills follow the [Agent Skills spec](https://agentskills.io/specification.md).

### Required Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

### Frontmatter Field Constraints

| Field         | Required | Constraints                                                    |
| ------------- | -------- | -------------------------------------------------------------- |
| `name`        | Yes      | 1-64 chars, lowercase `a-z`, numbers, hyphens. Must match dir. |
| `description` | Yes      | 1-1024 chars. Describe what it does and when to use it.        |
| `license`     | No       | License name (default: MIT)                                    |
| `metadata`    | No       | Key-value pairs (author, version, etc.)                        |

### Name Field Rules

- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match parent directory name exactly

**Valid**: `form-filling`
**Invalid**: `Form-Filling`, `-form`, `form--filling`

### Skill Directory Structure

```
skills/skill-name/
├── SKILL.md        # Required - main instructions (<500 lines)
├── references/     # Optional - detailed docs loaded on demand
├── scripts/        # Optional - executable code
└── assets/         # Optional - templates, data files
```

## Current Skills

### form-filling

Fill PDF and image forms using the Datalab Python SDK. Supports single and batch form operations with async processing.

**Triggers**: form filling, PDF forms, fillable documents, FormFillingOptions, batch fill forms

## Writing Style Guidelines

### Structure

- Keep `SKILL.md` under 500 lines (move details to `references/`)
- Use H2 (`##`) for main sections, H3 (`###`) for subsections
- Use bullet points and numbered lists liberally
- Short paragraphs (2-4 sentences max)

### Tone

- Direct and instructional
- Second person ("You are a form-filling specialist")
- Professional but approachable

### Formatting

- Bold (`**text**`) for key terms
- Code blocks for examples and templates
- Tables for reference data
- No excessive emojis

### Clarity Principles

- Clarity over cleverness
- Specific over vague
- Active voice over passive
- One idea per section

### Description Field Best Practices

The `description` is critical for skill discovery. Include:

1. What the skill does
2. When to use it (trigger phrases)
3. Related skills for scope boundaries

```yaml
description: Fill PDF and image forms using the Datalab Python SDK. Triggers: form filling, PDF forms, fillable documents, FormFillingOptions, batch fill forms.
```

## Skills

See `README.md` for the current skill. When adding new skill, follow the naming patterns of existing one.
