# How to Build Agent Commands

A guide for building new slash commands for the `.agents/commands/` directory. Use this as a prompt or reference when asking an AI agent to create a new command.

---

## What a Command Is

A command is a Markdown file in `.agents/commands/` that tells an AI agent exactly how to perform a repeatable task. When a user types `/COMMAND-NAME`, the agent reads this file and follows it.

Commands are:
- **Imperative** - written as instructions to the agent, not descriptions
- **Scoped** - one command does one thing well
- **Self-contained** - include everything the agent needs to execute without asking clarifying questions (except where user input is genuinely required)

---

## Prompt to Give an AI Agent

Use this prompt to have an agent build a new command for you:

```
I want you to create a new agent command file at:
  .agents/commands/<COMMAND-NAME>.md

First, read several existing commands in .agents/commands/ to understand the format and tone.
Then build the new command using the structure and rules below.

The command should do the following:
  [DESCRIBE WHAT THE COMMAND SHOULD DO IN PLAIN ENGLISH]

Key behaviors:
  - [behavior 1]
  - [behavior 2]
  - [any constraints, output format requirements, or edge cases]

Follow the command format defined in HOW-TO-BUILD-COMMANDS.md.
```

---

## File Structure

Every command file follows this structure (omit sections that don't apply):

```markdown
# COMMAND-NAME v1.0.0

One sentence describing what this command does and when to use it.

## Prerequisites

- [Tool or credential required, with link to skill if relevant]
- Omit this section if there are no prerequisites

## Usage

\```
/COMMAND-NAME <required-arg> [optional-arg]
\```

Where `<required-arg>` is [description]. Ask the user if not provided.

## Steps

1. [First thing the agent does]
2. [Second thing]
3. [Ask user for approval before destructive or irreversible actions]
4. [Final step]

## Output

[Describe what the agent produces - a file, a message, a PR, etc.]

Optionally include an output template:

\```
## Section Title
[content]
\```

## Rules / Notes

- [Any constraints, edge cases, or decision rules the agent must follow]
- [What to skip, what to never omit, merge behavior, naming conventions, etc.]
```

---

## Writing Good Steps

Steps should be specific enough that the agent doesn't have to guess. Ask yourself: if the agent followed these steps literally, would it do the right thing?

**Too vague:**
> 2. Summarize the content

**Good:**
> 2. Read the full file before writing anything. Extract: decisions made, action items (with owner), resources shared, constraints, and open questions. Group by topic.

**Patterns to use:**
- "Read X before doing Y" - prevents the agent from starting before it has full context
- "Ask the user for approval before writing" - gates destructive or hard-to-reverse actions
- "If X exists, do Y; otherwise do Z" - handles branching logic explicitly
- "Omit this section if there is no content" - prevents empty scaffolding in output
- "Ask the user for `<arg>` if not provided" - makes usage forgiving

---

## Output Sections

If the command produces a document, define its structure explicitly in an `## Output` section using a fenced code block. Include placeholder text like `[one sentence summary]` so the agent knows the expected level of detail.

Put the most important information first in the output - summary/takeaways before details.

---

## Preservation and Merge Rules

If the command reads or modifies existing files, be explicit about:
- What must never be removed or omitted
- What can be skipped (filler, duplicates, low-signal content)
- How to merge with existing content (append-only, replace, diff-and-add)
- How to handle conflicts or stale content

---

## Naming Conventions

- Filename: `SCREAMING-KEBAB-CASE.md` (e.g., `OPEN-PR.md`, `EXTRACT-KB.md`)
- Command name in the H1 heading matches the filename without `.md`
- Version starts at `v1.0.0`; increment minor for behavior changes, patch for wording fixes

---

## Examples of Commands Built Here

| Command | What it does |
|---|---|
| `SUMMARIZE-TRANSCRIPT.md` | Converts a raw meeting transcript into a structured summary with takeaways and resources at the top. Never loses decisions, action items, constraints, or named blockers. |
| `EXTRACT-KB.md` | Reads any source file, extracts durable reusable knowledge, and merges it into topic-based files under `0-kb/`. Shows a plan for approval before writing. |
| `SPIKE.md` | Investigates a Jira ticket or question, explores the codebase, and produces a structured technical spike with options and a recommendation. |
| `DRY-MD.md` | Rewrites a Markdown file to remove duplication while preserving every unique fact. Requires user approval before overwriting. |
| `STANDUP.md` | Generates a ready-to-paste standup from recent git activity, open PRs, and in-progress Jira tickets. |

---

## Checklist Before Saving a New Command

- [ ] One-sentence description at the top makes the purpose clear
- [ ] Steps are specific enough to follow without guessing
- [ ] User input points are explicit ("ask if not provided")
- [ ] Destructive steps require user approval
- [ ] Output format is defined if the command produces a document
- [ ] Preservation/merge rules are stated if the command touches existing files
- [ ] No sections are left empty - omit sections that don't apply
