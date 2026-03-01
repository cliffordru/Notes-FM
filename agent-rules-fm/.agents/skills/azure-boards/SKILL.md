````skill
---
name: azure-boards
version: 1.0.0
description: Use when working with Azure Boards using the Azure CLI (az boards), to get information about work items, create and manage tasks, bugs, user stories, and queries.
origin: 
read-only: true
---

# Azure Boards Skill using az boards (Command Line Interface)

## Prerequisites

- Azure CLI (`az`) with DevOps extension installed and authenticated
- Azure DevOps organization and project configured (see @.agents/skills/ado/SKILL.md)

## Overview

Azure Boards provides a rich set of capabilities for planning and tracking work, code defects, and issues using Kanban and Scrum methods. The Azure CLI provides command-line access to work items, queries, iterations, and more.

## Getting Started

Ensure you have Azure CLI with the DevOps extension installed and configured.

**Quick Setup**: Run the automated setup script (recommended):

```powershell
.agents\setup-ado.ps1
```

This will install the DevOps extension, authenticate, and configure defaults for:
- Organization: https://dev.azure.com/ConstellationADO
- Project: CVDM

**Manual Verification**:

```powershell
az --version
az extension list
az devops configure --list
```

See [@.agents/skills/ado/SKILL.md](@.agents/skills/ado/SKILL.md) and [.agents/REPO_RULES.md](.agents/REPO_RULES.md) for more details.

## Common Work Item Commands

### Query Work Items

List work items assigned to you:

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' AND [System.State] <> 'Removed' ORDER BY [System.ChangedDate] DESC"
```

List active work items:

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.State] = 'Active' AND [System.AssignedTo] = @Me"
```

List items by iteration:

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.IterationPath] = 'ProjectName\\Sprint 1'"
```

### Show Work Item Details

Get detailed information about a specific work item:

```powershell
az boards work-item show --id <work-item-id>
```

Get specific fields:

```powershell
az boards work-item show --id <work-item-id> --query "{Id: id, Title: fields.'System.Title', State: fields.'System.State', AssignedTo: fields.'System.AssignedTo'.displayName}"
```

### Create Work Items

Create a new task:

```powershell
az boards work-item create --title "Task title" --type "Task" --assigned-to "@Me" --description "Detailed description"
```

Create a bug:

```powershell
az boards work-item create --title "Bug title" --type "Bug" --assigned-to "@Me" --description "Steps to reproduce" --fields "Microsoft.VSTS.TCM.ReproSteps=Step 1<br>Step 2"
```

Create a user story:

```powershell
az boards work-item create --title "User story title" --type "User Story" --description "As a user, I want..."
```

Create a child work item:

```powershell
az boards work-item create --title "Subtask" --type "Task" --assigned-to "@Me" --parent <parent-work-item-id>
```

### Update Work Items

Update work item state:

```powershell
az boards work-item update --id <work-item-id> --state "Active"
az boards work-item update --id <work-item-id> --state "In Progress"
az boards work-item update --id <work-item-id> --state "Resolved"
az boards work-item update --id <work-item-id> --state "Closed"
```

Update title and description:

```powershell
az boards work-item update --id <work-item-id> --title "New title" --description "Updated description"
```

Assign to someone:

```powershell
az boards work-item update --id <work-item-id> --assigned-to "user@company.com"
```

Add tags:

```powershell
az boards work-item update --id <work-item-id> --fields "System.Tags=tag1; tag2; tag3"
```

### Work Item Relations

Link work items:

```powershell
az boards work-item relation add --id <work-item-id> --relation-type "Parent" --target-id <parent-id>
az boards work-item relation add --id <work-item-id> --relation-type "Related" --target-id <related-id>
```

Show relations:

```powershell
az boards work-item relation show --id <work-item-id>
```

## Work Item Types

Common work item types in Azure Boards:

- **Epic**: Large body of work that can be broken down into features
- **Feature**: Service or functionality delivered to end users
- **User Story**: Requirement from the user's perspective
- **Task**: Work to be done
- **Bug**: Code defect or issue
- **Issue**: Risk or impediment

## WIQL (Work Item Query Language)

WIQL is used to query work items. Common fields:

- `[System.Id]` - Work item ID
- `[System.Title]` - Title
- `[System.State]` - State (New, Active, Resolved, Closed, etc.)
- `[System.AssignedTo]` - Person assigned
- `[System.CreatedDate]` - Creation date
- `[System.ChangedDate]` - Last modified date
- `[System.WorkItemType]` - Type (Bug, Task, User Story, etc.)
- `[System.IterationPath]` - Sprint/iteration
- `[System.AreaPath]` - Area classification
- `[System.Tags]` - Tags

Example complex query:

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'Active' AND [System.AssignedTo] = @Me AND [System.CreatedDate] >= @Today - 7"
```

## Extracting Work Item Number from Branch Name

Common pattern in PowerShell:

```powershell
$branchName = git rev-parse --abbrev-ref HEAD
if ($branchName -match '(\d+)') {
    $workItemId = $matches[1]
    az boards work-item show --id $workItemId
}
```

## Output Formats

Control output format:

```powershell
# JSON (default)
az boards work-item show --id 123

# Table format
az boards work-item show --id 123 --output table

# YAML format
az boards work-item show --id 123 --output yaml

# TSV (tab-separated)
az boards work-item show --id 123 --output tsv
```

## Usage with JQ (for JSON parsing)

If you have `jq` installed for JSON parsing:

```powershell
az boards work-item show --id 123 | jq '.fields."System.Title"'
```

Or use PowerShell's built-in JSON handling:

```powershell
$workItem = az boards work-item show --id 123 | ConvertFrom-Json
$workItem.fields.'System.Title'
$workItem.fields.'System.State'
```

## Help

For detailed help on any command:

```powershell
az boards --help
az boards work-item --help
az boards work-item create --help
az boards query --help
```

````