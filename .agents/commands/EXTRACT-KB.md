# EXTRACT-KB v1.0.0

Analyze a file and extract durable, reusable knowledge into topic-based `.md` files under `/0-kb/`. Merges into existing KB files when the topic already exists; creates new files for new topics.

## Usage

```
/EXTRACT-KB <source-file>
```

Where `<source-file>` is any `.md`, `.txt`, transcript, summary, spike, or notes file. Ask the user for the path if not provided.

## What counts as KB-worthy

Extract knowledge that is:
- Durable - still true weeks or months from now (not tied to a single task or sprint)
- Reusable - useful context for future decisions, onboarding, or investigation
- Non-obvious - not something any engineer would already know

### Examples of KB-worthy content
- How a system or integration works (architecture, data flow, constraints)
- Vendor/carrier relationships, capabilities, and known limitations
- Organizational context (team ownership, product stances, known blockers)
- Regulatory or compliance requirements (FCC mandates, carrier rules)
- Historical context for past decisions ("we tried X and it worked 25% of the time")
- Named gotchas, edge cases, or failure modes

### Examples of what to skip
- Task-specific action items or sprint work
- Meeting logistics or social content
- Information that is already captured in the KB file without adding new detail

## Steps

1. Read the full source file
2. List all existing KB files in `/0-kb/` and read any that are plausibly related to topics in the source
3. Identify all KB-worthy facts, decisions, and context in the source file
4. Group extracted knowledge by topic
5. For each topic:
   - If a matching KB file exists: plan additions, checking each item against existing content to avoid redundancy
   - If no matching KB file exists: plan a new file with a clear, lowercase-hyphenated name (e.g., `sms-delivery.md`, `ringswitch-sip.md`, `freeswitch.md`)
6. Present the proposed changes to the user before writing:
   - List each file to be created or updated
   - Show a brief summary of what will be added to each
   - Ask for approval
7. After approval, write all files

## KB File Format

Each KB file should follow this structure:

```markdown
# [Topic Title]

_Last updated: YYYY-MM-DD_

## Overview

[1-3 sentences: what this topic covers and why it matters]

## Key Facts

- [Durable fact or constraint]
- [Named limitation, vendor behavior, or gotcha]
- ...

## How It Works

[Optional: architecture or flow description if relevant]

## History & Decisions

- **[Date if known]:** [Decision made, why, and outcome] - source if known
- ...

## Open Questions

- [Things that were unknown at time of writing]

## References

- [Link or file](url-or-path) - what it covers
```

Omit sections that have no content. Keep each bullet to one clear idea.

## Naming Conventions

- Filenames: lowercase, hyphen-separated, specific but not too narrow
- Prefer broad topic files over highly specific ones (e.g., `sms-delivery.md` not `t-mobile-spam-2026-03.md`)
- A good test: would an engineer searching for this topic find the file by its name?

## Merge Rules

When adding to an existing file:
- Add new facts only - do not restate what is already there
- Append to the relevant section, or add a new section if the topic is genuinely new
- Update `_Last updated_` date
- Never remove existing content unless it is factually incorrect (flag it to the user instead)
