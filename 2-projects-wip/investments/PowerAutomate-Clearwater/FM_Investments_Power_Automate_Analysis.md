# FM Investments - Power Automate Integration with Clearwater
## Comprehensive Analysis & Summary

**Meeting Date:** [Recorded Session]  
**Document Created:** February 19, 2026  
**Project:** Clearwater Investment System Integration

---

## Executive Summary

FM Global's Investments team has developed Power Automate Desktop flows to automate the daily process of extracting investment data from multiple investment manager portals and uploading it to their new Clearwater investment system. This automation eliminates significant manual data entry work and ensures accurate, timely position and transaction data flows into Clearwater for accounts where direct API/SFTP integration is not available.

**Current Status:** Operational in personal productivity environment  
**Objective:** Migrate to dedicated Power Platform environments with proper governance and shared infrastructure

---

## Meeting Participants

| Name | Role | Team |
|------|------|------|
| **Cliff Gray** | Solutions Architect | Investments Team (New to team) |
| **Rick Carroll** | Principal App Dev / Solutions Architect | Hobbs Brook Team (Real Estate & Investments) |
| **Morgan Halton** | Product Owner | Collaboration Platforms & Power Platform |

---

## Business Context

### The Clearwater Project

**Primary Value Proposition:**  
Clearwater Analytics was selected because it offered pre-existing connectivity to numerous banks and investment managers, promising automatic data flow for investment transactions.

**Reality:**  
While Clearwater provides broad connectivity, **not 100% coverage exists**. Currently, 5-6 investment managers lack direct connectivity to Clearwater, with the possibility of more in the future.

### Investment Manager Gap

Investment managers without Clearwater connectivity:
- Do not offer SFTP or API integration
- Only provide web portal access for data retrieval
- Require manual login and file downloads
- Use two-factor authentication (complicating automation)

**Impact:** Without automation, FM staff would need to manually log into each portal daily, extract position and transaction data, populate Clearwater templates, and transmit files.

---

## Technical Solution

### Power Automate Desktop Implementation

**Solution Type:** Power Automate Desktop (Attended Flows)

**Why Desktop vs. Cloud:**
1. **Screen scraping capability** - Required for portals without download functionality
2. **Network share access** - Needed to save files for GlobalScape SFTP transfer
3. **Browser cookie management** - Handles 2FA persistence

### Data Processing Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Daily Automation Process                         │
└─────────────────────────────────────────────────────────────────────┘

1. LOGIN PHASE
   ├── Automated login to investment manager portals
   ├── Handle 2FA (cookies stored for persistence)
   └── Access account dashboards

2. DATA EXTRACTION
   ├── Download CSVs/Excel files (preferred)
   └── Screen scrape when downloads unavailable (last resort)

3. DATA TRANSFORMATION
   ├── Parse downloaded data
   ├── Map to Clearwater GDT (Global Data Template) format
   ├── Populate required fields:
   │   ├── Position Files: As-of date, Account, CUSIP/Ticker, Shares, Price
   │   └── Transaction Files: Dividends, Stock splits, Buys/Sells
   └── Generate one Excel file per Clearwater account

4. FILE DELIVERY
   ├── Save formatted files to network share
   └── GlobalScape picks up files for SFTP to Clearwater
```

### Current Operations

**Frequency:**
- Position files: **Daily**
- Transaction files: **Daily execution**, but actual transactions are infrequent (typically quarterly for mutual funds)

**File Generation:**
- **~12 position files** created daily
- Distributed across **5 portals**
- Some portals → multiple accounts
- Some portals → single account (1:1)

**Clearwater GDT Format:**
- One spreadsheet per Clearwater account
- Position files typically contain single line item per spreadsheet

---

## Current Technical Architecture

### Environment

**Current Location:** Personal Productivity Environment  
**Primary Owner:** Rick Carroll (individual account)  
**Shared Access:** Joe Ellis (one team member)  
**Execution Location:** Rick's desktop/laptop

### Authentication & Credentials

**Current State:**
- Flows run under Rick Carroll's personal account
- Investment portal credentials stored in browser
- 2FA handled via "trust this device" cookie persistence
- Some portals haven't required re-authentication since initial setup

**Identified Risk:**
- Cookie persistence per Windows user profile
- Multiple users may conflict with stored authentication
- Potential "ping-pong" effect if different team members run flows

---

## Key Technical Challenges

### 1. Two-Factor Authentication Management

**Problem:**  
Most investment portals require 2FA, complicating automated access.

**Current Workaround:**  
Browser cookies set to "don't ask again" on trusted machine. Works well for single-user scenario but creates challenges for shared environments.

**Future Consideration:**  
Service account needed to maintain consistent cookie store across team.

### 2. Endpoint Infrastructure

**Current:** Running on developer's laptop  
**Problem:** Ties up personal machine during execution

**Solutions Under Consideration:**

| Option | Pros | Cons | Notes |
|--------|------|------|-------|
| **Azure Virtual Desktop (AVD) - Shared** | Multiple users can log in simultaneously | Auto-shutdown at 5 PM local time | Consumption-based pricing |
| **AVD - Individual** | Personal profiles preserved | Higher cost (one VM per user) | Predictable shutdown behavior |
| **Server 2025 in Data Center** | 24/7 availability, multiple RDP sessions | Office licensing complexity | Recommended option for stability |

**Critical Constraint:** Flows must be **attended** (cannot run unattended on schedule due to browser/UI interaction requirements)

**Office Licensing Consideration:**  
Microsoft licensing is per-user, not per-device. Installing Office on shared servers requires careful licensing planning.

### 3. Service Account Strategy

**Requirement:** Dedicated service account for flow execution

**Benefits:**
- Consistent browser cookie storage
- Shared credential management via Password State
- Power Platform licensing applied to service account
- Office licensing for Excel operations
- Eliminates individual user dependency

**Open Question:**  
Can multiple team members simultaneously log into a VM and execute flows under the same service account?

---

## Power Platform Governance

### Current State: Personal Productivity Environment

**Limitations of Personal Productivity:**
- Intended for individual efficiency tools
- Not designed for business-critical processes
- Limited sharing and collaboration features
- Inappropriate for systems moving millions of dollars

### Proposed: Dedicated Environments

**Environment Strategy:**

```
Investments Power Platform Structure
├── Development Environment
│   ├── Flow development and testing
│   └── POC and experimentation
├── Production Environment
│   ├── Live daily operations
│   └── Files sent to Clearwater
└── [Optional] Sandbox/Staging Environment
    └── For testing portal changes
```

**Access Control via AD Groups:**

| Role | Permissions | Intended Users |
|------|-------------|----------------|
| **Environment Maker** | Create/edit flows, full admin | Rick Carroll, Joe Ellis, Development team |
| **Environment Runner** | Execute flows only | Operations team members |
| **Environment Owner** | Full environment administration | Product owner, Lead architect |

### Power Platform Best Practices

**Environment Variables:**
- Extract repeated configuration values
- Set once at environment level
- Flows inherit values automatically
- Simplifies environment migration (Dev → Prod)

**Solution Management:**
- Export flows as .zip packages
- Import to new environments
- Maintain version control
- Team can assist with migration process

**CI/CD Considerations:**
- Morgan's team does not own CI/CD pipelines
- Teams experimenting with ADO/Octopus integration
- Platform team provides necessary permissions
- Implementation responsibility on development team
- Manual migration acceptable for infrequent changes

---

## Precedent at FM Global

### Existing Power Platform Usage

**1. Polaris Location Contacts**
- Contact management system for customer locations
- Primary/secondary contact tracking
- Phone numbers, plant contacts
- Production system

**2. ESD Department Citizen Developer App**
- Created by end user with Power Apps access
- Shared with 300+ people
- Reviewed by InfoSec and Solution Architecture
- Focus on support ownership, security, data access controls
- Approved for production use

**3. Finance Department - Mainframe Modernization**
- Partner-developed Power Apps
- Moving legacy mainframe systems to Power Platform
- Desktop automation for report generation
- Replacing manual "mouse click and wait" workflows
- Multiple automation projects in progress

### FM Global's Power Platform Philosophy

**Governance Approach:**  
*"We don't want to squash innovation and say no, we want to make sure you're doing it correctly."*

**Key Review Questions:**
1. Who owns/supports the application?
2. Who pays for licensing?
3. Does it meet FM security standards?
4. What happens if it breaks?
5. Who has access to what data?

**Approval Process:**
- Required for citizen developers promoting personal tools to departmental use
- IT-developed solutions generally exempt (SA awareness still required)
- Product owner acknowledgment
- Information security review when appropriate
- Support/ownership documentation

---

## Requirements & Next Steps

### Immediate Actions

**1. Environment Creation (1-2 weeks)**
- Schedule follow-up meeting with Chris Cahill (Platform team)
- Define environment naming conventions
- Determine environment count (Dev/Prod/Staging)
- Create environments in Power Platform admin center

**2. Active Directory Group Setup**
- Define roles (Maker, Runner, Owner)
- Create AD groups for each role
- Link groups to environment permissions
- Identify approvers (potentially Barbara from Investments)
- Coordinate with Security Admin team

**3. Service Account Provisioning**
- Request service account creation
- Store credentials in Password State
- Apply Power Platform licensing (Power Automate Desktop)
- Apply Office 365 licensing (for Excel operations)
- Configure for flow execution

**4. Solution Architecture Notification**
- Inform Phil and Mark Lesk (already aware)
- Document Power Platform usage in enterprise architecture
- Ensure SA awareness of production Power Platform deployment
- Confirm approach aligns with IT standards

**5. Information Security Review**
- Morgan to consult John Bruno (InfoSec team)
- Determine if formal security review required
- Given financial data sensitivity, ensure proper diligence
- Document security control decisions

### Infrastructure Planning

**6. Endpoint/VM Strategy**
- Decide: Shared service account vs. individual user profiles
- Decide: AVD vs. Server 2025
- Consider daily execution schedule (morning only)
- Account for attended flow requirement
- Plan for Office installation and licensing

**Recommendation:** Server 2025 in data center
- Avoids AVD auto-shutdown issues
- Supports multiple RDP sessions
- 24/7 availability
- Service Desk ticket required to initiate

**7. Migration Planning**
- Export flows from Personal Productivity environment
- Import to new Dev environment
- Configure environment variables
- Test authentication and connectivity
- Validate file generation
- Test GlobalScape pickup integration
- Migrate to Production
- Document runbook for operations team

### Long-Term Considerations

**8. Team Expansion**
- Currently: Rick Carroll, Joe Ellis
- Expand to additional team members
- Training on flow execution
- Access provisioning via AD groups
- Shared VM training/onboarding

**9. Portal Change Management**
- Investment manager portals may change layouts
- Download locations may move
- Flow updates required when portals change
- Low frequency expected (not continuous development)
- Staging environment useful for testing

**10. Additional Portal Integration**
- Currently 5-6 portals
- Possibility of additional managers without Clearwater connectivity
- Scalable pattern established
- New flows follow existing architecture

---

## Success Criteria

### Operational Metrics

✅ **Daily position file generation:** 12 files across 5 portals  
✅ **Transaction file monitoring:** Daily execution, files created when transactions occur  
✅ **Data accuracy:** Files match Clearwater GDT format specifications  
✅ **File delivery:** Files successfully transferred via GlobalScape to Clearwater  
✅ **Automation reliability:** Minimal manual intervention required  

### Governance Metrics

✅ **Environment separation:** Business-critical flows isolated from personal productivity  
✅ **Access control:** Role-based permissions via AD groups  
✅ **Team ownership:** Multiple team members capable of execution  
✅ **Infrastructure resilience:** Execution not dependent on individual laptops  
✅ **Credential security:** Service account managed in Password State  
✅ **Compliance:** InfoSec and SA awareness/approval obtained  

---

## Risk Assessment

### High Priority Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **AVD Auto-Shutdown** | Flow interruption if running past 5 PM | Use Server 2025 instead of AVD |
| **2FA Cookie Expiration** | Flow failures requiring manual re-auth | Service account strategy, cookie monitoring |
| **Portal UI Changes** | Broken screen scraping/download automation | Monitoring, staging environment testing |
| **Single Point of Failure** | Only Rick can fix/update flows | Knowledge transfer, documentation, team training |
| **Office Licensing on Server** | Complex Microsoft licensing requirements | Engage licensing team early |

### Medium Priority Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Multi-User Cookie Conflicts** | Authentication ping-pong | Service account, testing, runbook procedures |
| **Network Share Access** | GlobalScape integration failure | Service account permissions, path validation |
| **Flow Performance** | Execution time extends into AVD shutdown window | Morning-only execution schedule |

### Low Priority Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **New Investment Managers** | Additional portals to integrate | Scalable architecture already established |
| **Clearwater GDT Format Changes** | File format updates required | Change management process, Clearwater communication |

---

## Cost Considerations

### Power Platform Licensing

**Required Licenses:**
- Power Automate Desktop (per-user or per-flow license)
- Applied to service account
- Morgan's team can facilitate licensing

**Environment Costs:**
- Minimal - environments themselves are low/no cost
- Licensing tied to users and flow execution

### Infrastructure Costs

**Azure Virtual Desktop:**
- Consumption-based pricing (per hour)
- Cost savings from nightly shutdown
- Multiple AVDs if individual user approach

**Server 2025:**
- Flat monthly cost
- 24/7 availability
- Traditional VM pricing model

**Office 365 Licensing:**
- Per-user model
- Required for Excel operations
- Service account needs license

### Operational Costs

**Low Maintenance Expected:**
- Infrequent updates (not continuous development)
- Portal changes drive updates
- No CI/CD infrastructure overhead for simple manual deployments

---

## Technical Debt & Future Enhancements

### Known Limitations

**1. Attended Flows**
- Requires VM session to be active
- Cannot fully background/schedule
- Desktop automation dependencies

**2. Screen Scraping Fragility**
- UI changes break automation
- Preferred: file downloads
- Reality: Some portals require scraping

**3. Manual Trigger**
- Daily manual execution required
- Team member must initiate flows
- No unattended scheduling

### Potential Future Improvements

**If Investment Managers Add APIs:**
- Migrate from Desktop to Cloud flows
- Leverage HTTP connectors
- Remove screen scraping
- Enable true unattended execution

**Enhanced Monitoring:**
- Alerting on flow failures
- Automated error notifications
- Success/failure logging
- Integration with monitoring platforms

**CI/CD Pipeline:**
- Automated deployment Dev → Prod
- Version control in ADO
- Octopus deployments
- Requires team to build and maintain

---

## Decision Log

### Decisions Made

✅ Migrate from Personal Productivity to dedicated environments  
✅ Create separate Dev and Prod environments  
✅ Use AD groups for role-based access control  
✅ Implement service account for flow execution  
✅ Schedule follow-up with Chris Cahill for environment setup  
✅ Notify Mark Lesk and Phil (SA) of Power Platform deployment  
✅ Consult John Bruno (InfoSec) for security review determination  

### Decisions Pending

⏳ **Infrastructure Choice:** AVD vs. Server 2025  
⏳ **User Profile Strategy:** Shared service account vs. individual profiles  
⏳ **Environment Count:** Dev/Prod only vs. adding Staging/Sandbox  
⏳ **CI/CD Implementation:** Manual migration vs. automated pipeline  
⏳ **Team Access Scope:** Define full list of users needing access  
⏳ **AD Group Naming:** Establish naming conventions  

### Decisions Deferred

🔜 **Business Ownership Transfer:** Keep in IT for foreseeable future (handing to business is "pipe dream")  
🔜 **Unattended Flow Migration:** Revisit if investment managers add API access  
🔜 **Advanced Monitoring:** Implement if operational needs justify  

---

## Action Items

### Morgan Halton (Platform Team)

- [ ] Schedule follow-up meeting with Chris Cahill, Rick, and Cliff
- [ ] Consult John Bruno (InfoSec) regarding security review needs
- [ ] Provide Steve Marshall (Endpoint team) heads-up about incoming VM request
- [ ] Support environment creation (1-2 week timeline)
- [ ] Assist with flow migration via screen share
- [ ] Facilitate Power Platform and Office licensing for service account

### Rick Carroll (Investments Development)

- [ ] Continue daily flow execution in current environment until migration
- [ ] Define environment naming preferences
- [ ] Identify full team member list for AD group membership
- [ ] Work with endpoint team on VM provisioning
- [ ] Coordinate service account creation request
- [ ] Prepare flows for export/migration
- [ ] Document flow operations for team training
- [ ] Test flows in new Dev environment post-migration

### Cliff Gray (Solutions Architect)

- [ ] Notify Mark Lesk and Phil of Power Platform deployment
- [ ] Document architecture in SA repository
- [ ] Support infrastructure decision-making (AVD vs. Server)
- [ ] Coordinate with Rick on team requirements
- [ ] Ensure alignment with FM enterprise architecture standards

### Chris Cahill (Platform Team - Future)

- [ ] Lead environment naming and structure design session
- [ ] Create AD groups for environment access control
- [ ] Define environment variable strategy
- [ ] Guide flow migration process
- [ ] Configure environment permissions
- [ ] Document environment access procedures

---

## Reference Information

### FM Global Power Platform Governance

**Product Owner:** Morgan Halton  
**Scope:** Exchange, SharePoint, Teams, Power Platform  
**Philosophy:** Enable with guardrails, not prohibit  

**Historical Context:**  
"Power Platform at FM has historically been nobody wants to touch it, nobody wants to own it, but everybody wants to use it."

**Current Maturity:** Establishing best practices, formal approval processes for citizen developers, growing production usage

### Key Contacts

| Name | Role | Team |
|------|------|------|
| Morgan Halton | Product Owner | Collaboration Platforms & Power Platform |
| Chris Cahill | Platform Engineer | Collaboration Platforms |
| Mark Lesk | Solution Architect | Enterprise Architecture |
| Phil | Solution Architect | Enterprise Architecture |
| John Bruno | Information Security | InfoSec |
| Steve Marshall | Product Owner | Endpoint/Virtual Machines |
| Barbara | Business Leader | Investments (potential AD group approver) |
| Joe Ellis | Developer | Investments Team |

### Related Technologies

**Power Platform Components Used:**
- Power Automate Desktop (attended flows)
- Power Platform environments
- Environment variables

**Integration Points:**
- GlobalScape (SFTP file transfer to Clearwater)
- Network file shares
- Investment manager web portals (5-6 currently)
- Clearwater Analytics (destination system)

**Authentication:**
- Active Directory (FM Global)
- Browser-based 2FA (investment portals)
- Password State (service account storage)

---

## Glossary

**AVD (Azure Virtual Desktop):** Microsoft's cloud-based virtual desktop infrastructure  
**Clearwater:** New investment accounting system for FM Global  
**GDT (Global Data Template):** Clearwater's standardized Excel format for data uploads  
**GlobalScape:** SFTP tool for secure file transfer  
**Power Platform:** Microsoft's low-code application platform (Power Apps, Power Automate, Power BI)  
**Personal Productivity Environment:** Default Power Platform workspace for individual users  
**Attended Flow:** Power Automate process requiring active user session (vs. unattended background execution)  
**Environment Variables:** Centrally managed configuration values in Power Platform  
**AD Groups:** Active Directory security groups for access control  

---

## Appendix: Clearwater GDT File Specifications

### Position File Format

**Purpose:** Daily snapshot of investment holdings  
**Frequency:** Daily  
**One file per:** Clearwater account  
**Typical rows:** 1 (single position per account in current implementation)  

**Required Fields:**
- As-of date
- Account identifier
- CUSIP or Ticker symbol
- Number of shares
- Current price
- Additional metadata (per Clearwater spec)

### Transaction File Format

**Purpose:** Record of investment activities  
**Frequency:** Daily execution, quarterly actual data (for mutual funds)  
**One file per:** Transaction batch  

**Transaction Types:**
- Dividend declarations
- Stock splits
- Buys
- Sells
- Other corporate actions

**Required Fields:**
- Transaction date
- Transaction type
- Account identifier
- Security identifier
- Quantity/amount
- Price (where applicable)

---

## Document Control

**Author:** Compiled from meeting transcript  
**Version:** 1.0  
**Last Updated:** February 19, 2026  
**Classification:** Internal - FM Global IT  
**Related Documents:**  
- [Hobbs Brook Summary](../hobbs_brook_summary.md)
- [Investment Hobbs Brook Landscape](../investment_hobbs_brook_landscape.md)
- [LeanIX Info](../LeanIX_Info.txt)

---

## Meeting Recording

**Source:** FM Investments - Power Automate.vtt  
**Duration:** ~25 minutes  
**Format:** Teams meeting transcript

---

*End of Analysis Document*
