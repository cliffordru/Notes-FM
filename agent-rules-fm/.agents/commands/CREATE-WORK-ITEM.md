````markdown
# CREATE-WORK-ITEM v1.0.0

Create a new Azure Boards work item using the Azure Boards skill (@.agents/skills/azure-boards/SKILL.md). If the user has not provided a description, ask them for it.

The expected usage is:

```
@CREATE-WORK-ITEM <description>
```

## Prerequisites

- Azure CLI (`az`) with DevOps extension installed and authenticated (@.agents/skills/azure-boards/SKILL.md)
- Azure DevOps project configured

## REQUIRED INFORMATION:

- Work item type (Task, Bug, User Story, Feature - ask if not provided)
- Title/Description (ask if not provided)
- Parent work item ID (optional - ask if creating a subtask)
- Assigned to (default to @Me unless specified)

## STEPS:

1. Determine the work item type:
   - **Bug**: For defects or issues
   - **Task**: For work to be done
   - **User Story**: For user requirements
   - **Feature**: For larger capabilities
   
2. Using the user's description as a guide, create the work item with appropriate fields:
   ```powershell
   az boards work-item create --title "<title>" --type "<type>" --assigned-to "@Me" --description "<description>"
   ```

3. If this is a subtask, link it to the parent:
   ```powershell
   az boards work-item relation add --id <new-work-item-id> --relation-type "Parent" --target-id <parent-id>
   ```

4. Analyze the codebase relative to the user's description (if applicable):
   - Search for related files and functionality
   - Identify implementation areas
   - Note any existing patterns or conventions to follow

5. Update the work item with additional details:
   ```powershell
   az boards work-item update --id <work-item-id> --fields "Microsoft.VSTS.Common.AcceptanceCriteria=<criteria>"
   ```
   
   Include:
   - **Acceptance Criteria**: Clear, testable conditions for completion
   - **Reproduction Steps** (for bugs): Step-by-step instructions
   - **Code Insights**: Relevant files, patterns, or implementation notes
   - **Tags**: Add relevant tags for categorization

## OUTPUT:

Provide the created work item details:

```
✅ Work Item Created Successfully!

🆔 Work Item ID: [ID]
📋 Type: [Bug/Task/User Story/Feature]
📝 Title: [Title]
🔗 URL: [Azure DevOps URL]

📌 Details:
- Assigned to: [User]
- State: [New/Active]
- Parent: [Parent ID if applicable]

✏️ Acceptance Criteria:
[List of criteria]

💡 Implementation Notes:
[Code insights and recommendations]

🏷️ Tags: [tag1, tag2, tag3]
```

## Example Usage:

**User Input:**
```
@CREATE-WORK-ITEM Fix login validation to allow email addresses with plus signs
```

**System Response:**
```
✅ Work Item Created Successfully!

🆔 Work Item ID: 12345
📋 Type: Bug
📝 Title: Fix login validation to allow email addresses with plus signs
🔗 URL: https://dev.azure.com/YourOrg/YourProject/_workitems/edit/12345

📌 Details:
- Assigned to: Cliff Gray
- State: New
- Priority: 2

✏️ Acceptance Criteria:
- Email validation accepts addresses containing "+" character
- Existing users with "+" in email can log in successfully
- Unit tests added for email validation edge cases
- No regression in existing email validation

💡 Implementation Notes:
- Check email validation logic in: scripts/IdentityProvider/
- Update regex pattern to include "+" as valid character
- Test with common patterns: user+tag@domain.com

🏷️ Tags: authentication; validation; email
```

## Tips:

- Be specific with acceptance criteria - they should be testable
- For bugs, include reproduction steps in the description
- Link related work items when creating subtasks
- Add appropriate tags for better organization and filtering
- Set priority based on impact and urgency (1-4, where 1 is highest)

````