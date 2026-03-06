# DAILY-STATUS v1.1.0

Query Jira for in-progress work across SRE Core, SRE Consulting, and InfoSec, then write a fresh daily status summary to `1-meetings/1-daily-status.md`. Replaces the file contents entirely each run. Includes parent epic and labels for each ticket.

## Prerequisites

- `acli` installed and authenticated to Jira (`acli jira auth status`)
- See the [Atlassian skill](.cursor/skills/atlassian/SKILL.md) if setup is needed

## Usage

```
/DAILY-STATUS
```

No arguments required.

## Steps

1. Verify `acli` is authenticated: run `acli jira auth status`. If not authenticated, follow the Atlassian skill to authenticate before proceeding.
2. Run the following Python script to fetch all in-progress tickets with parent and labels in parallel. The `search` command does not support `parent` as a field, so individual `view --json` calls are required per ticket.

```python
import subprocess, json, concurrent.futures

PROJECTS = {
    "SRE Core": "SRE",
    "SRE Consulting": "HELP",
    "InfoSec": "SEC"
}

def search(project_key):
    result = subprocess.run(
        ["acli", "jira", "workitem", "search",
         "--jql", f"project = {project_key} AND status = 'In Progress' ORDER BY updated DESC",
         "--fields", "key,summary,assignee,priority,labels",
         "--limit", "50", "--json"],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data if isinstance(data, list) else data.get("issues", [])

def fetch_issue(key):
    result = subprocess.run(
        ["acli", "jira", "workitem", "view", key, "--fields", "*all", "--json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

all_keys = {}
for name, key in PROJECTS.items():
    issues = search(key)
    all_keys[name] = [(i["key"], i["fields"]) for i in issues]

flat_keys = [k for issues in all_keys.values() for k, _ in issues]
details = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futures = {ex.submit(fetch_issue, k): k for k in flat_keys}
    for f in concurrent.futures.as_completed(futures):
        k = futures[f]
        details[k] = f.result()
```

3. Parse the results: for each ticket extract `summary`, `assignee.emailAddress`, `priority.name`, `labels` (list), and `parent` (key + summary if present, else "none").
4. Note any unassigned tickets, individuals carrying many tickets, thematic clusters, or RCA/incident-linked work worth calling out.
5. Write the output (replacing all existing content) to `/1-meetings/1-daily-status.md` using the format below.

## Output Format

```markdown
# Daily Status - YYYY-MM-DD

## SRE Core (N in progress)

**[Priority]**
- **[KEY]** - [Summary] _([assignee-email-prefix] or unassigned)_ | parent: [PARENT-KEY: Parent Summary or none] | labels: `label1`, `label2` (or none)

**[Priority]**
- ...

## SRE Consulting (N in progress)

- **[KEY]** - [Summary] _([assignee-email-prefix] or unassigned)_ | parent: [PARENT-KEY: Parent Summary or none] | labels: `label1` (or none)
- ...

## InfoSec (N in progress)

- **[KEY]** - [Summary] _([assignee-email-prefix] or unassigned)_ | parent: [PARENT-KEY: Parent Summary or none] | labels: `label1` (or none)
- ...

## Notable

- [Optional: call out clusters, unassigned items, a person carrying many tickets, RCA/incident-linked work, or thematic patterns]
```

## Rules / Notes

- Use today's date (not a placeholder) in the heading.
- Group SRE Core items by priority (High, Medium, Low). Skip a priority group if no tickets fall under it.
- For SRE Consulting and InfoSec, a flat list is fine since all items tend to be Medium priority - omit the priority grouping unless meaningful variation exists.
- Assignee display: use the email prefix . For unassigned tickets, write `unassigned` in italics.
- Parent display: show as `KEY: Summary` (e.g. `SRE-354: Upgrade terraform-infrastructure TF and providers`). If no parent, write `none`.
- Labels display: wrap each label in backticks, comma-separated. If no labels, write `none`.
- Ticket titles containing `[Analyst]` or similar role prefixes should be preserved as-is in the summary.
- The Notable section is optional - only include it if there is something genuinely worth flagging (e.g., 3+ tickets on one person, a named blocker visible from ticket titles, an unassigned ticket that looks urgent).
- Do not include a preamble, explanation, or commentary outside the document itself. Write the file and confirm to the user that it has been updated.
- Project keys: SRE Core = `SRE`, SRE Consulting = `HELP`, InfoSec = `SEC`.
