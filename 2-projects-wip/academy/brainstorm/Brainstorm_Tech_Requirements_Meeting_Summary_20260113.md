# Technical Requirements Meeting Summary
**Date:** January 13, 2026  
**Participants:**
- **FM Global:** Jim Gauld, Jonathan Davis, Jay Greenlee
- **Brainstorm:** Gus Hytonen, Wayne Maughan

---

## Meeting Overview
Technical discovery meeting to discuss integration options between Brainstorm's learning platform and FM Global's Learning Management System (LCO/Saba) for delivering mandatory AI training.

Left off 15:48
https://fmglobal-my.sharepoint.com/personal/johnathan_davis_fm_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fjohnathan%5Fdavis%5Ffm%5Fcom%2FDocuments%2FRecordings%2FTech%20Requirements%20Meeting%20wBrainstorm%20and%20FM%2D20260113%5F133434%2DMeeting%20Recording%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E0e3e1b48%2D09c8%2D4912%2D9ec6%2D39043a638912

Call rest api to get list of content
---

## Key Points Discussed

### FM Global's Learning Platform Context

1. **Current System:** Learning Center Online (LCO)
   - Backend: Cornerstone Saba Cloud instance
   - Also use Degreed for one organization
   - Saba is being sundowned at end of 2027

2. **Migration Plans**
   - Recently decided (a few weeks ago) to migrate to Cornerstone Learn and Galaxy platform
   - No company announcement made yet
   - Will remain on Saba through end of 2027
   - Implementation just starting

### FM Global's Requirements

1. **Primary Use Case:** Mandatory AI Training
   - Quarterly mandatory training for all FM Global employees
   - First training went out in December (AI fundamentals)
   - Next training in early March (focused on prompting) - timeline too short for integration
   - Looking for vendor partner to help with ongoing mandatory training (Q2/Q3 and beyond)

2. **Secondary Use Case:** Role-Specific Training
   - Targeted training for specific roles (e.g., field engineers)
   - Lower priority, considered "low hanging fruit"
   - Could potentially point users directly to Brainstorm platform

3. **User Experience Requirements**
   - Simplicity is critical
   - Avoid multiple clicks to access content
   - Prefer single point of entry through LCO/LMS
   - Don't want to send users to completely different platform for all training management

### Brainstorm Platform Capabilities

1. **Company Overview**
   - Microsoft Learning Partner
   - Specializes in end-user focused microlearning ("flows")
   - Dynamic content with branching based on user responses
   - Focus areas: Microsoft technologies, AI security, AI productivity
   - Tool-agnostic AI training content
   - Not a full LMS - niche focus on technology and AI training

2. **Existing Integrations**
   - Microsoft Teams, Viva Learning, SharePoint
   - SAP SuccessFactors (LMS connection)
   - Cornerstone integration in development (releasing now)
   - No pre-built Saba connection

3. **Content Format**
   - Does NOT support SCORM or AICC formats
   - Content not designed to be fully embedded in other platforms
   - Hosted on Brainstorm platform

### Integration Options Discussed

#### Option 1: Web Links (Simplest)
- **Description:** Link from LCO directly to Brainstorm courses
- **Authentication:** Single Sign-On (SSO) for seamless user experience
- **Pros:** Can implement immediately, minimal technical effort
- **Cons:** Point-in-time catalog, requires manual updates
- **Use Case:** Access point in FM University, suitable for secondary use cases

#### Option 2: API Integration (Recommended Long-term)
- **Description:** Automated connection using Brainstorm's RESTful APIs
- **Key Features:**
  - API-first platform
  - All admin portal functionality available via endpoints
  - Can pull course catalog dynamically
  - Can retrieve completion data
  - Can push assignments
  
- **Workflow:**
  1. Call API endpoint to get current course list
  2. Ingest into LCO catalog
  3. Make assignments in LCO
  4. Users launch to Brainstorm platform via URL with SSO
  5. Track completions via API calls back to Brainstorm
  
- **Pros:** 
  - Dynamic catalog updates as Brainstorm adds/updates content
  - Automated maintenance
  - Similar to LinkedIn integration FM Global already uses
  
- **Cons:**
  - Requires technical implementation
  - Need architect review
  - More setup time

#### Option 3: Export/Import
- **Description:** Export completion data from Brainstorm, import to LCO
- **Use Case:** If only need completion tracking in LMS
- **Status:** Currently available capability

### Technical Considerations

1. **Assignments Administration**
   - Can be managed in LCO OR Brainstorm, but NOT both
   - Recommendation: Pick one system to avoid conflicts
   - If assigned in LCO, performance tracked on Brainstorm platform

2. **Completion Reporting**
   - Can track in both systems simultaneously (unlike assignments)
   - Completions available via API endpoints
   - Can pull back to LMS if needed
   - Can remain in Brainstorm system only

3. **API Access**
   - API library documentation behind login
   - Need Brainstorm platform account to access
   - Gus will send account access to FM Global team

4. **Cornerstone Integration Timeline**
   - Beta launch: End of January/early February 2026
   - For Cornerstone On-Demand (not Galaxy)
   - Expanding pilot program
   - No major GA release expected beyond beta
   - Likely ready before FM Global completes Cornerstone implementation

### Reference Example

Jim mentioned FM Global's InfoSec team uses similar model:
- Vendor platform with custom content
- SCORM package exported from vendor
- Imported into LCO library
- Assignments made in LCO
- Performance tracked on vendor platform
- Vendor platform handles additional functionality (follow-up assignments, etc.)

**Note:** This won't work exactly for Brainstorm since they don't provide SCORM packages

---

## Next Steps

1. **Gus (Brainstorm):**
   - Send platform access credentials to FM Global team
   - Provide API library documentation access

2. **FM Global Team:**
   - Review Brainstorm API library
   - Get architect to evaluate integration requirements
   - Identify exact course titles/content needed

3. **Follow-up Meeting:**
   - Jonathan to schedule with Jim and John Tang
   - Review API findings
   - Discuss specific integration approach
   - Timeline: Week of January 20, 2026

4. **Future Consideration:**
   - Monitor Cornerstone integration development
   - May align with FM Global's migration timeline
   - Could simplify integration once both systems on Cornerstone

---

## Open Questions

1. Which integration approach will FM Global prefer for initial implementation?
2. Will assignments be managed in LCO or Brainstorm?
3. Where should completion tracking be the source of truth?
4. What is the specific content catalog needed for Q2/Q3 mandatory training?
5. Timeline for implementation to support Q2/Q3 training goals?

---

## Meeting Outcome

Positive discovery session with multiple viable integration paths identified. Technical feasibility confirmed for both short-term (web links) and long-term (API integration) solutions. FM Global team to conduct internal technical review before determining final approach.