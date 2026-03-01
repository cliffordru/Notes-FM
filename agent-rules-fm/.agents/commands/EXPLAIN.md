# EXPLAIN v1.0.1

Produce a plain-English explanation of a file, function, class, or Azure Boards work item — including what it does, why it exists, and how it fits into the larger system.

## Prerequisites

- Azure CLI (`az`) with DevOps extension for work item access (@.agents/skills/azure-boards/SKILL.md)

## Usage

```
/EXPLAIN <target>
```

Where `<target>` is one of:

- A file path (e.g., `app/models/user.rb`)
- A function or class name (e.g., `UserAuthService`)
- An Azure Boards work item ID (e.g., `12345`)
- A concept or question (e.g., "how does billing work?")

Ask the user for a target if not provided.

## Steps

1. Identify what the target is (file, symbol, work item, or concept)
2. If a work item: fetch details using the Azure Boards skill (@.agents/skills/azure-boards/SKILL.md), then locate the relevant code
3. If a file or symbol: read the code and trace its callers, dependencies, and data flow
4. If a concept: search the codebase for relevant files and entry points
5. Synthesize findings into a layered explanation

## Output

```
## Explanation: [target]

### What it does
[1-3 sentence plain-English summary]

### Why it exists
[The problem it solves or the requirement it fulfills]

### How it works
[Step-by-step walkthrough of key logic — no jargon, no line-by-line narration]

### How it fits in
[Where it sits in the larger system: what calls it, what it calls, what it affects]

### Key files
- [file path] — [one-line description of its role]

### Gotchas / non-obvious things
- [anything surprising, legacy, or easy to misunderstand]
```

Tailor the depth to the complexity of the target. A single function needs 3-4 sentences; a subsystem may need all sections.
