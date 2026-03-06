### Meeting Purpose and Context
- The meeting focused on planning and prioritizing logging assessments and remediation efforts for various applications, with the goal of building transparency and preparing for discussions with Infosec. No immediate commitments were made; the session was primarily for understanding scope, risks, and resource estimates.

### Application Categories and Prioritization
- Applications were grouped into three categories: SaaS (vendor-hosted), COTS (commercial off-the-shelf), and custom-built.
- Custom applications and those with highly restricted or mission-critical data were prioritized for assessment. SaaS apps were generally deprioritized unless they were mission-critical or contained highly restricted data.
- Specific applications discussed included Atlas, e-file, Onbase, Tridian docs, Argus, Trejura, Knowledge Portal, Sitecore, Actico, Bloomberg Anywhere, Workday, and others.

### Assessment and Remediation Estimates
- Rough Order of Magnitude (ROM) estimates were provided for assessment hours and remediation sprints for each application:
    - PeopleSoft: 60 hours for assessment; remediation estimate not provided due to uncertainty.
    - Knowledge Portal, Enterprise Search: 20 hours for assessment; 1 sprint for remediation.
    - Sitecore: 60 hours for assessment; remediation not specified.
    - Atlas: 40 hours for assessment; 2 sprints for remediation.
    - Actico, Tridian Docs: 60 hours for assessment each; remediation not specified.
    - Yardy and similar SaaS: 20 hours for assessment, time-boxed due to uncertainty.
    - Workday: Assessment required, but expected to be complex due to volume and mapping challenges.
- Remediation estimates were generally not provided for SaaS and COTS apps until assessments are completed.

### Technical and Strategic Considerations
- For SaaS, the focus is on leveraging out-of-the-box logging and determining what logs are available versus what is needed. Remediation is typically limited to what is feasible within the SaaS platform.
- Mission-criticality and data classification (especially highly restricted data) are key factors in prioritization.
- Log volume and velocity were discussed as potential cost drivers, with the need to estimate log volume per application and consider Splunk pricing models.
- Retention policies and the value of logs (e.g., whether they generate alerts) were identified as factors for future review and possible relaxation of logging posture.
- Entitlement changes and user management logs are considered the most important for SaaS applications with highly restricted data.
- Integration points, such as custom APIs and reverse proxies, were highlighted as areas for assessment, especially for applications like Actico and Enterprise Search.

### Application-Specific Notes
- Atlas: Assessment will focus on API interactions from the UI, excluding Esri ArcGIS Enterprise, which is modeled as a separate IT component.
- Onbase: Assessment already started; gaps remain to be filled. Enrichment of logs may be required, either within the COTS product or by CTDR post-ingestion.
- E-file: Marked for retirement due to migration to Atlas and SIEM retirement. No further assessment needed.
- Tridian Docs: Integration activity is already captured; direct work by business groups needs assessment.
- Sitecore: Platform-level logging should focus on configuration changes, not public usage. Apps on Sitecore are managed separately.
- Actico: All access goes through a custom reverse proxy, which could alleviate logging requirements for consumers. Admin and development activities within Actico are considered high risk and require assessment.
- Bloomberg Anywhere: Highly restricted; assessment needed to determine what is accessed and logged.
- Workday: Contains PII and high-risk business data; assessment will focus on authorization, access, and integration logs.

### Action Items and Next Steps
- Phillip to add Atlas, Onbase, and Tridian Docs assessments to their backlog for early prioritization.
- Mark to continue gathering data and prepare for further conversations with Infosec; no immediate actions for other applications.
- Team to estimate log volume per application as part of the assessment process.
- Review and update application modeling in Lean IX and DMX, especially for dependencies like Esri and Atlas.

### Open Questions and Uncertainties
- Remediation effort for COTS and SaaS apps remains uncertain until assessments are completed.
- Number of users per application was considered as a multiplier for assessment effort but was not included due to data availability challenges.
- Sufficiency and enrichment of logs for Onbase and other COTS products are pending further review.
- Scope boundaries for assessments (e.g., Workday, Atlas, Esri) need clarification as part of ongoing planning.

### Closing Remarks
- The meeting concluded with agreement to focus on prioritized assessments, defer broader actions until more data is collected, and maintain flexibility in planning pending further discussions with Infosec.
