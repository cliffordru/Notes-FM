# REVIEW v1.0.0

Self-review the current branch's changes before opening a pull request.

## Steps

1. Get the diff of all changes unique to this branch vs `main`
2. For each changed file, check for:
   - Debug statements (`Write-Host`, `Write-Debug`, `console.log`, `debugger`, `binding.pry`)
   - Hardcoded values that should be constants or config
   - TODO/FIXME comments introduced in this branch (flag, don't remove)
   - Missing or incomplete test coverage for changed logic
   - Dead code or unused variables/methods introduced
   - Inconsistency with surrounding code style or conventions
   - Public interface changes that may affect callers
3. Cross-reference changes against the linked work item (if branch name contains a work item ID) to verify acceptance criteria appear to be met
4. Produce a structured review summary

## Output

```
## Self-Review Summary

### ✅ Looks good
- [items that are clean]

### ⚠️ Concerns (address before review)
- [file:line] description of issue

### 💬 Notes for reviewers
- [anything worth calling out in the PR description]
```

Offer to fix any flagged concerns automatically where safe.
