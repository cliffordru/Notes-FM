# Investment & Hobbs Brook Technology Landscape

**Generated**: January 31, 2026  
**Purpose**: Understanding the relationship between Investment Management and Hobbs Brook asset management systems

---

## Executive Summary

FM Global's investment management technology landscape consists of **5 core applications** that support both corporate investment operations and Hobbs Brook's real estate investment subsidiary. These systems demonstrate a clear architectural pattern: **centralized corporate investment tools** (Bloomberg, Clearwater) operate alongside **dedicated Hobbs Brook investment accounting platforms** (CAMRA, ChathamDirect), with **Lease Pilot** serving as a bridge between real estate operations and investment tracking.

**Key Finding**: 60% of investment applications (3 of 5) directly support Hobbs Brook operations, indicating that Hobbs Brook represents a significant portion of FM Global's investment management technology footprint.

---

## Asset Overview

### Total Investment-Related Assets: 5 Applications

| Application | Primary Use | Business Capability | Hobbs Brook Asset |
|-------------|-------------|---------------------|-------------------|
| [Bloomberg Anywhere](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/d0a783c7-b6a2-4527-a8d9-efc30c6557b9) | Corporate Investment Data | Investments | ❌ No |
| [Clearwater Analytics](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/284af6d1-8c7c-41d7-9033-2e4e68b609e3) | Corporate Investment Operations | Investments | ❌ No |
| [CAMRA Investment Accounting](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/e6e401b8-c1c4-4b11-881e-f36c25798e76) | Hobbs Brook Tax & Accounting | Investment Accounting | ✅ Yes |
| [ChathamDirect](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/86256d0c-8949-440c-a61f-62d733e7b346) | Hobbs Brook Derivative Management | Investment Accounting | ✅ Yes |
| [Lease Pilot](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/a408f17e-cfc9-4d83-bc8c-106622af3186) | Hobbs Brook Real Estate Management | Real Estate + Investments | ✅ Yes |

---

## Technology Segmentation

### Corporate Investment Technology (2 Applications)

These systems serve FM Global's broader corporate investment management needs.

#### 1. Bloomberg Anywhere
- **Business Purpose**: Market data and communication platform for treasury and investment operations
- **Key Capabilities**:
  - Real-time currency rates and foreign exchange data
  - Bank communication for cash management
  - Web-based terminal access (3rd party hosted)
  - Financial market intelligence
- **Business Value**: Enables treasury team to make informed currency and cash management decisions
- **Technical Status**: Adequate/Appropriate fit, Active lifecycle
- **URL**: [View in LeanIX](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/d0a783c7-b6a2-4527-a8d9-efc30c6557b9)

#### 2. Clearwater Analytics
- **Business Purpose**: Enterprise investment accounting and reporting platform
- **Key Capabilities**:
  - Consolidated investment portfolio management
  - Accounting and compliance reporting
  - Performance analytics
  - Multi-asset class support
- **Business Value**: Provides comprehensive view of corporate investment portfolio with regulatory compliance capabilities
- **Technical Status**: Active lifecycle
- **URL**: [View in LeanIX](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/284af6d1-8c7c-41d7-9033-2e4e68b609e3)

---

### Hobbs Brook Investment Accounting (3 Applications)

These systems specifically support Hobbs Brook's real estate investment subsidiary operations, noted in LeanIX under "**Finance / Financial accounting / Investment accounting (e.g., Hobbs Brook, fee-for-service)**"

#### 3. CAMRA Investment Accounting
- **Business Purpose**: Tax and investment accounting specialized for Hobbs Brook operations
- **Key Capabilities**:
  - Investment accounting module with tax features
  - Hobbs Brook-specific financial tracking
  - Subsidiary accounting reconciliation
  - Investment transaction processing
- **Business Value**: Ensures accurate tax compliance and financial reporting for Hobbs Brook real estate investment entity
- **Relationship to Corporate**: Distinct from corporate investment accounting (Clearwater), focused on subsidiary-level operations
- **Technical Status**: Active lifecycle
- **Alias**: CAMRA
- **URL**: [View in LeanIX](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/e6e401b8-c1c4-4b11-881e-f36c25798e76)

#### 4. ChathamDirect
- **Business Purpose**: Interest rate derivative and hedging management for Hobbs Brook
- **Key Capabilities**:
  - Derivative instrument tracking
  - Interest rate risk management
  - Hedging strategy execution
  - Fair value calculations
  - Mark-to-market reporting
- **Business Value**: Manages financial risk associated with Hobbs Brook's real estate financing through derivative instruments
- **Relationship to Corporate**: Specialized tool for Hobbs Brook's investment hedge accounting, complementing CAMRA's core accounting
- **Technical Status**: Active lifecycle
- **URL**: [View in LeanIX](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/86256d0c-8949-440c-a61f-62d733e7b346)

#### 5. Lease Pilot
- **Business Purpose**: Commercial real estate lease administration and investment tracking
- **Key Capabilities**:
  - Lease portfolio management
  - Tenant relationship tracking
  - Rent roll and revenue forecasting
  - Property investment performance analytics
  - ASC 842 lease accounting compliance
- **Business Value**: Bridges operational real estate management with investment performance tracking for Hobbs Brook properties
- **Unique Position**: **Only application serving BOTH real estate operations AND investment capabilities**, making it a critical integration point
- **Business Capabilities**: 
  - Hobbs Brook / Real Estate
  - Investments
- **Technical Status**: Active lifecycle
- **URL**: [View in LeanIX](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/a408f17e-cfc9-4d83-bc8c-106622af3186)

---

## Business Capability Mapping

### Investment Management Hierarchy

```
Investments (Corporate)
├── Bloomberg Anywhere - Market Data & Treasury Operations
├── Clearwater Analytics - Portfolio Accounting & Reporting
└── Investments (Hobbs Brook Specific)
    └── Lease Pilot - Real Estate Investment Tracking

Finance / Financial Accounting / Investment Accounting (Hobbs Brook)
├── CAMRA Investment Accounting - Tax & Core Accounting
├── ChathamDirect - Derivative & Hedge Accounting
└── Lease Pilot - Lease Accounting & Investment Performance
```

---

## Operational Relationships

### How These Systems Work Together

#### Corporate Investment Workflow
1. **Bloomberg Anywhere** provides market data → informs treasury decisions
2. **Clearwater Analytics** consolidates all corporate investments → produces enterprise-level reports

#### Hobbs Brook Investment Workflow
1. **Lease Pilot** tracks real estate leases and property performance → generates investment returns data
2. **CAMRA Investment Accounting** processes investment transactions → handles tax accounting
3. **ChathamDirect** manages hedging instruments → provides fair value data
4. Data flows into corporate reporting systems (potentially Clearwater) for consolidated view

#### Integration Point
- **Lease Pilot** likely feeds investment performance data to both:
  - CAMRA for accounting treatment
  - Corporate systems for consolidated investment reporting

---

## Responsible Team

All 5 investment applications share the **same core responsible team**, indicating a centralized investment technology ownership model:

| Name | Role Coverage | Assets Managed |
|------|---------------|----------------|
| **Barbara Kowack-Murthy** | Primary | 5 of 5 (100%) |
| **Richard Carroll** | Primary | 5 of 5 (100%) |
| **Matthew Mlyniec** | Primary | 5 of 5 (100%) |

**Insight**: This unified ownership ensures consistent governance and technology strategy across both corporate and Hobbs Brook investment platforms.

---

## Technical Health Summary

| Metric | Status | Notes |
|--------|--------|-------|
| **Completion Rate** | 100% | All 5 applications fully documented |
| **Quality Seal** | ⚠️ 5 of 5 BROKEN | Data quality or governance issues across entire investment portfolio |
| **Lifecycle Status** | ✅ All Active | No end-of-life or phase-out concerns |
| **Functional Fit** | ✅ Appropriate/Adequate | Systems meet business requirements |

### Risk Assessment

**🔴 Critical**: All investment applications have BROKEN quality seals despite 100% completion rates. This suggests:
- Potential data integrity issues
- Missing governance controls
- Incomplete relationship mappings in LeanIX
- Opportunity for quality improvement initiative

---

## Strategic Insights

### 1. Hobbs Brook Investment Specialization
The existence of dedicated investment accounting tools (CAMRA, ChathamDirect) for Hobbs Brook indicates:
- **Regulatory complexity**: Subsidiary operations require specialized financial and tax treatment
- **Scale**: Large enough investment portfolio to justify separate systems
- **Risk management**: Sophisticated hedging strategies require specialized tools (ChathamDirect)

### 2. Technology Consolidation Opportunity?
With 5 separate investment applications, there may be opportunities to:
- Evaluate if Clearwater Analytics could absorb CAMRA/ChathamDirect functionality
- Standardize on fewer platforms to reduce complexity
- Improve integration between Lease Pilot and core accounting systems

### 3. Data Integration Maturity
The separate system landscape suggests:
- **Manual data flows** may exist between systems
- **Reconciliation overhead** between corporate and Hobbs Brook reporting
- **Potential for automation** through API integrations or data hub architecture

### 4. Investment in Real Estate Focus
3 of 5 applications (60%) support Hobbs Brook real estate operations, indicating:
- Real estate investment is a significant business line
- Technology investment reflects strategic importance of property portfolio
- Specialized needs require purpose-built solutions

---

## Business Questions for Consideration

1. **Integration**: How do CAMRA and ChathamDirect integrate with corporate systems like Clearwater?
2. **Reporting**: Is there a consolidated investment reporting workflow that spans all 5 systems?
3. **Data Quality**: What is driving the BROKEN quality seal status across all applications?
4. **Modernization**: Are there opportunities to consolidate platforms or modernize the tech stack?
5. **Growth**: As Hobbs Brook grows, will current systems scale or require replacement?

---

## Recommendations

### Short-term (0-6 months)
1. **Address Quality Seal Issues**: Audit and remediate the data quality problems causing BROKEN seals
2. **Document Integration Points**: Map data flows between these 5 systems
3. **Validate Business Capabilities**: Ensure LeanIX accurately reflects current system usage

### Medium-term (6-12 months)
1. **Integration Assessment**: Evaluate integration maturity and identify automation opportunities
2. **Vendor Roadmap Review**: Meet with Clearwater, CAMRA, ChathamDirect vendors to understand product evolution
3. **Consolidation Feasibility**: Conduct study on potential platform consolidation

### Long-term (12-24 months)
1. **Investment Technology Strategy**: Develop 3-5 year roadmap for investment platform evolution
2. **Hobbs Brook Growth Planning**: Ensure systems can scale with business growth
3. **Corporate-Subsidiary Alignment**: Determine optimal balance between unified platforms vs. specialized tools

---

## Appendix: Asset Details

### All Investment Assets by Type

**Applications (5)**:
- [Bloomberg Anywhere](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/d0a783c7-b6a2-4527-a8d9-efc30c6557b9) (Corporate Investments)
- [Clearwater Analytics](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/284af6d1-8c7c-41d7-9033-2e4e68b609e3) (Corporate Investments)  
- [CAMRA Investment Accounting](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/e6e401b8-c1c4-4b11-881e-f36c25798e76) (Hobbs Brook)
- [ChathamDirect](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/86256d0c-8949-440c-a61f-62d733e7b346) (Hobbs Brook)
- [Lease Pilot](https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/a408f17e-cfc9-4d83-bc8c-106622af3186) (Hobbs Brook Real Estate + Investments)

**IT Components**: None identified  
**Other Asset Types**: None identified

### Related Business Capabilities

1. **Investments** (Corporate-level)
2. **Finance / Financial accounting / Investment accounting (e.g., Hobbs Brook, fee-for-service)** (Subsidiary-level)
3. **Hobbs Brook / Real Estate** (Property operations)

---

**Document Owner**: Technology Products Team (via LeanIX)  
**Last Updated**: January 31, 2026  
**Next Review**: Quarterly or as investment technology landscape changes
