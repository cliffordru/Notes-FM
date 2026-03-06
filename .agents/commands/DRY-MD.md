

# DRY-MD v1.0.0

Rewrite a Markdown file to be DRY, token-efficient, and useful while preserving every unique fact, example, name, claim, decision, ask, and quote. Prioritize clarity and usefulness over brevity.

## Usage

```
/DRY-MD <target>
```

Where `<target>` is a `.md` file (README, AGENTS, CLAUDE, etc.) or directory containing markdown files. Ask the user for a file path if not provided.

## Steps

1. Read the target file
2. Extract atomic points from the source
3. Delete exact and near-duplicate ideas per the preservation rules below
4. Group remaining points into H2 themes, each idea under the single most relevant H3
5. Write each point as a short paragraph, bullet, or step
6. Re-check: no idea appears in more than one section, bullet, or heading
7. Run a markdown linter on the result and fix any issues
8. Present the rewritten file to the user for approval before overwriting

## Preservation Rules

Preserve every unique fact, example, name, claim, decision, ask, and quote.

### Allowed removals

- Exact repeats and near-repeats that add no new information
- Paraphrases merged into one item, keeping the most specific wording
- Rhetorically meaningful repetition kept once and tagged: (repeated emphasis in source)

## Formatting

- Hierarchical markdown structure using H1-H3
- Prefer short paragraphs, bullets, and numbered steps
- One idea per bullet, ideally one line
- Nesting: max depth 2, prefer 1. Use a new H3 instead of deep sub-bullets
- Use tables when they improve clarity over lists or prose

## Placement

- Every idea appears once, in the best place
- Move content to the right section instead of copying it
- Keep supporting details close to the claim they support

## Output

Present the full rewritten file contents to the user. After user approval, overwrite the original file.
