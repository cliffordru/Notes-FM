# Saba → Degreed Integration via GlobalScape

## Project Overview

Improving the integration between **Saba**, **GlobalScape**, and **Degreed** (LCO - Learning Center Online) to address recurring issues and documentation gaps that have persisted for approximately 1.5 years.

## Reference Files

- **Lucid Design**: `C:\Users\grayc1\OneDrive - FM Global\all\projects\academy\saba-degreed-globalscape\LCO_Degreed.png`
- **Technical JSON**: [Saba.json](Saba.json)

---

## Current System

### GlobalScape Jobs

There are currently **9 GlobalScape jobs** managing the Saba-Degreed integration:

1. `162_Saba_ChromeRiverData_Upload_Timer`
2. `165_Saba_Photo_Upload_Timer`
3. `167_Saba_Degreed_RL_Upload_Timer`
4. `167_Saba_Degreed_RL_Upload_Timer_ReRun`
5. `168_Saba_Vemo_Upload_Timer`
6. `170_Saba_Degreed_Content_Upload_Timer`
7. `170_Saba_Degreed_Content_Upload_Timer_ReRun`
8. `171_Saba_Degreed_Completion_Upload_Timer`
9. `171_Saba_Degreed_Completion_Upload_Timer_ReRun`

---

## Meeting Notes

### January 28, 2026 - Alignment Meeting

**Recording**: [Meeting Recording](https://fmglobal-my.sharepoint.com/personal/melissa_giamberardino_fm_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fmelissa%5Fgiamberardino%5Ffm%5Fcom%2FDocuments%2FRecordings%2FAlignment%20on%20current%20Globalscape%20Saba%20%2D%2D%20Degreed%20jobs%2D20260128%5F183017UTC%2DMeeting%20Recording%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2Eb2f87cef%2Dc227%2D43e9%2D9175%2Db9921fb9baf7)

#### Action Items

- **Document Current Process** (39:09): Vinod will document the existing integration process from the GlobalScape perspective
- **Document Business Requirements** (41:43): Melissa will document her expectations and requirements for how the process should flow
  - Melissa to write up what the system *should* do
  - Vinod to write up what it *does* do
- **Compare and Align** (41:43): Vinod and Melissa will compare the technical documentation and business requirements to identify gaps and areas for improvement
- **Testing in Beta** (28:55): Any proposed changes will be tested in the Degreed beta environment before being implemented in production
- **Schedule Follow-up Meeting** (42:43): The team will reconvene in two weeks to review documentation, discuss findings, and determine further actions
- **Standardize Documentation** (42:16): The team will consider how to store and standardize requirements and architectural guidelines for GlobalScape integrations moving forward

#### Key Issues Identified

**File Handling on Retries**:
- **Desired behavior**: If there is a retry, first confirm no file in folder; if there is, delete it
- **Current issue**: Degreed only has logic to pick up a file (if there are multiple files, we do not know which one they pick up)
- **Problems**: No file scenario, multiple files scenario
- **Constraint**: GlobalScape is limited as to what it can do

---

## Available Resources

### Process Documentation
- [Lucidchart Swim Lane Process Flow](https://lucid.app/lucidchart/47b387da-4a1b-402c-9ed5-f4bf416535d4/edit?viewport_loc=-1714%2C543%2C3626%2C1812%2C0_0&invitationId=inv_6ad27ce5-cbfb-4a8a-a1de-c57ca139ce1d) - Walked through during meeting
- [Business Process Flow (Visio)](https://fmglobal.sharepoint.com/:u:/r/teams/AcademyProductTeam-LXP-DegreedAdminShared/Shared%20Documents/Degreed%20Process%20Workflows%20and%20Support/Completion%20and%20Required%20Learning%20Process%20from%20Saba%20to%20Degreed%20V1.vsdx?d=w25705c9577e641c09c84ef20739c8d00&csf=1&web=1&e=xElGK3) - Created by team and Shaun

### Testing Documents
- [Degreed Testing Documents Folder](https://fmglobal.sharepoint.com/:f:/r/teams/AcademyProductTeam-LXP-DegreedAdminShared/Shared%20Documents/Degreed%20Testing%20Documents?csf=1&web=1&e=QlkdnB)

### Current Gaps
- ❌ No solution design document available
- ❌ No technical details on GlobalScape PowerShell or jobs documented
- ❌ Design documents from original implementation period not readily available
- ⚠️ Some team members lack access to Lucidchart diagram

---

## Outstanding Questions & Next Steps

### Critical Questions (from February 25, 2026)

- **Ownership**: Someone needs to take ownership and drive this forward—we've been discussing necessary improvements for about 1.5 years. Who will own this?
- **Requirements Review**: Need to review current requirements to ensure they are still valid
- **Design Artifacts**: Develop an updated design artifact that reflects how the business requirements were implemented
- **Efficiency Analysis**: Identify where efficiencies are needed based on recurring issues
- **Documentation Reuse**: These artifacts can be reused during the new system implementation—they will just need to be refreshed
- **Access Issue**: Missing access to the Lucidchart diagram (needs resolution)
- **Attribution**: Shaun was the original creator of that business process workflow (team may have updated it since)

### Required Actions

1. **Schedule meeting** with clear agenda and defined expected outcomes
2. **Grant access** to Lucidchart diagram for all team members
3. **Determine ownership** of this initiative going forward
4. **Document current state** (Vinod - GlobalScape perspective)
5. **Document desired state** (Melissa - Business requirements)
6. **Create/update design artifacts** reflecting implementation
7. **Identify efficiency improvements** based on recurring issues

---

## Project History

### Original Implementation Team

- Paul K.
- Vinod Reddy
- Stephanie Rice
- John Tang
- Shaun
- Jim

### Historical Context

- Integration was originally designed and implemented some time ago
- Recurring issues have been discussed for approximately 1.5 years
- Request for existing documentation made at end of January meeting
- John Tang has been leading this effort for the last couple of years
- The team does not want to review raw code from JSON files—proper documentation is needed

---

## Key Stakeholders

| Name | Role | Team |
|------|------|------|
| Melissa Giamberardino (CW) | Business Analyst | Product Enablement |
| Vinod Reddy (CW) | Technical Lead | GPES Plat Enab & Sup, Internal |
| John Tang | Principal Business Analyst | Product Enablement |
| Stephanie Rice | Lead | Product Support |
| Matthew DeBlois | | |
| Cliff Gray | | |

---

## Timeline

| Date | Event |
|------|-------|
| January 28, 2026 | Initial alignment meeting (1:30 PM - 2:00 PM EST) |
| February 11, 2026 | Expected 2-week follow-up meeting (not confirmed) |
| February 24, 2026 | Follow-up requested by Melissa (1 month post-meeting) |
| February 24, 2026 | Stephanie Rice requests design documentation |
| February 24, 2026 | Vinod provides JSON file for 9 jobs |
| February 25, 2026 | John Tang provides available resources |
| February 25, 2026 | Stephanie Rice raises critical questions about ownership |
| **TBD** | **Next meeting to be scheduled** |
