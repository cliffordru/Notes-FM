# STANDUP v1.0.0

Generate a standup summary from recent git activity, open PRs, and in-progress work items.

## Prerequisites

- Azure CLI (`az`) with DevOps extension installed and authenticated (@.agents/skills/ado/SKILL.md)
- Azure DevOps organization and project configured

## Steps

1. Get recent commits across all local branches (Friday if today is Monday, otherwise yesterday):
   ```powershell
   $dayOfWeek = (Get-Date).DayOfWeek.value__
   if ($dayOfWeek -eq 1) { $since = "last friday 00:00" } else { $since = "yesterday 00:00" }
   git log --all --since=$since --until="today 00:00" --author="$(git config user.email)" --oneline
   ```
2. Get open PRs authored by the current user:
   ```powershell
   az repos pr list --creator (az ad signed-in-user show --query userPrincipalName -o tsv) --status active
   ```
3. Get in-progress work items assigned to the current user:
   ```powershell
   az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] = 'Active' ORDER BY [System.ChangedDate] DESC"
   ```
4. Synthesize into a standup blurb

## Output

Format the output as a ready-to-paste standup message:

```
**Yesterday**
- [summarized work from commits/PRs]

**Today**
- [derived from open PRs and in-progress work items]

**Blockers**
- None (or list any if inferable from PR comments/CI status)
```

Keep it concise — 1-2 bullet points per section. Do not include raw commit hashes or ticket IDs unless they add clarity.
