# Meeting Summary: FM Global Academy Projects
**Date:** January 23, 2026  
**Participants:** John Tang, Cliff Gray  
**Duration:** ~24 minutes

---

## Executive Summary

Discussion covered four key Learning & Development technology projects requiring solution architecture support. Projects range from urgent vendor replacement (June 2026 deadline) to ongoing integration improvements, all impacting FM Global's learning technology ecosystem.

---

## Projects Overview

### 1. 🔴 **Matterport Replacement** (URGENT - June 2026)
**Problem:** Current 3D walkthrough tool (Matterport) must be replaced due to unfavorable T&C identified in legal review.

**Key Requirements:**
- Must support E57 file format to migrate 150+ existing 3D workspaces
- Some locations no longer accessible for re-recording
- Needed for consultant engineering program cohort starting June 2026

**Status:** 4 vendors identified; InfoSec and procurement reviews underway

**Action Needed:** Solution architecture review of vendor options

---

### 2. 🟡 **Proofpoint LMS Integration** (MEDIUM PRIORITY)
**Problem:** InfoSec team manually creating SCORM packages, losing AI-driven personalization and adaptive learning features.

**Desired State:**
- Bidirectional integration similar to existing LinkedIn Learning model
- Users launch from Saba, content hosted on Proofpoint
- Completion data syncs between systems
- AI suggests personalized training based on performance

**Challenge:** Team lacks REST API integration expertise

**Action Needed:** Technical feasibility assessment of Proofpoint API integration with Saba

---

### 3. 🟡 **Brainstorm Integration** (MEDIUM PRIORITY)
**Problem:** Jonathan Davis requested Microsoft training content integration with similar requirements to Proofpoint.

**Requirements:** Same integration pattern as Proofpoint (bidirectional sync, single user experience)

**Action Needed:** Review Brainstorm API documentation and determine integration feasibility

---

### 4. 🟢 **Degreed Integration Issues** (LOW PRIORITY - Being Monitored)
**Problem:** Existing Saba-to-Degreed integration experiencing reliability issues causing data discrepancies.

**Current Architecture:**
```
Saba → 3 Flat Files → Globalscape (SFTP/PowerShell) → Degreed SFTP → Degreed
```

**Issues:**
- Multiple failure points (file pickup, transformation, transmission, corruption)
- Degreed only processes one file per day; missed files = lost data
- Recurring learning workaround (concatenating User ID + Content ID + Due Date)

**Action Needed:** Architecture review to identify failure points and improve error handling

**Next Steps:** Monday meeting with Globalscape team scheduled

---

## Common Themes

### Skill Gaps
- REST API development and integration
- Complex integration architecture
- Advanced SFTP/ETL troubleshooting

### Strategic Context
- **LMS Migration Pending:** Saba being sunset end of 2027, migrating to Cornerstone Galaxy
- **Integration Philosophy:** Desire for unified user experience (Saba/Degreed as front door) while leveraging specialized platforms (LinkedIn Learning, Proofpoint, Brainstorm)
- **Investment Timing:** Need to balance short-term (Saba) vs. long-term (Cornerstone) integration investments

---

## Priority Action Items

### URGENT (June 2026 Deadline)
- [ ] Solution architecture review of Matterport replacement vendors
- [ ] Validate E57 format support across vendor options
- [ ] Complete vendor selection and plan migration

### SHORT-TERM
- [ ] Assess Proofpoint REST API integration feasibility with Saba
- [ ] Review Brainstorm API documentation and integration requirements
- [ ] Evaluate if LinkedIn Learning integration pattern can be replicated

### ONGOING
- [ ] Attend Degreed/Globalscape architecture review (Monday)
- [ ] Document integration failure points and design retry mechanisms

### STRATEGIC
- [ ] Consider all integrations in context of Cornerstone Galaxy migration timeline
- [ ] Document reusable integration patterns for future implementations
