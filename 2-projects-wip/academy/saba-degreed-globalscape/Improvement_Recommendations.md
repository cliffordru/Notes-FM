# GlobalScape Integration: Improvement Recommendations & Implementation Guide

**Document Created**: March 3, 2026  
**Based On**: prompt.md outstanding issues + Saba.json technical analysis  
**Priority**: HIGH - System has been in degraded state with recurring issues for 1.5+ years

---

## Executive Summary

This document provides actionable recommendations to address the critical issues identified in the Saba → Degreed integration via GlobalScape MFT. It includes technical specifications, code examples, resource requirements, and implementation timelines.

### Key Recommendations

1. 🔴 **CRITICAL**: Restore missing `Saba_Zip` custom command
2. 🔴 **CRITICAL**: Fix retry job logic with proper file cleanup
3. 🟡 **HIGH**: Implement proper error handling and alerting
4. 🟡 **HIGH**: Add pre-execution folder validation
5. 🟢 **MEDIUM**: Modernize to API-based integration (phase 2)

---

## Table of Contents

1. [Immediate Fixes (Week 1-2)](#immediate-fixes)
2. [Short-Term Improvements (Month 1-2)](#short-term-improvements)
3. [Long-Term Modernization (Quarter 2-3)](#long-term-modernization)
4. [Required Skills & Resources](#required-skills--resources)
5. [Implementation Roadmap](#implementation-roadmap)
6. [Code Examples](#code-examples)
7. [Testing Strategy](#testing-strategy)
8. [Risk Mitigation](#risk-mitigation)

---

## Immediate Fixes (Week 1-2)

### 🔴 Priority 1: Restore Missing Saba_Zip Command

**Problem**: All 9 event rules fail because custom command `Saba_Zip` does not exist

**Impact**: Complete integration failure, no data flowing between systems

**Solution**: Recreate the custom command with proper error handling

#### Implementation Steps

**1. Locate Original Script** (if it exists)
```powershell
# Search for backup or archive
Get-ChildItem -Path "C:\GlobalScape\CustomCommands" -Recurse -Filter "*Saba*" -ErrorAction SilentlyContinue
Get-ChildItem -Path "\\FileServer\Backups\GlobalScape" -Recurse -Filter "*zip*" -ErrorAction SilentlyContinue
```

**2. If Original Not Found, Recreate**

**Option A: Basic Zip Command**
```powershell
<#
.SYNOPSIS
    Saba_Zip - Compress files for Saba integration transfer
.DESCRIPTION
    Compresses individual file or directory contents into a zip archive
    for efficient transfer to Degreed/other systems
.PARAMETER SourcePath
    Path to file or directory to compress
.PARAMETER DestinationPath
    Output path for zip file (must end in .zip)
.PARAMETER DeleteSource
    If $true, deletes source files after successful compression
.EXAMPLE
    Saba_Zip.ps1 -SourcePath "C:\Staging\Degreed\data.csv" -DestinationPath "C:\Output\data.zip"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,
    
    [Parameter(Mandatory=$true)]
    [ValidatePattern('\.zip$')]
    [string]$DestinationPath,
    
    [Parameter(Mandatory=$false)]
    [switch]$DeleteSource = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$LogPath = "C:\GlobalScape\Logs\Saba_Zip.log"
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp [$Level] $Message"
    Add-Content -Path $LogPath -Value $logMessage
    Write-Output $logMessage
}

try {
    Write-Log "Starting compression: $SourcePath -> $DestinationPath"
    
    # Validate source exists
    if (-not (Test-Path -Path $SourcePath)) {
        throw "Source path does not exist: $SourcePath"
    }
    
    # Create destination directory if needed
    $destDir = Split-Path -Path $DestinationPath -Parent
    if (-not (Test-Path -Path $destDir)) {
        Write-Log "Creating destination directory: $destDir"
        New-Item -Path $destDir -ItemType Directory -Force | Out-Null
    }
    
    # Remove existing destination file if it exists
    if (Test-Path -Path $DestinationPath) {
        Write-Log "Removing existing destination file: $DestinationPath" -Level "WARN"
        Remove-Item -Path $DestinationPath -Force
    }
    
    # Compress the file(s)
    Write-Log "Compressing files..."
    Compress-Archive -Path $SourcePath -DestinationPath $DestinationPath -CompressionLevel Optimal -Force
    
    # Verify the zip was created
    if (-not (Test-Path -Path $DestinationPath)) {
        throw "Compression failed - destination file not created"
    }
    
    $zipSize = (Get-Item $DestinationPath).Length
    Write-Log "Compression successful. Zip size: $($zipSize / 1KB) KB"
    
    # Delete source if requested
    if ($DeleteSource) {
        Write-Log "Deleting source files/directory: $SourcePath"
        Remove-Item -Path $SourcePath -Recurse -Force
    }
    
    Write-Log "Saba_Zip completed successfully" -Level "SUCCESS"
    exit 0
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)" -Level "ERROR"
    Write-Log "Stack Trace: $($_.ScriptStackTrace)" -Level "ERROR"
    exit 1
}
```

**3. Register in GlobalScape**

Navigate to GlobalScape Admin Console:
1. Go to `Resources` → `Custom Commands`
2. Click `Add Custom Command`
3. Configure:
   - **Name**: `Saba_Zip`
   - **ID**: `0b04bb0e-3f0d-55c6-a166-49bc658fb477` (use existing GUID from JSON)
   - **Type**: PowerShell Script
   - **Script Path**: `C:\GlobalScape\CustomCommands\Saba_Zip.ps1`
   - **Execution Account**: Service account with file system access
   - **Parameters**: Map to script parameters

**4. Test Command**
```powershell
# Create test data
"test,data,file" | Out-File "C:\Temp\test.csv"

# Execute custom command through GlobalScape test console
# Or test directly:
.\Saba_Zip.ps1 -SourcePath "C:\Temp\test.csv" -DestinationPath "C:\Temp\test.zip" -Verbose
```

**5. Re-enable Event Rules**

Once custom command is registered, event rules should validate successfully.

---

### 🔴 Priority 2: Fix Retry Job Logic

**Problem**: Retry jobs run regardless of primary job status, no folder cleanup

**Impact**: Multiple files in target folder, Degreed picks up wrong file

**Solution**: Implement intelligent retry with pre-checks

#### Approach A: Conditional Retry Execution

**Add condition to each retry job:**

```powershell
<#
.SYNOPSIS
    Pre-Retry Validator - Check if retry is needed
.DESCRIPTION
    Validates conditions before retry job executes:
    1. Primary job failed (check log or status file)
    2. Target folder has leftover files
    3. Cleanup those files before retry
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$PrimaryJobName,
    
    [Parameter(Mandatory=$true)]
    [string]$TargetFolderPath,
    
    [Parameter(Mandatory=$false)]
    [string]$StatusFilePath = "C:\GlobalScape\Status"
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "$timestamp - $Message"
}

try {
    Write-Log "=== Pre-Retry Validation for $PrimaryJobName ==="
    
    # Check 1: Did primary job fail?
    $statusFile = Join-Path $StatusFilePath "$PrimaryJobName.status"
    
    if (Test-Path $statusFile) {
        $status = Get-Content $statusFile -Raw | ConvertFrom-Json
        
        if ($status.LastRunStatus -eq "Success") {
            Write-Log "Primary job succeeded, retry not needed"
            exit 0  # Exit successfully but don't continue to retry
        }
        
        Write-Log "Primary job failed: $($status.LastRunError)"
    } else {
        Write-Log "Warning: No status file found, assuming retry needed"
    }
    
    # Check 2: Are there files in target folder?
    if (Test-Path $TargetFolderPath) {
        $existingFiles = Get-ChildItem -Path $TargetFolderPath -File
        
        if ($existingFiles.Count -gt 0) {
            Write-Log "Found $($existingFiles.Count) file(s) in target folder"
            
            foreach ($file in $existingFiles) {
                Write-Log "Removing: $($file.Name) (Size: $($file.Length) bytes, Modified: $($file.LastWriteTime))"
                
                # Archive before delete (safety measure)
                $archivePath = "C:\GlobalScape\Archive\PreRetryCleanup"
                if (-not (Test-Path $archivePath)) {
                    New-Item -Path $archivePath -ItemType Directory -Force | Out-Null
                }
                
                $archiveFile = Join-Path $archivePath "$($file.Name)_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
                Move-Item -Path $file.FullName -Destination $archiveFile -Force
                Write-Log "Archived to: $archiveFile"
            }
            
            Write-Log "Target folder cleaned successfully"
        } else {
            Write-Log "Target folder is empty, proceeding with retry"
        }
    } else {
        Write-Log "Target folder does not exist, creating: $TargetFolderPath"
        New-Item -Path $TargetFolderPath -ItemType Directory -Force | Out-Null
    }
    
    # Check 3: Verify Degreed endpoint is reachable
    Write-Log "Validating Degreed endpoint connectivity..."
    
    # This would be the actual Degreed SFTP host or API endpoint
    $degreedEndpoint = "sftp.degreed.com"  # Replace with actual
    
    try {
        $testConnection = Test-NetConnection -ComputerName $degreedEndpoint -Port 22 -WarningAction SilentlyContinue
        
        if ($testConnection.TcpTestSucceeded) {
            Write-Log "Degreed endpoint is reachable"
        } else {
            Write-Log "WARNING: Cannot reach Degreed endpoint - retry may fail"
        }
    } catch {
        Write-Log "WARNING: Connection test failed: $($_.Exception.Message)"
    }
    
    Write-Log "=== Pre-Retry Validation Complete - Proceeding with Retry ==="
    exit 0
    
} catch {
    Write-Log "ERROR in pre-retry validation: $($_.Exception.Message)"
    exit 1
}
```

**Integration into GlobalScape Event Rule:**

For each retry job (167_ReRun, 170_ReRun, 171_ReRun):

1. Add statement at beginning of StatementsList
2. Statement Type: Custom Command
3. Command: `Pre-Retry-Validator`
4. Parameters:
   - PrimaryJobName: `167_Saba_Degreed_RL_Upload_Timer`
   - TargetFolderPath: `\\FileServer\GlobalScape\Degreed\Staging\RequiredLearning`
5. If Failed Actions: Exit event rule

#### Approach B: Status File Pattern

Create status files that primary jobs write on completion:

```powershell
# End of primary job - write status
$statusFile = "C:\GlobalScape\Status\$($env:GLOBALSCAPE_EVENTRULE_NAME).status"

$status = @{
    JobName = $env:GLOBALSCAPE_EVENTRULE_NAME
    LastRunTime = (Get-Date).ToString("o")
    LastRunStatus = if ($?) { "Success" } else { "Failed" }
    LastRunError = if (-not $?) { $Error[0].Exception.Message } else { $null }
    RecordCount = $recordsProcessed  # Your variable
    FileSize = $fileSize  # Your variable
} | ConvertTo-Json

$status | Out-File -FilePath $statusFile -Force
```

Retry jobs read this file to decide whether to execute.

---

### 🔴 Priority 3: Implement Comprehensive Logging

**Problem**: Limited visibility into job execution, failures, and data volumes

**Solution**: Structured logging with centralized collection

#### Enhanced Logging Module

```powershell
<#
.SYNOPSIS
    GlobalScape Integration Logging Module
#>

class IntegrationLogger {
    [string]$LogPath
    [string]$JobName
    [string]$SessionId
    
    IntegrationLogger([string]$jobName) {
        $this.JobName = $jobName
        $this.SessionId = [guid]::NewGuid().ToString().Substring(0,8)
        
        $logDir = "C:\GlobalScape\Logs\$jobName"
        if (-not (Test-Path $logDir)) {
            New-Item -Path $logDir -ItemType Directory -Force | Out-Null
        }
        
        $logFile = "$(Get-Date -Format 'yyyyMMdd')_$($this.SessionId).log"
        $this.LogPath = Join-Path $logDir $logFile
    }
    
    [void]Info([string]$message) {
        $this.WriteLog("INFO", $message)
    }
    
    [void]Warning([string]$message) {
        $this.WriteLog("WARN", $message)
    }
    
    [void]Error([string]$message) {
        $this.WriteLog("ERROR", $message)
    }
    
    [void]Success([string]$message) {
        $this.WriteLog("SUCCESS", $message)
    }
    
    [void]Metric([hashtable]$metrics) {
        $metricsJson = $metrics | ConvertTo-Json -Compress
        $this.WriteLog("METRIC", $metricsJson)
    }
    
    [void]WriteLog([string]$level, [string]$message) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        $logEntry = "$timestamp [$level] [$($this.JobName)] [$($this.SessionId)] $message"
        
        # Write to file
        Add-Content -Path $this.LogPath -Value $logEntry
        
        # Also write to console for GlobalScape capture
        Write-Output $logEntry
        
        # If error, also write to Windows Event Log
        if ($level -eq "ERROR") {
            try {
                Write-EventLog -LogName Application -Source "GlobalScape_Integration" `
                    -EntryType Error -EventId 1001 -Message $message -ErrorAction SilentlyContinue
            } catch {
                # Event source may not be registered, ignore
            }
        }
    }
}

# Usage example:
# $logger = [IntegrationLogger]::new("167_Saba_Degreed_RL_Upload")
# $logger.Info("Starting job execution")
# $logger.Metric(@{RecordsProcessed=150; ExecutionTimeMs=2500; FileSize=1024000})
```

#### Log Aggregation Script

```powershell
<#
.SYNOPSIS
    Aggregate and analyze job execution logs
#>

function Get-JobExecutionSummary {
    param(
        [Parameter(Mandatory=$true)]
        [string]$JobName,
        
        [Parameter(Mandatory=$false)]
        [int]$LastNDays = 7
    )
    
    $logDir = "C:\GlobalScape\Logs\$JobName"
    $cutoffDate = (Get-Date).AddDays(-$LastNDays)
    
    $logFiles = Get-ChildItem -Path $logDir -Filter "*.log" | 
        Where-Object { $_.CreationTime -ge $cutoffDate }
    
    $summary = @{
        JobName = $JobName
        Period = "$LastNDays days"
        TotalRuns = 0
        SuccessfulRuns = 0
        FailedRuns = 0
        AverageExecutionTime = 0
        TotalRecordsProcessed = 0
        LastRunStatus = "Unknown"
        Errors = @()
    }
    
    foreach ($logFile in $logFiles) {
        $content = Get-Content $logFile -Raw
        
        if ($content -match "SUCCESS") {
            $summary.SuccessfulRuns++
        } elseif ($content -match "ERROR") {
            $summary.FailedRuns++
            
            # Extract error messages
            $errors = $content | Select-String -Pattern "\[ERROR\] (.+)" -AllMatches
            foreach ($error in $errors.Matches) {
                $summary.Errors += $error.Groups[1].Value
            }
        }
        
        $summary.TotalRuns++
    }
    
    return $summary | ConvertTo-Json -Depth 5
}

# Generate daily summary report
Get-JobExecutionSummary -JobName "167_Saba_Degreed_RL_Upload" -LastNDays 1
```

---

## Short-Term Improvements (Month 1-2)

### 🟡 Priority 4: Add Email Alerting

**Solution**: PowerShell email alerts on failures

```powershell
<#
.SYNOPSIS
    Send email alert for job failures
#>

function Send-JobFailureAlert {
    param(
        [Parameter(Mandatory=$true)]
        [string]$JobName,
        
        [Parameter(Mandatory=$true)]
        [string]$ErrorMessage,
        
        [Parameter(Mandatory=$false)]
        [hashtable]$AdditionalInfo = @{}
    )
    
    $smtpServer = "smtp.fmglobal.com"  # Replace with actual
    $fromAddress = "globalscape-alerts@fmglobal.com"
    $toAddresses = @(
        "melissa.giamberardino@fmglobal.com",
        "vinod.reddy@fmglobal.com",
        "john.tang@fmglobal.com"
    )
    
    $subject = "❌ GlobalScape Job Failed: $JobName"
    
    $bodyHtml = @"
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .error { color: red; font-weight: bold; }
        .info-table { border-collapse: collapse; margin-top: 15px; }
        .info-table td { padding: 8px; border: 1px solid #ddd; }
        .info-table td:first-child { background-color: #f0f0f0; font-weight: bold; }
    </style>
</head>
<body>
    <h2 style="color: red;">GlobalScape Integration Job Failed</h2>
    
    <table class="info-table">
        <tr><td>Job Name</td><td>$JobName</td></tr>
        <tr><td>Timestamp</td><td>$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</td></tr>
        <tr><td>Server</td><td>$env:COMPUTERNAME</td></tr>
        <tr><td>Error</td><td class="error">$ErrorMessage</td></tr>
    </table>
    
    <h3>Additional Information</h3>
    <table class="info-table">
"@
    
    foreach ($key in $AdditionalInfo.Keys) {
        $bodyHtml += "<tr><td>$key</td><td>$($AdditionalInfo[$key])</td></tr>"
    }
    
    $bodyHtml += @"
    </table>
    
    <p><strong>Action Required:</strong> Please investigate and resolve the issue.</p>
    
    <p style="font-size: 0.9em; color: #666;">
        This is an automated alert from GlobalScape MFT Platform.<br>
        Log files: \\FileServer\GlobalScape\Logs\$JobName\
    </p>
</body>
</html>
"@
    
    try {
        Send-MailMessage -SmtpServer $smtpServer `
            -From $fromAddress `
            -To $toAddresses `
            -Subject $subject `
            -Body $bodyHtml `
            -BodyAsHtml `
            -Priority High
        
        Write-Output "Alert email sent successfully"
    } catch {
        Write-Error "Failed to send alert email: $($_.Exception.Message)"
        # Log to file as backup
        $alertLog = "C:\GlobalScape\Logs\EmailAlerts\failed_$(Get-Date -Format 'yyyyMMddHHmmss').json"
        @{
            JobName = $JobName
            ErrorMessage = $ErrorMessage
            EmailError = $_.Exception.Message
        } | ConvertTo-Json | Out-File $alertLog
    }
}

# Usage in event rule:
# Send-JobFailureAlert -JobName $env:GLOBALSCAPE_EVENTRULE_NAME -ErrorMessage $Error[0].Exception.Message
```

---

### 🟡 Priority 5: Data Validation Layer

**Problem**: Unknown data quality, format issues may cause downstream failures

**Solution**: Validate data before transfer

```powershell
<#
.SYNOPSIS
    Validate data file before sending to Degreed
#>

function Test-DegreedDataFile {
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath,
        
        [Parameter(Mandatory=$true)]
        [ValidateSet('RequiredLearning', 'Content', 'Completions')]
        [string]$DataType
    )
    
    $logger = [IntegrationLogger]::new("DataValidation_$DataType")
    $logger.Info("Starting validation for: $FilePath")
    
    $validationResults = @{
        IsValid = $true
        Errors = @()
        Warnings = @()
        RowCount = 0
        ValidationTime = [datetime]::Now
    }
    
    try {
        # Check file exists and not empty
        if (-not (Test-Path $FilePath)) {
            $validationResults.IsValid = $false
            $validationResults.Errors += "File does not exist"
            return $validationResults
        }
        
        $fileInfo = Get-Item $FilePath
        if ($fileInfo.Length -eq 0) {
            $validationResults.IsValid = $false
            $validationResults.Errors += "File is empty (0 bytes)"
            return $validationResults
        }
        
        # Parse CSV and validate structure
        $data = Import-Csv -Path $FilePath
        $validationResults.RowCount = $data.Count
        
        if ($data.Count -eq 0) {
            $validationResults.IsValid = $false
            $validationResults.Errors += "No data rows found (header only)"
            return $validationResults
        }
        
        # Data type specific validation
        switch ($DataType) {
            'RequiredLearning' {
                $requiredColumns = @('EmployeeId', 'CourseId', 'AssignedDate', 'DueDate')
                
                foreach ($col in $requiredColumns) {
                    if ($col -notin $data[0].PSObject.Properties.Name) {
                        $validationResults.IsValid = $false
                        $validationResults.Errors += "Missing required column: $col"
                    }
                }
                
                # Validate data quality
                $invalidRows = $data | Where-Object { 
                    [string]::IsNullOrWhiteSpace($_.EmployeeId) -or 
                    [string]::IsNullOrWhiteSpace($_.CourseId) 
                }
                
                if ($invalidRows) {
                    $validationResults.Warnings += "Found $($invalidRows.Count) rows with missing EmployeeId or CourseId"
                }
            }
            
            'Content' {
                $requiredColumns = @('ContentId', 'Title', 'Provider', 'URL')
                
                foreach ($col in $requiredColumns) {
                    if ($col -notin $data[0].PSObject.Properties.Name) {
                        $validationResults.IsValid = $false
                        $validationResults.Errors += "Missing required column: $col"
                    }
                }
            }
            
            'Completions' {
                $requiredColumns = @('EmployeeId', 'CourseId', 'CompletionDate', 'Score')
                
                foreach ($col in $requiredColumns) {
                    if ($col -notin $data[0].PSObject.Properties.Name) {
                        $validationResults.IsValid = $false
                        $validationResults.Errors += "Missing required column: $col"
                    }
                }
                
                # Validate dates
                $invalidDates = $data | Where-Object { 
                    try {
                        [datetime]::Parse($_.CompletionDate) | Out-Null
                        $false
                    } catch {
                        $true
                    }
                }
                
                if ($invalidDates) {
                    $validationResults.IsValid = $false
                    $validationResults.Errors += "Found $($invalidDates.Count) rows with invalid CompletionDate"
                }
            }
        }
        
        # Check for duplicate records
        $duplicates = $data | Group-Object -Property { 
            if ($_.EmployeeId) { "$($_.EmployeeId)_$($_.CourseId)" } 
            else { $_.ContentId }
        } | Where-Object { $_.Count -gt 1 }
        
        if ($duplicates) {
            $validationResults.Warnings += "Found $($duplicates.Count) duplicate records"
        }
        
        # Log results
        if ($validationResults.IsValid) {
            $logger.Success("Validation passed: $($validationResults.RowCount) rows")
        } else {
            $logger.Error("Validation failed: $($validationResults.Errors -join '; ')")
        }
        
        if ($validationResults.Warnings) {
            $logger.Warning("Validation warnings: $($validationResults.Warnings -join '; ')")
        }
        
    } catch {
        $validationResults.IsValid = $false
        $validationResults.Errors += "Exception during validation: $($_.Exception.Message)"
        $logger.Error($_.Exception.Message)
    }
    
    return $validationResults
}

# Usage in event rule:
# $validation = Test-DegreedDataFile -FilePath $stagingFile -DataType "RequiredLearning"
# if (-not $validation.IsValid) { 
#     Send-JobFailureAlert -JobName "Data Validation" -ErrorMessage ($validation.Errors -join "; ")
#     exit 1 
# }
```

---

## Long-Term Modernization (Quarter 2-3)

### 🟢 Priority 6: Move to API-Based Integration

**Current**: File-based SFTP transfers  
**Target**: Direct API-to-API synchronization

**Benefits**:
- Real-time or near-real-time sync
- No file staging required
- Better error handling at record level
- Reduced latency
- Easier monitoring and debugging

#### Proposed Architecture

```
┌─────────────┐
│  Saba API   │
└──────┬──────┘
       │ REST API calls
       ▼
┌──────────────────────────────┐
│   Integration Service        │
│   (PowerShell or C# service) │
│                              │
│   • API orchestration        │
│   • Data transformation      │
│   • Error handling           │
│   • Retry logic              │
│   • Monitoring/logging       │
└──────┬───────────────────────┘
       │ REST API calls
       ▼
┌─────────────┐
│ Degreed API │
└─────────────┘
```

#### Implementation Plan

**Phase 1: API Discovery**
- Document all Saba API endpoints currently used
- Document all Degreed API endpoints
- Create API authentication setup (OAuth 2.0, API keys)
- Test API calls in Postman/similar

**Phase 2: Build Integration Service**

```powershell
<#
.SYNOPSIS
    Modern API-based integration service for Saba → Degreed
.DESCRIPTION
    Replaces file-based GlobalScape jobs with direct API calls
#>

class SabaDegreedIntegrationService {
    [string]$SabaApiBaseUrl
    [string]$DegreedApiBaseUrl
    [hashtable]$SabaAuthHeaders
    [hashtable]$DegreedAuthHeaders
    
    SabaDegreedIntegrationService() {
        $this.SabaApiBaseUrl = "https://saba.fmglobal.com/api/v2"
        $this.DegreedApiBaseUrl = "https://api.degreed.com/api/v2"
        
        # Authentication setup
        $this.SabaAuthHeaders = $this.GetSabaAuthHeaders()
        $this.DegreedAuthHeaders = $this.GetDegreedAuthHeaders()
    }
    
    [hashtable]GetSabaAuthHeaders() {
        # Implement Saba authentication (OAuth or API key)
        $apiKey = Get-Secret -Name "Saba_API_Key" -AsPlainText
        
        return @{
            "Authorization" = "Bearer $apiKey"
            "Content-Type" = "application/json"
            "Accept" = "application/json"
        }
    }
    
    [hashtable]GetDegreedAuthHeaders() {
        # Implement Degreed authentication
        $clientId = Get-Secret -Name "Degreed_Client_ID" -AsPlainText
        $clientSecret = Get-Secret -Name "Degreed_Client_Secret" -AsPlainText
        
        # Get OAuth token
        $tokenUrl = "https://api.degreed.com/oauth/token"
        $tokenBody = @{
            grant_type = "client_credentials"
            client_id = $clientId
            client_secret = $clientSecret
        }
        
        $tokenResponse = Invoke-RestMethod -Uri $tokenUrl -Method Post -Body $tokenBody
        
        return @{
            "Authorization" = "Bearer $($tokenResponse.access_token)"
            "Content-Type" = "application/json"
            "Accept" = "application/json"
        }
    }
    
    [object[]]GetRequiredLearningFromSaba() {
        $logger = [IntegrationLogger]::new("API_RequiredLearning")
        $logger.Info("Fetching required learning from Saba API")
        
        try {
            $endpoint = "$($this.SabaApiBaseUrl)/learners/assignments"
            $params = @{
                status = "active"
                modifiedSince = (Get-Date).AddDays(-1).ToString("o")
                pageSize = 1000
            }
            
            $queryString = ($params.GetEnumerator() | ForEach-Object { 
                "$($_.Key)=$($_.Value)" 
            }) -join "&"
            
            $url = "$endpoint?$queryString"
            
            $response = Invoke-RestMethod -Uri $url -Method Get -Headers $this.SabaAuthHeaders
            
            $logger.Info("Retrieved $($response.items.Count) required learning records")
            
            return $response.items
            
        } catch {
            $logger.Error("Failed to get required learning: $($_.Exception.Message)")
            throw
        }
    }
    
    [void]SendRequiredLearningToDegreed([object[]]$learningRecords) {
        $logger = [IntegrationLogger]::new("API_RequiredLearning")
        $logger.Info("Sending $($learningRecords.Count) records to Degreed")
        
        $successCount = 0
        $failCount = 0
        
        # Batch records (Degreed may accept batch API calls)
        $batchSize = 100
        $batches = @()
        
        for ($i = 0; $i -lt $learningRecords.Count; $i += $batchSize) {
            $batch = $learningRecords[$i..[Math]::Min($i + $batchSize - 1, $learningRecords.Count - 1)]
            $batches += ,@($batch)
        }
        
        foreach ($batch in $batches) {
            try {
                $endpoint = "$($this.DegreedApiBaseUrl)/required-learning"
                
                # Transform Saba format to Degreed format
                $degreedPayload = $batch | ForEach-Object {
                    @{
                        employeeId = $_.learnerId
                        contentId = $_.learningId
                        assignedDate = $_.assignedDate
                        dueDate = $_.dueDate
                        status = "assigned"
                    }
                }
                
                $body = $degreedPayload | ConvertTo-Json -Depth 10
                
                $response = Invoke-RestMethod -Uri $endpoint -Method Post `
                    -Headers $this.DegreedAuthHeaders -Body $body
                
                $successCount += $batch.Count
                $logger.Info("Batch successful: $($batch.Count) records")
                
            } catch {
                $failCount += $batch.Count
                $logger.Error("Batch failed: $($_.Exception.Message)")
                
                # Could implement retry logic here
                # Or save failed records for manual review
            }
        }
        
        $logger.Metric(@{
            TotalRecords = $learningRecords.Count
            SuccessCount = $successCount
            FailCount = $failCount
            SuccessRate = [Math]::Round(($successCount / $learningRecords.Count) * 100, 2)
        })
    }
    
    [void]SyncRequiredLearning() {
        $records = $this.GetRequiredLearningFromSaba()
        if ($records.Count -gt 0) {
            $this.SendRequiredLearningToDegreed($records)
        }
    }
}

# Usage:
# $service = [SabaDegreedIntegrationService]::new()
# $service.SyncRequiredLearning()
```

**Phase 3: Deploy as Windows Service or Azure Function**

Option 1: Windows Service
```powershell
# Service wrapper
New-Service -Name "SabaDegreedIntegration" `
    -BinaryPathName "C:\Services\SabaDegreedIntegration\service.exe" `
    -DisplayName "Saba-Degreed Integration Service" `
    -Description "API-based integration between Saba LMS and Degreed LXP" `
    -StartupType Automatic
```

Option 2: Azure Function (C# recommended for production)
```csharp
// Azure Function Timer Trigger
[FunctionName("SabaDegreedSync")]
public static async Task Run(
    [TimerTrigger("0 0 2 * * *")] TimerInfo myTimer, // Daily at 2 AM
    ILogger log)
{
    log.LogInformation($"Saba-Degreed sync started at: {DateTime.Now}");
    
    var service = new SabaDegreedIntegrationService();
    await service.SyncRequiredLearningAsync();
    
    log.LogInformation("Sync completed");
}
```

---

## Required Skills & Resources

### Technical Skills Matrix

| Skill | Current Priority | Future Priority | Team Member | Proficiency Needed |
|-------|------------------|-----------------|-------------|-------------------|
| **PowerShell** | 🔴 Critical | 🟡 Medium | Vinod, IT Ops | Advanced |
| **GlobalScape Admin** | 🔴 Critical | 🟢 Low | Vinod | Expert |
| **Saba API** | 🟡 Medium | 🔴 Critical | John, Developer | Intermediate |
| **Degreed API** | 🟡 Medium | 🔴 Critical | John, Developer | Intermediate |
| **C#/.NET** | 🟢 Low | 🟡 Medium | Developer (TBD) | Intermediate |
| **Azure Functions** | 🟢 Low | 🟡 Medium | Developer (TBD) | Basic-Intermediate |
| **REST APIs** | 🟡 Medium | 🔴 Critical | Developer (TBD) | Intermediate |
| **JSON/XML** | 🟡 Medium | 🟡 Medium | All | Basic-Intermediate |
| **Git/Source Control** | 🟡 Medium | 🟡 Medium | All | Basic |
| **Testing/QA** | 🟡 Medium | 🟡 Medium | Melissa, QA | Intermediate |

### Team Resource Requirements

**Immediate (Week 1-4)**:
- 1 GlobalScape Administrator (Vinod) - 20 hours/week
- 1 PowerShell Developer - 30 hours/week
- 1 Business Analyst (Melissa) - 10 hours/week for testing
- 1 Project Manager - 5 hours/week

**Short-Term (Month 2-3)**:
- 1 GlobalScape Administrator - 10 hours/week
- 1 PowerShell Developer - 20 hours/week
- 1 API Integration Developer - 20 hours/week (if moving to API model)
- 1 QA Engineer - 15 hours/week

**Long-Term (Quarter 2-3)**:
- 1 API Integration Developer - 40 hours/week
- 1 DevOps Engineer - 20 hours/week
- 1 QA Engineer - 20 hours/week
- 1 Technical Writer - 10 hours/week

### Training Needs

| Team Member | Training Required | Duration | Priority |
|-------------|-------------------|----------|----------|
| Vinod | PowerShell Advanced Techniques | 2 days | 🔴 High |
| John | Saba API Deep Dive | 1 day | 🟡 Medium |
| John | Degreed API Deep Dive | 1 day | 🟡 Medium |
| New Developer | Azure Functions & Serverless | 3 days | 🟢 Low |
| All | Git & Version Control Best Practices | 0.5 day | 🟡 Medium |

---

## Implementation Roadmap

### Phase 1: Stabilization (Weeks 1-4)

**Week 1:**
- ✅ Recreate and test Saba_Zip custom command
- ✅ Register command in GlobalScape
- ✅ Validate all 9 event rules

**Week 2:**
- ✅ Implement pre-retry folder cleanup logic
- ✅ Deploy to all retry jobs
- ✅ Add comprehensive logging to all jobs
- ✅ Test in Degreed beta environment

**Week 3:**
- ✅ Implement email alerting
- ✅ Create monitoring dashboard (PowerBI or similar)
- ✅ Document all file paths and folders
- ✅ Update connection profiles if needed

**Week 4:**
- ✅ Full end-to-end testing
- ✅ Create runbooks for common issues
- ✅ Knowledge transfer session with team
- ✅ Deploy to production with rollback plan

**Deliverables**:
- ✅ Working GlobalScape integration with all 9 jobs operational
- ✅ Comprehensive logging and alerting
- ✅ Documentation of current state
- ✅ Testing artifacts and results

### Phase 2: Enhancement (Months 2-3)

**Month 2:**
- Data validation layer implementation
- Performance optimization
- Additional error handling scenarios
- Backup and recovery procedures

**Month 3:**
- API endpoint documentation for Saba & Degreed
- Proof-of-concept API-based integration
- Comparison analysis: File-based vs. API-based

**Deliverables**:
- ✅ Enhanced reliability and monitoring
- ✅ API integration feasibility study
- ✅ Recommendation for modernization approach

### Phase 3: Modernization (Quarters 2-3)

**Q2:**
- API-based integration development
- Testing in parallel with existing file-based system
- Performance benchmarking

**Q3:**
- Cutover planning
- Production deployment of API-based system
- Decommission file-based integration
- Final documentation

**Deliverables**:
- ✅ Modern, maintainable API-based integration
- ✅ Reduced operational overhead
- ✅ Improved data freshness and reliability

---

## Code Examples

### Complete Event Rule Enhancement Pattern

```powershell
<#
.SYNOPSIS
    Enhanced Saba-Degreed Integration Job Template
.DESCRIPTION
    Standard pattern for all integration jobs with:
    - Logging
    - Error handling
    - Validation
    - Alerting
    - Metrics
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$JobName,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet('RequiredLearning', 'Content', 'Completions')]
    [string]$DataType
)

# Initialize
$logger = [IntegrationLogger]::new($JobName)
$startTime = Get-Date

try {
    $logger.Info("=== Job Started: $JobName ===")
    $logger.Info("Data Type: $DataType")
    $logger.Info("Execution Time: $startTime")
    
    # Step 1: Pre-execution validation
    $logger.Info("Step 1: Pre-execution validation")
    
    $sourcePath = "\\FileServer\Saba\Export\$DataType"
    $stagingPath = "\\FileServer\GlobalScape\Degreed\Staging\$DataType"
    $archivePath = "\\FileServer\GlobalScape\Degreed\Archive\$DataType"
    
    # Ensure directories exist
    @($sourcePath, $stagingPath, $archivePath) | ForEach-Object {
        if (-not (Test-Path $_)) {
            $logger.Warning("Creating directory: $_")
            New-Item -Path $_ -ItemType Directory -Force | Out-Null
        }
    }
    
    # Step 2: Get data from Saba
    $logger.Info("Step 2: Extracting data from Saba")
    
    $sourceFile = Get-ChildItem -Path $sourcePath -Filter "*.csv" | 
        Sort-Object LastWriteTime -Descending | 
        Select-Object -First 1
    
    if (-not $sourceFile) {
        $logger.Warning("No source file found. Nothing to process.")
        exit 0
    }
    
    $logger.Info("Source file: $($sourceFile.Name), Size: $($sourceFile.Length) bytes")
    
    # Step 3: Validate data
    $logger.Info("Step 3: Data validation")
    
    $validation = Test-DegreedDataFile -FilePath $sourceFile.FullName -DataType $DataType
    
    if (-not $validation.IsValid) {
        $errorMsg = "Data validation failed: $($validation.Errors -join '; ')"
        $logger.Error($errorMsg)
        Send-JobFailureAlert -JobName $JobName -ErrorMessage $errorMsg -AdditionalInfo @{
            SourceFile = $sourceFile.FullName
            RowCount = $validation.RowCount
            Errors = ($validation.Errors -join "; ")
        }
        exit 1
    }
    
    $logger.Success("Validation passed: $($validation.RowCount) rows")
    
    # Step 4: Compress file
    $logger.Info("Step 4: Compressing file")
    
    $zipFileName = "$DataType_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
    $zipFilePath = Join-Path $stagingPath $zipFileName
    
    & "C:\GlobalScape\CustomCommands\Saba_Zip.ps1" `
        -SourcePath $sourceFile.FullName `
        -DestinationPath $zipFilePath `
        -LogPath "C:\GlobalScape\Logs\$JobName\Saba_Zip.log"
    
    if (-not $?) {
        throw "Compression failed"
    }
    
    $logger.Info("Compressed file created: $zipFileName")
    
    # Step 5: Transfer to Degreed
    $logger.Info("Step 5: Transferring to Degreed")
    
    # This would use GlobalScape's built-in SFTP task
    # Or a PowerShell SFTP module like Posh-SSH
    # Example:
    # $session = New-SFTPSession -ComputerName "sftp.degreed.com" -Credential $cred
    # Set-SFTPFile -SessionId $session.SessionId -LocalFile $zipFilePath -RemotePath "/upload/"
    
    $logger.Info("Transfer initiated")
    
    # Step 6: Verify transfer
    $logger.Info("Step 6: Verifying transfer")
    
    # Verification logic here
    # Could be checking SFTP directory or API confirmation
    
    $transferSuccess = $true  # Replace with actual check
    
    if (-not $transferSuccess) {
        throw "Transfer verification failed"
    }
    
    $logger.Success("Transfer verified successfully")
    
    # Step 7: Archive source file
    $logger.Info("Step 7: Archiving source file")
    
    $archiveFile = Join-Path $archivePath "$($sourceFile.BaseName)_$(Get-Date -Format 'yyyyMMdd_HHmmss')$($sourceFile.Extension)"
    Move-Item -Path $sourceFile.FullName -Destination $archiveFile -Force
    
    $logger.Info("Source file archived: $archiveFile")
    
    # Step 8: Cleanup staging
    $logger.Info("Step 8: Cleaning up staging area")
    
    Remove-Item -Path $zipFilePath -Force
    $logger.Info("Staging file removed")
    
    # Step 9: Log metrics
    $executionTime = (Get-Date) - $startTime
    
    $logger.Metric(@{
        JobName = $JobName
        DataType = $DataType
        RecordsProcessed = $validation.RowCount
        SourceFileSize = $sourceFile.Length
        CompressedFileSize = (Get-Item $zipFilePath -ErrorAction SilentlyContinue).Length
        ExecutionTimeSeconds = [Math]::Round($executionTime.TotalSeconds, 2)
        Status = "Success"
        Timestamp = (Get-Date).ToString("o")
    })
    
    # Step 10: Write success status file
    $statusFile = "C:\GlobalScape\Status\$JobName.status"
    @{
        JobName = $JobName
        LastRunTime = (Get-Date).ToString("o")
        LastRunStatus = "Success"
        LastRunError = $null
        RecordCount = $validation.RowCount
        ExecutionTimeSeconds = $executionTime.TotalSeconds
    } | ConvertTo-Json | Out-File -FilePath $statusFile -Force
    
    $logger.Success("=== Job Completed Successfully ===")
    $logger.Info("Total execution time: $($executionTime.ToString('mm\:ss'))")
    
    exit 0
    
} catch {
    $errorMessage = $_.Exception.Message
    $logger.Error("=== Job Failed ===")
    $logger.Error("Error: $errorMessage")
    $logger.Error("Stack Trace: $($_.ScriptStackTrace)")
    
    # Write failure status file
    $statusFile = "C:\GlobalScape\Status\$JobName.status"
    @{
        JobName = $JobName
        LastRunTime = (Get-Date).ToString("o")
        LastRunStatus = "Failed"
        LastRunError = $errorMessage
        RecordCount = 0
        ExecutionTimeSeconds = ((Get-Date) - $startTime).TotalSeconds
    } | ConvertTo-Json | Out-File -FilePath $statusFile -Force
    
    # Send alert
    Send-JobFailureAlert -JobName $JobName -ErrorMessage $errorMessage -AdditionalInfo @{
        ExecutionTime = ((Get-Date) - $startTime).ToString()
        ScriptStackTrace = $_.ScriptStackTrace
    }
    
    exit 1
}
```

---

## Testing Strategy

### Test Environments

| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| **Development** | Initial testing, script development | Synthetic | Developers |
| **Degreed Beta** | Integration testing | Sanitized production data | Dev + BA |
| **Production** | Live operations | Real data | Restricted |

### Test Cases

#### Test Case 1: Happy Path
- **Scenario**: Normal job execution with valid data
- **Steps**:
  1. Place valid CSV in source folder
  2. Trigger job manually or wait for timer
  3. Verify compression succeeds
  4. Verify transfer to Degreed
  5. Verify source file archived
  6. Check logs for success messages
- **Expected**: Job completes successfully, data appears in Degreed

#### Test Case 2: Retry Logic
- **Scenario**: Primary job fails, retry job succeeds
- **Steps**:
  1. Simulate primary job failure (disable Degreed connection)
  2. Verify retry job detects failure
  3. Re-enable connection
  4. Verify retry job cleans up any existing files
  5. Verify retry job processes successfully
- **Expected**: Retry identifies issue, cleans folder, completes transfer

#### Test Case 3: Multiple Files in Folder
- **Scenario**: Test the exact issue mentioned in requirements
- **Steps**:
  1. Place multiple files in Degreed staging folder manually
  2. Trigger retry job
  3. Verify pre-retry validator archives all existing files
  4. Verify new file transferred successfully
- **Expected**: Old files archived, single new file transferred

#### Test Case 4: Invalid Data
- **Scenario**: Data validation catches bad data
- **Steps**:
  1. Create CSV with missing required columns
  2. Trigger job
  3. Verify validation fails
  4. Verify alert email sent
  5. Verify job exits without transfer
- **Expected**: Job fails fast, no bad data sent to Degreed

#### Test Case 5: Network Failure
- **Scenario**: Connection to Degreed fails mid-transfer
- **Steps**:
  1. Simulate network issue during transfer
  2. Verify error handling captures issue
  3. Verify retry logic triggers appropriately
- **Expected**: Graceful failure, retry succeeds when connection restored

---

## Risk Mitigation

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Missing Saba_Zip breaks all jobs | HIGH | CRITICAL | Recreate immediately, test thoroughly, back up |
| Retry logic creates duplicate records | MEDIUM | HIGH | Implement folder cleanup, test extensively |
| API migration breaks production | LOW | CRITICAL | Run parallel systems, gradual cutover |
| Resource unavailability delays project | MEDIUM | MEDIUM | Cross-train team members, document everything |
| Degreed API changes break integration | LOW | HIGH | Version API calls, monitor Degreed release notes |
| Data corruption during transfer | LOW | HIGH | Add checksums, implement data validation |
| Security breach of credentials | LOW | CRITICAL | Use Azure Key Vault, rotate credentials regularly |

### Rollback Procedures

**If New Code Fails**:
1. Disable failing event rule immediately
2. Revert to previous version from backup (if available)
3. Manually process  any missed data files
4. Investigate root cause in dev environment
5. Implement fix and re-test before production deployment

**Rollback Scripts**:
```powershell
# Disable event rule via GlobalScape API or GUI
# If API available:
Disable-GlobalScapeEventRule -RuleName "171_Saba_Degreed_Completion_Upload_Timer"

# Manual file processing script for emergency use
Get-ChildItem "\\FileServer\Saba\Export\Completions" -Filter "*.csv" | 
    ForEach-Object {
        # Manual zip and transfer logic
    }
```

---

## Success Metrics

### Key Performance Indicators

| Metric | Current State | Target (Month 1) | Target (Month 6) |
|--------|---------------|------------------|------------------|
| **Job Success Rate** | Unknown (~60%?) | 95% | 99% |
| **Mean Time To Detect (MTTD)** | Unknown (days?) | < 1 hour | < 15 minutes |
| **Mean Time To Resolve (MTTR)** | Unknown (days?) | < 4 hours | < 1 hour |
| **Data Latency** | 24+ hours | 24 hours | 2 hours (with API) |
| **Manual Interventions** | High (weekly?) | < 1/week | < 1/month |
| **Alert Fatigue** | N/A | < 5 false alerts/week | < 1 false alert/week |

### Monitoring Dashboard

Implement PowerBI or Grafana dashboard showing:
- Job execution status (last 24 hours)
- Success/failure trends (last 30 days)
- Data volume trends
- Execution time trends
- Alert history
- System health indicators

---

## Appendix: Quick Reference Guides

### Troubleshooting Guide

**Problem**: Job fails with "Command 'Saba_Zip' does not exist"  
**Solution**: Verify custom command is registered, check path to PowerShell script

**Problem**: Retry job runs even when primary succeeded  
**Solution**: Check status file exists and contains correct status

**Problem**: Multiple files in Degreed folder  
**Solution**: Run pre-retry validator manually to clean up, investigate why not cleaned automatically

**Problem**: Data not appearing in Degreed  
**Solution**: Check GlobalScape logs, verify SFTP transfer succeeded, check Degreed import logs

**Problem**: Job times out  
**Solution**: Check data volume, optimize queries, increase timeout setting in event rule

### Emergency Contacts

| Role | Name | Email | Phone |
|------|------|-------|-------|
| GlobalScape Admin | Vinod Reddy | vinod.reddy@fmglobal.com | xxx-xxx-xxxx |
| Business Owner | Melissa Giamberardino | melissa.giamberardino@fmglobal.com | xxx-xxx-xxxx |
| Degreed Admin | John Tang | john.tang@fmglobal.com | xxx-xxx-xxxx |
| IT Operations | [TBD] | itops@fmglobal.com | xxx-xxx-xxxx |

---

**Document Status**: v1.0 - Ready for review and approval  
**Next Review Date**: March 10, 2026  
**Owner**: Stephanie Rice (Product Support) / John Tang (Product Enablement)
