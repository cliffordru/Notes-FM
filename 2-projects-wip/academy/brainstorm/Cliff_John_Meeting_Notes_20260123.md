# Meeting Notes: FM Global Academy Projects Discussion
**Date:** January 23, 2026  
**Participants:** John Tang, Cliff Gray  
**Duration:** ~24 minutes

---

## Table of Contents
1. [Matterport Replacement Project](#1-matterport-replacement-project)
2. [Proofpoint LMS Integration](#2-proofpoint-lms-integration)
3. [Brainstorm Integration](#3-brainstorm-integration)
4. [Degreed Integration Issues](#4-degreed-integration-issues)

---

## 1. Matterport Replacement Project

### Overview
FM Global needs to replace Matterport, the 3D walkthrough tool used for virtual facility access in training programs, due to unfavorable terms and conditions identified during a recent legal review.

### Background
- **Tool:** Matterport (3D walkthroughs/virtual tours)
- **Duration of Use:** 4-5 years
- **Payment Method:** Corporate card (flying under the radar - not formally reviewed by InfoSec or in solution inventory)
- **Initial Adoption:** Started during COVID when physical building access was limited
- **Current Usage:** ~150 workspaces with 3D recordings
- **Primary Use Case:** Embedded in consultant engineering program curriculum

### Key Requirements
1. **E57 Format Support** (Critical)
   - Must support E57 file format for importing existing 3D renderings
   - Some physical locations no longer accessible for re-recording
   - Migration of 150+ existing workspaces required

2. **Use Case:**
   - 3D walkthroughs embedded into LMS curriculums
   - Virtual facility tours for training purposes
   - No user tracking/assessment data in Matterport (handled by LMS and LCO)

### Vendor Evaluation Process
- **Vendor Shortlist:** 4 potential vendors identified
- **Target:** Narrow down to 2-3 vendors
- **Due Diligence Completed:**
  - NDA sent to at least one vendor
  - Risk Recon review completed by InfoSec (Mike)
  - PureIQ review requested from Procurement (Don)
  - Business requirements list received

### Timeline
- **Target Completion:** June 2026
- **Driver:** Next cohort of consultant engineering program starts in June

### Stakeholders
- **Business:** Consultant Engineering Program team
- **Legal:** Legal review team (identified T&C issues)
- **InfoSec:** Mike (Risk Recon)
- **Procurement:** Don (PureIQ review)
- **Solution Architecture:** Tamur (requested for vendor review assistance)

### Current Status
- Actively researching replacement vendors
- InfoSec and procurement reviews underway
- Requirements gathering complete
- Seeking solution architecture guidance for vendor selection

### Next Steps
- Solution architecture review of vendor options
- Complete vendor evaluation and selection
- Plan migration of existing E57 files
- Implementation before June 2026 cohort

---

## 2. Proofpoint LMS Integration

### Overview
InfoSec team (Steve McGrath and Mary Someraro) seeking integration between FM Global's LMS (Saba) and Proofpoint, a specialized information security training platform.

### Background
- **Current Process:** Manual SCORM package creation
  - Steve curates security content from Proofpoint
  - Builds SCORM packages manually
  - Uploads to Saba LMS
  - Time-consuming and limits functionality

### Business Case
**Lost Capabilities with Current Approach:**
- **AI-Driven Personalization:** Proofpoint can suggest additional training based on assessment performance
- **Adaptive Learning Paths:** System identifies weak areas and recommends targeted content
- **Real-time Content Access:** Direct access to Proofpoint's full library vs. manual curation

**Example Use Case:**
- User scores poorly on phishing course
- Proofpoint AI automatically suggests remedial training
- System builds personalized improvement plan

### Technical Challenges
1. **REST API Review Needed**
   - Proofpoint provided API documentation via their trust center
   - Team lacks technical expertise to evaluate integration feasibility
   - Need to determine if Saba can integrate with Proofpoint's API

2. **User Experience Concerns**
   - Don't want users navigating between two different LMS experiences
   - Prefer Saba as single launching point
   - Want to avoid dual-LMS user experience

### Desired Integration Model
Similar to existing **LinkedIn Learning Integration:**
- Bidirectional feed between systems
- Content library imported into Saba
- Users launch courses from Saba
- Content hosted on external platform (deployed SCORM)
- Completions sync back to both systems
- Nightly job updates transcripts in both directions

### Current FM Infrastructure
- **LMS:** Saba (being sunset end of 2027)
- **Future LMS:** Cornerstone Galaxy (migration planning in progress)
- **Configuration Support:** Jim Gauld (Senior Configuration Analyst)
  - Full admin rights to Saba
  - Can handle basic integrations (SSO, key updates)
  - Limited REST API expertise

### Constraints
- Gap in technical skill set for REST API integration
- Need architectural guidance on feasibility
- Must maintain single-system user experience

### Stakeholders
- **InfoSec:** Steve McGrath, Mary Someraro
- **Learning Technology:** John Tang team
- **Configuration:** Jim Gauld
- **Solution Architecture:** Seeking Tamur's assistance

### Current Status
- Initial conversations with Proofpoint complete
- API documentation received
- Awaiting technical feasibility assessment

---

## 3. Brainstorm Integration

### Overview
Jonathan Davis requested integration with Brainstorm, a vendor providing Microsoft training content, with very similar requirements to the Proofpoint integration.

### Key Details
- **Purpose:** Microsoft training content delivery
- **Vendor:** Brainstorm
- **Documentation:** API documentation provided by vendor
- **Request Timing:** Earlier in the week (before meeting date)

### Integration Requirements
- Similar to Proofpoint integration needs
- Need to review API documentation
- Determine feasibility with current LMS (Saba)
- Evaluate integration architecture

### Stakeholders
- **Requestor:** Jonathan Davis
- **Learning Technology:** John Tang team
- **Solution Architecture:** Seeking assistance

### Current Status
- Initial request received
- API documentation available
- Pending technical review

---

## 4. Degreed Integration Issues

### Overview
Existing integration between Saba (LMS) and Degreed (LXP) experiencing reliability issues with data synchronization, particularly for recurring/required learning.

### Background
- **Degreed:** Learning Experience Platform (LXP) - the "front door to learning" for FM users
- **Goal:** Users access all learning through Degreed, but required learning managed in Saba
- **Integration Age:** Couple of years in production

### Technical Architecture

#### Current Integration Flow:
```
Saba LMS → 3 Flat Files → Globalscape (SFTP/transformation) → Degreed SFTP → Degreed LXP
```

#### The Recurring Learning Problem:
**LMS Approach (Saba):**
- Courses set on recurring cycles (e.g., annual)
- Course expires and gets re-added to transcript
- Same content ID used for recurring instances

**LXP Limitation (Degreed):**
- Keys off content ID only
- Sees course as "complete" if completed previously
- No logic for recurring/expiring requirements
- Not designed for required learning management

#### The Workaround Solution:
**Via Globalscape PowerShell Processing:**
1. Saba exports 3 flat files daily
2. Globalscape appends unique key to create distinct identifier
3. Concatenates: `User ID + Content ID + Due Date`
4. Creates unique identifier per recurrence cycle
   - Example: Harassment course 2025 vs. 2026 = different IDs
5. Sends modified files to Degreed SFTP

### Integration Issues

#### Reliability Problems:
1. **File Pickup Failures**
   - Globalscape fails to retrieve files from Saba
   
2. **Transformation Errors**
   - PowerShell concatenation job issues
   
3. **Transmission Problems**
   - Connection issues to Degreed SFTP
   
4. **File-in-Transit Corruption**
   - Files corrupted during transfer

#### Degreed Processing Constraints:
1. **Timer-Based Ingestion**
   - Jobs run on fixed schedule
   - Files dropped after job execution wait until next day
   
2. **Single File Per Day Limit**
   - Only processes most recent file
   - If 2 files queued, older file ignored
   - Missing records from skipped files

3. **No Retry Mechanism**
   - Missed files = lost data
   - Manual intervention required

### Data Quality Impact
- **Primary Issue:** Data discrepancies between Saba and Degreed
- **Manifestation:** Required learning not appearing in Degreed
- **Troubleshooting Challenge:** Failures occur at multiple points in workflow
- **User Impact:** Incomplete required learning visibility

### Monitoring Challenges
- **Confirmation Messages Implemented:** Globalscape sends success notifications
- **False Positives Identified:** Success messages don't guarantee end-to-end completion
- **Limited Visibility:** Difficult to identify failure point in multi-step process

### Proposed Solution Approach
1. **Architecture Review**
   - Evaluate entire integration workflow
   - Identify failure points and bottlenecks
   - Assess whether current approach is optimal

2. **Error Handling Improvements**
   - Add job rerun capabilities
   - Implement error flags and alerts
   - Build automated recovery processes

3. **Validation Enhancements**
   - Better end-to-end confirmation
   - Data reconciliation checks
   - Proactive failure detection

### Stakeholders
- **Learning Technology:** John Tang, Melissa
- **Configuration:** Jim Gauld
- **Infrastructure:** Globalscape team
- **Vendor:** Degreed
- **Solution Architecture:** Tamur (requested for review)

### Meeting Scheduled
- **When:** Monday (meeting invite from Melissa)
- **Purpose:** Review Globalscape process
- **Attendees:** Globalscape team, learning technology team, solution architecture

### Current Status
- **Priority:** Lowest (workarounds available)
- Issues identified and documented
- Architecture review meeting scheduled
- Lucid chart workflow diagram created
- Seeking architectural guidance for optimization

---

## Cross-Cutting Themes

### Common Needs Across Projects
1. **Solution Architecture Expertise**
   - API integration feasibility assessments
   - Integration pattern recommendations
   - Technical architecture review

2. **Integration Capabilities**
   - REST API integrations
   - SCORM/xAPI standards
   - Bidirectional data synchronization

3. **LMS Ecosystem Complexity**
   - Multiple platforms (Saba, Degreed, Proofpoint, Brainstorm, LinkedIn Learning)
   - Pending LMS migration (Saba → Cornerstone Galaxy by end of 2027)
   - Balance between centralized and specialized systems

### Technical Skill Gaps
- REST API development and integration
- Complex integration architecture
- Advanced SFTP/ETL troubleshooting

### Strategic Considerations
- **LMS Migration Timeline:** Saba sunset end of 2027
- **Investment Decisions:** Short-term (Saba) vs. long-term (Cornerstone Galaxy)
- **User Experience:** Desire for unified learning portal despite multiple backend systems

---

## Action Items

### Immediate (Matterport - June 2026 Deadline)
- [ ] Solution architecture review of 4 vendor options
- [ ] Validate E57 format support
- [ ] Complete vendor selection
- [ ] Plan migration strategy

### Short-Term (LMS Integrations)
- [ ] Technical feasibility assessment for Proofpoint REST API integration
- [ ] Review Brainstorm API documentation and integration requirements
- [ ] Evaluate integration patterns (similar to LinkedIn Learning model)

### Ongoing (Degreed Integration)
- [ ] Attend Globalscape review meeting (Monday)
- [ ] Document failure points in current workflow
- [ ] Design error handling and retry mechanisms
- [ ] Implement data reconciliation processes

### Strategic
- [ ] Consider integration roadmap in context of Cornerstone Galaxy migration
- [ ] Evaluate consolidated vs. specialized LMS strategy
- [ ] Document integration patterns for future implementations
