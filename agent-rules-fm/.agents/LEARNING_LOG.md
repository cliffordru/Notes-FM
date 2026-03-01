# Repo Agent Learning Log

AI agents: update these sections as you discover patterns in this codebase.

- Keep entries concise. If this exceeds 50 entries, suggest the user review and trim.
- When upstreaming, suggest repo-specific patterns for .agents/REPO_RULES.md or universal patterns for AGENTS.md via PR.
- Delete conflicting patterns - keep only the most recent/accurate entry.

## Discovered Patterns

- **Azure DevOps Organization**: https://dev.azure.com/ConstellationADO
- **Azure DevOps Project**: CVDM
- **Primary User Email**: E906351@constellation.com (use for work item assignments)
- **Repository Type**: Azure DevOps Git (not GitHub)
- **Shell Environment**: PowerShell (Windows)
- **Default Branch**: main
- **Work Item URL Pattern**: https://dev.azure.com/ConstellationADO/CVDM/_workitems/edit/{id}
- **GitHub Copilot Instructions**: `.github/copilot-instructions.md` provides automatic context to Copilot
- **Custom Commands**: Use `@command-name` to invoke .agents workflows (e.g., @standup, @review, @commit)
- **.agents Structure**: REPO_RULES.md (repo-specific, version-controlled), USER_RULES.md (personal, gitignored), TEAM_RULES.md (team, gitignored)

## Lessons Learned

- `@Me` syntax does NOT work in Azure CLI commands - use explicit email address instead
- User's git email (Cliff.Gray@Constellation.com) differs from ADO email (E906351@constellation.com)
- Work item assignment requires the ADO email: E906351@constellation.com
- Azure CLI configuration is global/persistent - no need to reconfigure on project reopen
- GitHub CLI (gh) commands won't work - this is an Azure DevOps repository
- `.github/copilot-instructions.md` should reference directories (not list specific items) for maintainability
- **Keep it DRY**: `.github/copilot-instructions.md` only references AGENTS.md - all repo/user info lives in REPO_RULES.md and USER_RULES.md
- Do not use em dash
- Do not specify copilot or agent when creating ado items

## Codebase Quirks

- Scripts are mix of PowerShell (.ps1) and bash (.sh) - prefer PowerShell for new scripts
- Multiple script subdirectories under /scripts/ for different automation tasks
- Checkmarx-related automation (security scanning platform)
- Identity provider and group management scripts indicate enterprise/multi-tenant setup
