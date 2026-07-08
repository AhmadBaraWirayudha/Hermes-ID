# International and National Standards Matrix

This matrix maps common standards to Hermes Analytics ID controls and implementation areas.

## Information security and cyber resilience

| Standard or framework | Scope | App relevance | Current or planned controls |
|---|---|---|---|
| ISO/IEC 27001 | Information security management system | Security governance for data, infrastructure, access, incident response | Security docs, logging, RBAC, backups, secret policy |
| ISO/IEC 27002 | Security control guidance | Detailed control implementation | Access control, operations, supplier controls, secure development |
| ISO/IEC 27017 | Cloud security controls | Cloud deployment guidance | Podman, cloud VM docs, object storage controls |
| ISO/IEC 27018 | Protection of personal data in public cloud | Cloud privacy controls | Privacy policy, data minimization, access controls |
| ISO/IEC 27701 | Privacy information management | Privacy governance | PDP mapping, privacy controls, data subject rights process |
| ISO/IEC 22301 | Business continuity management | Availability and recovery | Backup restore drills, recovery runbook, health checks |
| ISO 31000 | Risk management | Enterprise risk process | Risk register, geopolitical risk scoring |
| NIST Cybersecurity Framework 2.0 | Identify, Protect, Detect, Respond, Recover | Cyber governance | Threat model, diagnostics, logging, backups |
| NIST SP 800-53 | Security and privacy control catalog | Advanced control reference | RBAC, audit logs, contingency planning |
| CIS Controls v8 | Practical cyber hygiene | Hardening baseline | Inventory, secure configuration, vulnerability management |
| OWASP Top 10 | Web application security risks | API and UI security | Auth, rate limiting, input handling, logging |
| OWASP ASVS | Application security verification | Security testing target | Future security acceptance criteria |
| OWASP SAMM | Secure software maturity | Secure SDLC maturity | CI, dependency audit, release checklist |
| SLSA | Software supply-chain integrity | Build provenance | CI, signed releases as future control |
| SPDX and CycloneDX SBOM | Software bill of materials | Dependency transparency | Future SBOM generation |

## Privacy and data governance

| Standard or framework | Scope | App relevance | Current or planned controls |
|---|---|---|---|
| GDPR principles | International privacy benchmark | Privacy-by-design reference | Lawful basis mapping, minimization, access controls |
| OECD Privacy Guidelines | Privacy governance | Policy baseline | Collection limitation, purpose specification, safeguards |
| ISO 8000 | Data quality | Market observation quality | Data quality score, validation, profiling |
| DAMA DMBOK | Data management body of knowledge | Data governance model | Data catalog, data dictionary, lineage |
| DCAM | Data management capability assessment | Enterprise data maturity | Future maturity assessment |

## Financial technology and market data

| Standard or framework | Scope | App relevance | Current or planned controls |
|---|---|---|---|
| IOSCO principles | Securities market regulation | Market integrity reference | Disclaimers, source governance, analyst commentary policy |
| Basel operational risk principles | Operational resilience | Risk governance | Incident runbooks, continuity controls |
| FATF recommendations | AML and CFT baseline | Relevant if payments, onboarding, or regulated finance is added | AML policy placeholder and sanctions screening policy |
| ISO 20022 | Financial messaging | Future integrations | API and data model alignment if payment or bank integrations are added |
| FIX Protocol | Trading message standard | Future market connectivity | Not implemented, reference only |
| XBRL | Financial reporting taxonomy | Issuer financial statements | Potential future IDX and issuer data ingestion |
| LEI | Legal entity identifier | Entity reference data | Future entity normalization |

## AI and model governance

| Standard or framework | Scope | App relevance | Current or planned controls |
|---|---|---|---|
| ISO/IEC 42001 | AI management system | ML governance | Model registry, backtesting, model risk policy |
| NIST AI RMF | AI risk management | ML risk controls | Explainability, monitoring, validation, human oversight |
| OECD AI Principles | Responsible AI | Ethical model use | Transparency, fairness, accountability |
| EU AI Act reference | International AI benchmark | Governance benchmark | Risk classification and documentation for future use |
| Model Risk Management principles | Financial model governance | Forecast and scenario models | Backtesting, registry, validation documentation |

## Software, API, accessibility, and operations

| Standard or framework | Scope | App relevance | Current or planned controls |
|---|---|---|---|
| OpenAPI | API contract | FastAPI contract | OpenAPI export script |
| OAuth 2.0 and OIDC | Authentication standard | Future identity integration | Current API token, future OIDC |
| FAPI | Financial-grade API security | Future regulated financial API | Reference for future sensitive integrations |
| WCAG 2.2 | Accessibility | UI accessibility | Dark theme, contrast review as future control |
| ITIL 4 | IT service management | Operations | Runbooks, incident response, change management |
| SRE practices | Reliability engineering | Availability | SLOs, health checks, error budgets |
