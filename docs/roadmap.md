# Roadmap

This document outlines the planned evolution of **X-Vector Pro** from core stabilizations through advanced analytics and enterprise integrations. Milestones are grouped into near-term (next 3 months), mid-term (3–9 months), and long-term (9+ months) phases.

---

## Gantt Timeline

```mermaid
gantt
    title X-Vector Pro Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b
    section Core Stabilization
    Tests & Coverage        :done,    des1, 2025-07-01, 2025-08-15
    Docs Site (MkDocs)      :active,  des2, 2025-07-15, 2025-09-01
    CI/CD Automation        :         des3, 2025-08-01, 2025-09-15

    section Plugin Framework
    Plugin API v1           :         dev1, after des3, 60d
    Third-Party Plugin Hooks:         dev2, after dev1, 45d
    Plugin Sandbox Security :         dev3, after dev2, 30d

    section Advanced Analytics
    Real-Time Dashboards    :         ana1, 2025-12-01, 90d
    Behavior-Driven Models  :         ana2, after ana1, 60d
    Threat Pattern Library  :         ana3, after ana2, 45d

    section Enterprise Integrations
    RESTful API Endpoints   :         ent1, 2026-04-01, 60d
    LDAP/AD Authentication  :         ent2, after ent1, 45d
    SaaS Multi-Tenant Mode  :         ent3, after ent2, 90d

