
# COMMIT v1.1.0

I would like for you to create a commit message for the staged and unstaged changes on this branch. Look at the code that is unique to this branch and generate a commit message for it. Then stage the changes and commit them -- do not push to remote.

## Commit Message Rules

Format: `<TICKET-NUMBER>(<type>): <summary>`

Where:

- TICKET-NUMBER: Work item ID from branch name (e.g., 12345) or Azure Boards work item
- type: feat, fix, chore, refactor, test, docs
- summary: imperative present tense, concise

Example:

```powershell
git commit -m "12345(feat): add user authentication
- implement JWT token validation
- add login endpoint"
```

Once you're done, remind the user to push their changes.
