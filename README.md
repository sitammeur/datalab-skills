# Datalab Skills

Skills for document form filling powered by the [Datalab](https://documentation.datalab.to/) Python SDK to be used by AI agents.

## What Are Skills?

Skills are markdown files that provide AI agents with specialized knowledge and workflows for specific tasks. When added to your project, AI agents recognize relevant contexts and applies the appropriate frameworks, scripts, and best practices. Skills follow the [Agent Skills Specification](https://agentskills.io/).

## Available Skills

| Skill        | Purpose                                               |
| ------------ | ----------------------------------------------------- |
| form-filling | Fill PDF and image forms using the Datalab Python SDK |

## Installation Options

**Option 1: CLI Install (Recommended)**

Use [npx skills](https://github.com/vercel-labs/skills) to install skills directly:

```bash
# Install all skills
npx skills add sitammeur/datalab-skills

# Install specific skills
npx skills add sitammeur/datalab-skills --skill form-filling

# List available skills
npx skills add sitammeur/datalab-skills --list
```

This automatically installs to your `.claude/skills/` directory.

**Option 2: Clone and Copy**

```bash
git clone https://github.com/sitammeur/datalab-skills.git
cp -r datalab-skills/skills/* .claude/skills/
```

**Option 3: Git Submodule**

```bash
git submodule add https://github.com/sitammeur/datalab-skills.git .claude/datalab-skills
```

Then reference the skill from `.claude/datalab-skills/skills/`.

**Option 4: Fork and Customize**

1. Fork this repository
2. Customize skills for your needs
3. Clone your fork into your projects

**Option 5: SkillKit (Multi-Agent)**

Use [SkillKit](https://github.com/rohitg00/skillkit) to install skills across multiple AI agents (Claude Code, Cursor, Copilot, etc.):

```bash
# Install all skills
npx skillkit install sitammeur/datalab-skills

# Install specific skills
npx skillkit install sitammeur/datalab-skills --skill form-filling

# List available skills
npx skillkit install sitammeur/datalab-skills --list
```

## Usage

Simply ask an AI agent to help with form-filling tasks:

- "Use my user-identity.pdf to collect my personal field data and fill fw9.pdf using the form-filling skill." → Uses **form-filling** skill

Or invoke the skill directly (Claude Code): `/form-filling`

## Contributing

Contributions are welcome! Found improvements or have new skills to add? Open a pull request.

## License

MIT - Use these skills however you want.
