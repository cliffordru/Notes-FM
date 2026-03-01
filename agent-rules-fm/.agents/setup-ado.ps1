#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Setup script for Azure DevOps configuration

.DESCRIPTION
    This script configures the Azure CLI with default settings for the Checkmarx repository.
    It sets the default organization and project for Azure DevOps commands.

.EXAMPLE
    .\.agents\setup-ado.ps1
#>

$ErrorActionPreference = "Stop"

Write-Host "🔧 Azure DevOps Setup Script" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Cyan

TODO: add org
# Configuration
$Organization = "https://dev.azure.com/<organization-name>"
$Project = "CVDM"

# Check if Azure CLI is installed
Write-Host "Checking for Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
    } else {
        throw "Azure CLI not found"
    }
} catch {
    Write-Host "❌ Azure CLI is not installed" -ForegroundColor Red
    Write-Host "`nTo install Azure CLI, run:" -ForegroundColor Yellow
    Write-Host "  winget install -e --id Microsoft.AzureCLI`n" -ForegroundColor White
    exit 1
}

# Check if DevOps extension is installed
Write-Host "Checking for Azure DevOps extension..." -ForegroundColor Yellow
$extensions = az extension list 2>$null | ConvertFrom-Json
$devopsExt = $extensions | Where-Object { $_.name -eq "azure-devops" }

if (-not $devopsExt) {
    Write-Host "⚠️  Azure DevOps extension not found. Installing..." -ForegroundColor Yellow
    az extension add --name azure-devops
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Azure DevOps extension installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install Azure DevOps extension" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Azure DevOps extension is installed (v$($devopsExt.version))" -ForegroundColor Green
}

# Check authentication
Write-Host "`nChecking Azure authentication..." -ForegroundColor Yellow
try {
    $account = az account show 2>$null | ConvertFrom-Json
    if ($account) {
        Write-Host "✅ Authenticated as: $($account.user.name)" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Not authenticated to Azure" -ForegroundColor Yellow
    Write-Host "Running 'az login'..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Authentication failed" -ForegroundColor Red
        exit 1
    }
}

# Configure defaults
Write-Host "`nConfiguring Azure DevOps defaults..." -ForegroundColor Yellow
Write-Host "  Organization: $Organization" -ForegroundColor White
Write-Host "  Project: $Project" -ForegroundColor White

az devops configure --defaults organization=$Organization project=$Project
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Defaults configured successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to configure defaults" -ForegroundColor Red
    exit 1
}

# Verify configuration
Write-Host "`nVerifying configuration..." -ForegroundColor Yellow
az devops configure --list

# Test connection
Write-Host "`nTesting connection to Azure DevOps..." -ForegroundColor Yellow
try {
    $projects = az devops project list --organization $Organization 2>$null | ConvertFrom-Json
    if ($projects.value) {
        Write-Host "✅ Successfully connected to Azure DevOps" -ForegroundColor Green
        Write-Host "   Found $($projects.value.Count) project(s)" -ForegroundColor White
    }
} catch {
    Write-Host "⚠️  Could test connection, but defaults are configured" -ForegroundColor Yellow
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nYou can now use Azure DevOps commands without specifying --organization or --project" -ForegroundColor Cyan
Write-Host "`nExample commands:" -ForegroundColor Cyan
Write-Host "  az repos pr list --status active" -ForegroundColor White
Write-Host "  az boards work-item show --id 12345" -ForegroundColor White
Write-Host "  az boards query --wiql `"SELECT * FROM WorkItems WHERE [System.AssignedTo] = @Me`"`n" -ForegroundColor White
