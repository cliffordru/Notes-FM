# SUMMARIZE-TRANSCRIPT v1.0.0

Summarize a raw meeting transcript into a structured document that preserves all decisions, action items, context, and technical detail. Takeaways and resources always appear at the top.

## Usage

```
/SUMMARIZE-TRANSCRIPT <transcript-file>
```

Where `<transcript-file>` is a raw transcript `.md` (or `.txt`) file. Ask the user for the path if not provided.

## Steps

1. Read the full transcript from top to bottom before writing anything
2. Extract and categorize every substantive piece of information:
   - Decisions made (explicit or implicit)
   - Action items (who owns what)
   - Resources shared (links, docs, repos, code references)
   - Technical context, constraints, and open questions
   - Named participants and their roles/affiliations where stated
3. Identify key takeaways - the 2-5 most important outcomes a reader needs to know immediately
4. Note any constraints or blockers mentioned (e.g. product objections, missing support, fork risk)
5. Write the summary following the output format below
6. Ask the user: save as a new file next to the transcript? (suggested name: `<date>-summary-<meeting-name>.md`)

## Preservation Rules

Preserve every unique fact, decision, constraint, name, risk, number, and quote that has meaningful signal.

### Allowed omissions
- Pure filler ("um", "uh", false starts, social pleasantries)
- Exact repetitions that add no new information
- Side jokes or banter with no technical or organizational content

### Never omit
- Decisions, even tentative ones
- Action items, even informal ones ("I'll take that as a note")
- Named blockers or constraints (including political/organizational ones like "product thinks X is a competitor")
- Numeric specifics (customer counts, percentages, timeframes)
- Resources shared (links, doc references, code pointers)
- Disagreements or corrections made during the meeting
- Open questions left unresolved

## Output Format

```markdown
## Takeaways

- [2-5 bullet points: the most critical outcomes/decisions a reader needs immediately]

## Resources

- [Link or doc title](url) - brief description of what it covers
- ...

## Decisions

- **[Decision]:** [detail and rationale] - owner if named

## Action Items

- **[Person]:** [what they committed to do] - context/deadline if stated
- ...

## Technical Discussion

### [Topic A]

- [Key points, constraints, open questions grouped under this topic]

### [Topic B]

- ...

## Open Questions

- [Unresolved items that need follow-up, with who needs to answer if known]

## Participants

- [Name] - [role/team if mentioned]
- ...
```

## Notes

- If the transcript spans multiple topics, use one `### Topic` subsection per topic under Technical Discussion
- If a constraint was mentioned (political, technical, or organizational), capture it in the relevant topic section - do not bury or omit it
- If a number was mentioned (customers, percentages, latency, cost), include it verbatim
- Prefer the speaker's own words for decisions and action items over paraphrasing
- If something was flagged as a risk (even informally), note it
