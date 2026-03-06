

# FIX v1.1.3

## Prerequisites

- Atlassian CLI (`acli`) installed and authenticated (@.agents/skills/atlassian/SKILL.md)
- Github CLI (`gh`) installed and authenticated (@.agents/skills/gh/SKILL.md)

## Execution Steps

### 1. Fetch Jira Ticket Details

- Use the Atlassian skill (@.agents/skills/atlassian/SKILL.md) to retrieve ticket details for the provided ticket number
- Extract: title, description, acceptance criteria, and any technical requirements
- Confirm with user: "I found ticket [TICKET-NUM]: [TITLE]. Proceeding with implementation."

### 2. Create Feature Branch

- **Branch naming convention**: `<ticket-number>/<short-description>`
  - Example: `FOO-1234/fix-login-validation`
  - Use lowercase with hyphens, keep description concise (3-5 words max)
- **Commands**:
  ```bash
  git checkout main
  git pull origin main
  git checkout -b <ticket-number>/<short-description>
  ```
- Confirm branch creation with user

### 3. Implement Changes

- Analyze the Jira ticket requirements
- Make necessary code changes to address the issue
- Follow existing code patterns and project conventions
- Add/update tests if applicable

### 4. Pre-Commit Validation

- If you are Claude Code and have access to it, run `/simplify`.
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
  ```bash
  git push origin <branch-name>
  ```
- Confirm successful push

### 7. Create Draft Pull Request

- Use the GitHub skill to create a PR with:
  - **Base branch**: `main` (or user-specified)
  - **Head branch**: The newly created branch
  - **Status**: DRAFT
  - **Title**: `[TICKET-NUM] <Jira ticket title>`
  - **Body**: Use `PULL_REQUEST_TEMPLATE.md` and populate:
    - Jira ticket link
    - Description from ticket
    - Changes made
    - Testing steps
    - Any relevant notes
- Set appropriate labels if available (e.g., bug, feature, enhancement)

### 8. Final Confirmation

Provide the user with:

```
✅ Draft PR created successfully!

🔗 PR URL: [link]
📋 Jira Ticket: [TICKET-NUM]
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

- **Jira ticket not found**: "Unable to find ticket [NUM]. Please verify the ticket number and try again."
- **Git conflicts**: "There are merge conflicts with main. Please resolve them before proceeding."
- **Pre-commit failures**: List specific issues and attempt to fix, but escalate to user if unable to resolve automatically
- **Push failures**: Check for branch protection rules or permission issues
- **PR creation failures**: Verify GitHub authentication and repository permissions

## Notes

- Always maintain a conversational tone and keep the user informed at each step
- If any step fails, provide clear error messages and suggested remediation
- Ask for clarification if Jira ticket details are ambiguous or incomplete
- Respect existing project conventions (commit message format, code style, etc.)
