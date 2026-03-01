# Custom Context System

This directory allows you to customize AI agent behavior at multiple levels.

## GitHub Copilot (VS Code)

This repository uses GitHub Copilot with custom commands and skills:

- **Commands**: Type `@command-name` in Copilot Chat (e.g., `@standup`, `@review`, `@commit`)
- **Skills**: Tool-specific guidance in `.agents/skills/` directory
- **Instructions**: `.github/copilot-instructions.md` provides automatic repo context

See folder structure below for customization options.

## Configuration Hierarchy

AI agents read context in this priority order:

| Level | File Location | Purpose | Scope | Version Controlled | Synced |
| ----- | ------------ | ------- | ----- | ----------------- | ------ |
| 1. OS | `~/.agents/AGENTS.md` → tool symlinks* | Broad guidance: code quality, commit style, general preferences | All projects on your machine | Optional (self-managed) | Via setup script |
| 2. Repo | `<repo>/AGENTS.md` | Team conventions, repo architecture, shared standards | **All repos** | ✅ Yes | Via agent-sync |
| 3. Repo-Specific | `<repo>/.agents/REPO_RULES.md` | Repo gotchas, conventions, patterns | This repository only | ✅ Yes | Via agent-sync |
| 4. Team | `<repo>/.agents/TEAM_RULES.md` | Team conventions, shared offline | This repository only | ❌ No (gitignored) | Manual |
| 5. Personal | `<repo>/.agents/USER_RULES.md` | Your personal preferences, workflow style | This repository only | ❌ No (gitignored) | Manual |

*See [OS-Level](#os-level-optional) section below for symlink details.

**Key principle**: Higher levels take precedence — last file read wins on conflicts. Lower levels are additive and supplement higher levels.

## Customization Layers

### OS-Level (Optional)

For rules that apply to all your projects, use OS-level configuration. AI coding assistants (Claude, Codex, Gemini) each read from different default paths, so we symlink them to `~/.agents/AGENTS.md` for a single source of truth.

**Tool-specific locations**:

- Claude: `~/.claude/CLAUDE.md`
- Gemini: `~/.gemini/GEMINI.md`
- Codex: `~/.codex/CODEX.md`

Unfortunately, Cursor does not support OS-level file-based setup - it only supports repository-level. For OS-level Cursor rules, manually add them via Cursor Settings → Rules → User Rules.

**Setup**:

1. Clone agent-rules (if not already):

   TODO - will fill in later

   ```bash
   cd ~/repos
   git clone https://github.com/../agent-rules.git
   ```

2. Run the setup script to create `~/.agents/AGENTS.md` and symlinks:

   TODO
   ```bash
   ~/../agent-rules/bin/local-os-agent-setup.sh
   ```

### Repo-Level (AGENTS.md)

Shared across all repos via agent-sync. Contains team conventions, repo architecture, and shared standards.

### REPO_RULES.md

Created automatically by `agent-sync`. Add repository-specific conventions, architecture notes, and known gotchas here. Version-controlled and shared across the team.

### USER_RULES.md (Optional)

Personal AI customization (gitignored):

```bash
cp .agents/USER_RULES.md.example .agents/USER_RULES.md
```

Use for: coding style, workflow preferences, experiments, personal reminders.

### TEAM_RULES.md (Optional)

Team conventions shared offline (gitignored):

```bash
cp .agents/TEAM_RULES.md.example .agents/TEAM_RULES.md
```

Use for: code review guidelines, testing standards, team workflows.

### LEARNING_LOG.md (Optional)

Agent-writable log of discovered patterns (gitignored, opt-in):

```bash
cp .agents/LEARNING_LOG.md.example .agents/LEARNING_LOG.md
```

Agents create this automatically when discovering patterns. Engineers can seed it with known patterns.

## Contributing

Found a useful pattern that should be shared?

**Workflow:**

1. **Experiment** locally in `USER_RULES.md` or `TEAM_RULES.md`
2. **Validate** it works in real usage over several sessions
3. **Upstream** via PR:
   - **Repo-specific patterns** → Add to this repo's `.agents/REPO_RULES.md`
   - **Broadly useful patterns** → Submit PR to [agent-rules](https://github.com/../agent-rules) to add to `AGENTS.md`
4. **Benefit everyone** - Your improvement syncs to all repos via `agent-sync`

See the readme for contribution guidelines.
