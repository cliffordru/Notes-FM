````skill
---
name: ado
version: 1.0.0
description: Use when working with Azure DevOps using the Azure CLI (az devops), to get information about Azure DevOps, create and manage repositories, work items, and pull requests.
origin: 
read-only: true
---

# Azure DevOps Skill using az devops (Command Line Interface)

## Prerequisites

- Azure CLI (`az`) with the DevOps extension installed and authenticated (see below)

## Overview

Utilize Azure DevOps Command Line Interface (CLI) to effortlessly engage with Azure DevOps through a streamlined command-line interface. The Azure DevOps CLI provides a powerful toolset that allows users to automate tasks, integrate processes, and interact with Azure DevOps products such as Repos, Boards, Pipelines, and Artifacts, all from the comfort of your terminal.

### Options

```powershell
az devops --help
```

## Getting Started

Check to see if `az` is installed:

```powershell
az --version
```

If not installed, install it:

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
Remove-Item .\AzureCLI.msi
```

**Alternatively, using winget:**
```powershell
winget install -e --id Microsoft.AzureCLI
```

Verify the installation:

```powershell
az --version
```

## Installing the DevOps Extension

After installing the Azure CLI, install the DevOps extension:

```powershell
az extension add --name azure-devops
```

Verify the extension:

```powershell
az extension list
```

## Authenticating to Azure DevOps

To connect to your Azure DevOps organization, you need to authenticate.

Check if you are already authenticated:

```powershell
az account show
```

If you are not authenticated, login:

```powershell
az login
```

### Configure Default Organization and Project (Recommended)

**Quick Setup**: Run the automated setup script:

```powershell
.agents\setup-ado.ps1
```

**Manual Setup**: Set your default organization and project:

TODO: add org and project
```powershell
az devops configure --defaults organization=<organization-name> project=<project-name>
```

View current defaults:

```powershell
az devops configure --list
```

See [.agents/REPO_RULES.md](.agents/REPO_RULES.md) for detailed configuration options.

## Common Commands

### Pull Requests

List pull requests:

```powershell
# List all active PRs in the current project
az repos pr list --status active

# List PRs created by current user
az repos pr list --creator (az ad signed-in-user show --query userPrincipalName -o tsv) --status active

# List PRs assigned to current user as reviewer
az repos pr list --reviewer (az ad signed-in-user show --query id -o tsv) --status active
```

Show PR details:

```powershell
az repos pr show --id <PR_ID>
```

Create a pull request:

```powershell
az repos pr create --title "PR Title" --description "PR Description" --source-branch <branch> --target-branch main
```

### Repositories

List repositories:

```powershell
az repos list
```

Show repository details:

```powershell
az repos show --repository <repo-name>
```

### Work Items (Boards)

List work items assigned to you:

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC"
```

Show work item details:

```powershell
az boards work-item show --id <work-item-id>
```

Create a work item:

```powershell
az boards work-item create --title "Work Item Title" --type "Task" --assigned-to "@Me"
```

Update a work item:

```powershell
az boards work-item update --id <work-item-id> --state "In Progress"
```

### Pipelines

List pipelines:

```powershell
az pipelines list
```

Run a pipeline:

```powershell
az pipelines run --name <pipeline-name>
```

Show pipeline runs:

```powershell
az pipelines runs list --pipeline-name <pipeline-name>
```

## Usage

```powershell
az devops --help
```

### Getting Help

For detailed help on any command:

```powershell
az repos --help
az repos pr --help
az boards --help
az pipelines --help
```

## Environment Variables

You can also use environment variables to set defaults:

```powershell
$env:AZURE_DEVOPS_EXT_PAT = "your-personal-access-token"
```

This is useful for automation scenarios where interactive login is not possible.

````