# LeanIX Application Logging Information Summary

**Date:** March 3, 2026  
**Query Tool:** get_application_details.py  
**Applications Queried:** 8 (All found successfully)

---

## Executive Summary

LeanIX does not have a dedicated "logging" field in the application schema. However, the following information related to logging, monitoring, and data governance is available:

1. **ROPA Tags** (Records of Processing Activities) - Indicates data governance compliance
2. **Documents** - Links to code repositories where logging configuration may be documented
3. **IT Components** - Related infrastructure that may include logging/monitoring tools
4. **Descriptions** - May contain operational details about logging

---

## Application Details

### 1. ARGUS Enterprise
**Status:** ACTIVE  
**Owners:** Richard Carroll, Barbara Kowack-Murthy, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** None
- **Documents:** 
  - Azure DevOps Repository: [EnterpriseSecurity.Net6.0](https://dev.azure.com/fmglobal/APIChapter/_git/EnterpriseSecurity.Net6.0)
- **IT Components:**
  - Argus Data Manager (software)
- **Notes:** Logging configuration would likely be in the code repository

---

### 2. Bloomberg Anywhere
**Status:** ACTIVE  
**Owners:** Barbara Kowack-Murthy, Richard Carroll, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** `#ROPA_Finance` (Records of Processing Activities for Finance)
- **Documents:** None
- **IT Components:**
  - Bloomberg Terminal 1.x
- **Notes:** ROPA tag indicates data processing activities are documented for compliance

---

### 3. Clearwater Analytics (CWAN)
**Status:** ACTIVE  
**Owners:** Richard Carroll, Barbara Kowack-Murthy, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** None
- **Documents:** 
  - Product website: https://cwan.com/
- **IT Components:**
  - Azure Active Directory (authentication/identity management)
- **Notes:** AAD may provide authentication logging

---

### 4. NetDocuments
**Status:** ACTIVE  
**Owners:** Barbara Kowack-Murthy, Richard Carroll, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** `#ROPA_Legal` (Records of Processing Activities for Legal)
- **Documents:** None
- **IT Components:**
  - Azure Active Directory (authentication/identity management)
- **Notes:** ROPA tag indicates data processing activities are documented for compliance

---

### 5. PeopleSoft - Investment Accounting
**Status:** ACTIVE  
**Owners:** Richard Carroll, Barbara Kowack-Murthy, Gregory Velleca, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** None
- **Documents:** None
- **IT Components:**
  - GlobalSCAPE Enhanced File Transfer (file transfer logging)
  - Microsoft Windows Server
  - Oracle Database (database logging capabilities)
- **Notes:** Multiple infrastructure components likely have their own logging systems

---

### 6. Treasura
**Status:** ACTIVE  
**Owners:** Barbara Kowack-Murthy, Richard Carroll, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** `#ROPA_Finance` (Records of Processing Activities for Finance)
- **Documents:** None
- **IT Components:** None listed
- **Notes:** ROPA tag indicates data processing activities are documented for compliance

---

### 7. Yardi Real Estate Suite
**Status:** ACTIVE  
**Owners:** Richard Carroll, Barbara Kowack-Murthy, Phillip Murphy, Clifford Gray

**Logging-Related Information:**
- **Tags:** `#ROPA_Finance` (Records of Processing Activities for Finance)
- **Documents:** None
- **IT Components:**
  - Yardi Construction Manager (SaaS)
  - Yardi COROM (SaaS)
  - Yardi Deal Manager (SaaS)
  - Yardi Forecast Manager (SaaS)
  - Yardi One (SaaS)
  - Yardi Voyager (software - includes GL, AR, AP)
- **Notes:** Multiple Yardi components; vendor-managed SaaS likely has built-in logging

---

### 8. Atlas
**Status:** ACTIVE  
**Owners:** Clifford Gray, Todd Mather, Phillip Murphy  
**Observers:** Diane Hewitt

**Logging-Related Information:**
- **Tags:** `#ROPA_Engineering` (Records of Processing Activities for Engineering)
- **Documents:** Multiple Azure DevOps repositories and Veracode security information:
  - [dce-atlas-ui](https://dev.azure.com/fmglobal/DCE/_git/dce-atlas-ui)
  - [atlas-geoserver](https://dev.azure.com/fmglobal/DCE/_git/atlas-geoserver)
  - [atlas-gis-ssis](https://dev.azure.com/fmglobal/DCE/_git/atlas-gis-ssis)
  - [atlas-gis-db](https://dev.azure.com/fmglobal/DCE/_git/atlas-gis-db)
  - [Veracode Application Profile](https://analysiscenter.veracode.com/auth/index.jsp#HomeAppProfile:34278:1923478)
  - Multiple additional component repositories
- **IT Components:**
  - Microsoft SQL Server Reporting Services (has logging capabilities)
  - ESRI ArcGIS Enterprise (GIS database with logging)
  - Multiple CoreLogic and ESRI components
- **Notes:** Most comprehensive documentation and code repository links. Logging configuration likely in code repositories. Veracode integration suggests security monitoring.

---

## Recommendations for Finding Logging Information

Since LeanIX doesn't have dedicated logging fields, here's where to find actual logging information for each application:

### 1. **Applications with Code Repositories:**
   - **ARGUS Enterprise:** Check the Azure DevOps repo for logging configuration
   - **Atlas:** Check all Azure DevOps repositories for logging implementation

### 2. **Applications with ROPA Tags (Data Governance):**
   - **Bloomberg Anywhere** (#ROPA_Finance)
   - **NetDocuments** (#ROPA_Legal)
   - **Treasura** (#ROPA_Finance)
   - **Yardi Real Estate Suite** (#ROPA_Finance)
   - **Atlas** (#ROPA_Engineering)
   
   *Action:* Contact data governance team for ROPA documentation which should include data retention/logging policies

### 3. **SaaS Applications:**
   - **Clearwater Analytics**
   - **NetDocuments**
   - **Yardi components**
   
   *Action:* Check vendor documentation or admin consoles for logging settings

### 4. **Applications with Database Components:**
   - **PeopleSoft - Investment Accounting** (Oracle Database)
   - **Atlas** (SQL Server, ArcGIS Enterprise)
   
   *Action:* Check database-level audit logging and application logs

### 5. **Applications with Identity Management:**
   - **Clearwater Analytics** (Azure AD)
   - **NetDocuments** (Azure AD)
   
   *Action:* Azure AD provides authentication and access logs

---

## Next Steps

### To get actual logging configuration details:

1. **For custom/internal applications (ARGUS, Atlas):**
   - Review code repositories linked in LeanIX
   - Check Azure DevOps pipeline definitions
   - Review infrastructure-as-code configurations

2. **For ROPA-tagged applications:**
   - Contact data governance/compliance team
   - Request ROPA documentation
   - Review data retention policies

3. **For SaaS applications:**
   - Contact application administrators
   - Review vendor admin consoles
   - Check integration/monitoring dashboards

4. **For applications with database backends:**
   - Check database audit logging configuration
   - Review application connection strings and logging configs
   - Check ETL/data integration tool logs (e.g., GlobalSCAPE EFT)

5. **Additional sources not in LeanIX:**
   - Application-specific monitoring tools (e.g., Application Insights, Splunk, ELK)
   - SIEM systems
   - APM (Application Performance Monitoring) tools
   - Infrastructure monitoring (Azure Monitor, CloudWatch, etc.)

---

## Files Generated

- **JSON Data:** `results/application_details.json` (Complete query results)
- **Python Script:** `get_application_details.py` (Used to query LeanIX)
- **Summary:** This document

---

**Conclusion:** LeanIX provides architectural and governance metadata but not operational logging details. Use the repository links, ROPA documentation references, and IT component relationships as starting points to locate actual logging configurations and log data.
