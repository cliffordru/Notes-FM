### Meeting Overview

This meeting was a PI (Program Increment) look-ahead session focused on planning, dependencies, and updates for multiple teams and initiatives. The agenda included disaster recovery exercises, major product and platform updates, technical dependencies, and cross-team coordination for upcoming quarters.

---

### Announcements & General Updates

- **Disaster Recovery Exercise:** Scheduled for late April to early May; UAT will be unavailable during this period. Kevin Harris is the main contact for questions.
- **Meeting Structure:** Emphasis on sharing visuals, highlighting key items, and avoiding deep dives—follow-ups will be scheduled for complex issues.

---

### Team & Product Updates

#### Remote Assessment & Data Janitors (John Snyder)

- **Aegis Team:** 
  - PI2: Upgrade Esri to version 12.0 in Dev 2 sandbox as a practice run.
  - PI3: Plan to upgrade to Esri 12.1 for enterprise enablement; dependencies on VM backup, infrastructure, and workforce enablement teams.
  - Cloudflare implementation may impact timelines; awaiting more details from platform team.
- **Data Janitors (EDSR):**
  - Working on EWH integration to improve engineering data flow and reduce report generation time.
  - Targeting Q2 for portal teams to begin testing EDSR data hub integration.
  - Kamal is the main contact for EDSR integration questions.
- **Innovation Projects:**
  - Hale LE calculator in pilot phase; promising early results.
  - Fortress Fire POC advancing; may be handed to a product team depending on value and scope.
  - Fractal project ramping up; decision pending on whether to build as standalone or within SRS.
  - PeopleSoft tools upgrade requires doubling servers; critical for addressing vulnerabilities.
- **Atlas/Riskbusters:**
  - Atlas to replace remaining SIEM functionality by June; will become authoritative source for CAT data.
  - Historical imagery translations for portal’s April release; coordination with Ryan’s team.
  - Ongoing digitization of local flood maps, including international coverage.

---

#### Field and Account Engineering (Boldizsar Lassu)

- **Polaris & Project Illuminate:**
  - Main focus is enabling partial visits (prospect special and flexible special) to allow field engineers to collect targeted data.
  - Significant technical challenge: handling partial data sets and ensuring enterprise analytics remain robust.
  - Timeline and epics outlined for Polaris work; publication process involves close collaboration with BTP and other teams.
  - Portal consumption of partial visits and insights is still under discussion; no commitment from portal team yet.

---

#### Portal (Ryan Wilkes)

- **Key Initiatives:**
  - User management enhancements: division-level admin roles, improved integration with location contact management and Claim Connect.
  - Secure document sharing: policy-level security, expansion to policies and invoices, account-level risk document repository.
  - Enterprise Resilience Tracker: merging climate, fire, and boiler risk reports; initial deliverable to automate report merging for CSTs.
  - Dependencies: Data Hub/EDSR integration, Cloudflare, integrated QA, and DR exercises.
  - No commitment yet to support Project Illuminate in Q2; still in fact-finding phase.

---

#### Underwriting Systems (Pankaj Khatri)

- **Project Illuminate:** 
  - BTP will handle ordering of partial visits; integration with FSM and event-driven workflow between FE and AE.
  - Dependencies on rapid transit (Kafka/events), solution architecture, and platform teams.
- **Project Catalyst:** 
  - March deliverable for IRQ visited locations and April target for Rath’s risk analysis algorithm.
  - New POC for AI-driven insights and assistant in BTP; scope and requirements still being defined.
- **Brazil Financial Test:** 
  - Will require updated test environments, including BTP, aptitude, and possibly PeopleSoft; coordination underway.

---

#### Platform & Infrastructure (Eric Helwig, Erin Pervine, Matthew Mlyniec)

- **Cloudflare & Edge Security:**
  - PI2: Finalize architecture, migrate WAF rules and routing from Azure to Cloudflare, enable host file testing.
  - Sprints 10–13: Application teams to conduct regression/smoke tests as environments are migrated.
  - Brand cutover enablement will be ready by end of PI2; app teams can choose when to switch.
  - Breakout sessions planned for deeper technical questions.
- **GitHub Enterprise:** 
  - Architectural planning ongoing; no imminent migration, possible late-year or 2027 rollout.
- **Hasser Replacement:** 
  - POC with select apps in PI2; gradual onboarding with solution architecture involvement.
- **APIM Migration:** 
  - APIM V2 migration paused due to missing features; focus on hardening V1 and planning for APIC retirement in 2027.
- **Integrated Environments:** 
  - PI2: App teams onboard to new integrated QA; PI3: Dev onboarding.
  - Brazil FV testing will require data refresh and regression testing; timing TBD.
  - Next UAT data refresh scheduled for October unless otherwise needed.
- **Windows & SQL Server Upgrades:** 
  - Ongoing for all on-prem systems; communications led by John Dixon’s group, with Lisa Provost coordinating testing schedules.

---

#### Security (James Murphy)

- **High Risk Countries Initiative:** 
  - Focused on travel and network isolation for China, Hong Kong, and similar locations; uses Atlas travel risk layer as a source.
- **VPN Upgrade:** 
  - New solution to replace Cisco ASA by 2027; POCs planned for next PI, with goal to migrate all users by end of Q3.
- **STS Endpoint Retirement:** 
  - On-prem not affected; cloud teams must update configurations before next DR test.

---

#### Shared Services (Sushan Modak)

- **EZMAN Replacement:** 
  - Transition layer being built between internal auth and plain ID; scope may increase as on-prem systems update.
- **User Sync Re-architecture:** 
  - Dependent on Event Grid work from platform; timeline uncertain.
- **Other Initiatives:** 
  - Self-service app for test users, retiring non-HA endpoints, ongoing support for new roles and tech debt.
  - Time tracker UX improvements planned but limited by bandwidth.

---

#### Approvals, Gold Diggers, RDS, and User Management (Aislinn Walters)

- **DART & FM Approvals Customer Portal:** 
  - Replacing AIM application; built in OutSystems; dependencies with other teams are minimal but exist.
- **Blue Prism Retirement:** 
  - Migrating automations to Power Platform; CWS resources being onboarded.
- **Gold Diggers:** 
  - Supporting platform shell, notification center, and RDS; community contributions now enabled for RDS.
- **Enterprise User Management:** 
  - Separating portal user management from enterprise; phased architecture in design with solution architecture support.

---

### Key Dependencies & Risks

- **Cloudflare Migration:** Potential for minor issues; parallel testing required. Brand cutover timing is flexible for app teams.
- **PeopleSoft & Financial Testing:** Coordination needed across multiple teams for Brazil test and PeopleSoft upgrade.
- **EDSR Integration:** Portal and Data Janitors teams must align on timing and data flow for Q2 testing.
- **Platform Event Grid:** Shared Services’ user sync re-architecture depends on this; timeline not yet confirmed.
- **STS Endpoint & Windows/SQL Upgrades:** All impacted teams must update configurations and test as scheduled.

---

### Action Items & Next Steps

- **Cloudflare Breakout Session:** Eric to schedule for app teams with technical questions.
- **EDSR Integration Follow-up:** John Snyder to confirm timing and readiness for portal testing.
- **Brazil Financial Test Coordination:** Pankaj and Dave Evans to align with PeopleSoft and aptitude teams.
- **STS Endpoint Updates:** Teams to review and update configurations before DR test; Dan Weston available for support.
-