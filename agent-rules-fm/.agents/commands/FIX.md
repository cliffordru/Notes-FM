# FIX v1.1.2

## Prerequisites

- Azure CLI (`az`) with DevOps extension installed and authenticated (@.agents/skills/ado/SKILL.md)
- Azure Boards work items accessible (@.agents/skills/azure-boards/SKILL.md)

## Execution Steps

### 1. Fetch Work Item Details

- Use the Azure Boards skill (@.agents/skills/azure-boards/SKILL.md) to retrieve work item details for the provided work item ID
- Command: `az boards work-item show --id <work-item-id>`
- Extract: title, description, acceptance criteria, and any technical requirements
- Confirm with user: "I found work item [WORK-ITEM-ID]: [TITLE]. Proceeding with implementation."

### 2. Create Feature Branch

- **Branch naming convention**: `<work-item-id>/<short-description>`
  - Example: `12345/fix-login-validation`
  - Use lowercase with hyphens, keep description concise (3-5 words max)
- **Commands**:
  ```powershell
  git checkout main
  git pull origin main
  git checkout -b <work-item-id>/<short-description>
  ```
- Confirm branch creation with user

### 3. Implement Changes

- Analyze the work item requirements
- Make necessary code changes to address the issue
- Follow existing code patterns and project conventions
- Add/update tests if applicable

### 4. Pre-Commit Validation

- Execute: `.agents/commands/PRE-COMMIT.md`
- **If issues found**:
  - List all issues clearly
  - Fix them automatically where possible
  - Re-run validation until clean
- **If validation passes**: Proceed to step 5

### 5. Commit Changes

- Stage all changes: `git add .`
- Execute: `.agents/commands/COMMIT.md` to generate and apply commit message
- Verify commit was successful

### 6. Push to Remote

- Push branch to remote:
  ```powershell
  git push origin <branch-name>
  ```
- Confirm successful push

### 7. Create Draft Pull Request

- Use the Azure DevOps CLI to create a PR with:
  - **Command**: `az repos pr create --draft true --source-branch <branch-name> --target-branch main --title "[WORK-ITEM-ID] <work item title>" --description "<PR description>"`
  - **Base branch**: `main` (or user-specified)
  - **Head branch**: The newly created branch
  - **Status**: DRAFT
  - **Title**: `[WORK-ITEM-ID] <work item title>`
  - **Body**: Populate with:
    - Work item link (automatically linked if ID in title)
    - Description from work item
    - Changes made
    - Testing steps
    - Any relevant notes
- Link work item: `az repos pr work-item add --id <pr-id> --work-items <work-item-id>`
- Set appropriate labels/tags if available (e.g., bug, feature, enhancement)

### 8. Final Confirmation

Provide the user with:

```
✅ Draft PR created successfully!

🔗 PR URL: [link]
📋 Work Item: [WORK-ITEM-ID]
🌿 Branch: [branch-name]

⚠️ NEXT STEPS (Human Review Required):
1. Review the code changes in the PR
2. Test the changes locally or in a preview environment
3. Verify all acceptance criteria are met
4. Update the PR description if needed
5. Mark as "Ready for Review" when satisfied
6. Request reviews from appropriate team members

This is a critical human-in-the-loop checkpoint to ensure quality before peer review.
```

## Error Handling

- **Work item not found**: "Unable to find work item [ID]. Please verify the work item ID and try again."
- **Git conflicts**: "There are merge conflicts with main. Please resolve them before proceeding."
- **Pre-commit failures**: List specific issues and attempt to fix, but escalate to user if unable to resolve automatically
- **Push failures**: Check for branch protection rules or permission issues
- **PR creation failures**: Verify Azure DevOps authentication and repository permissions

## Notes

- Always maintain a conversational tone and keep the user informed at each step
- If any step fails, provide clear error messages and suggested remediation
- Ask for clarification if work item details are ambiguous or incomplete
- Respect existing project conventions (commit message format, code style, etc.)
