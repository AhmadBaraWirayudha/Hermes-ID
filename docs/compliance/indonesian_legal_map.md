# Indonesian Legal and Regulatory Domain Map

This document maps legal and regulatory domains that may affect Hermes Analytics ID. It is not legal advice. Confirm applicability based on the final business model, licensing status, data processing, user flows, and monetization model.

## Data protection and electronic systems

| Legal domain | Examples of relevant Indonesian instruments | Applicability to app | Controls |
|---|---|---|---|
| Personal data protection | Law No. 27 of 2022 on Personal Data Protection, PDP Law | Applies if the app processes personal data such as user accounts, portfolio profiles, risk quizzes, emails, device data, or analytics identifiers | Privacy policy, consent tracking, data minimization, data subject rights process, breach response |
| Electronic information and transactions | ITE Law and amendments, including Law No. 11 of 2008, Law No. 19 of 2016, and later amendments | Applies to electronic systems, content, online services, and digital communications | Acceptable use, content moderation, logs, security controls |
| Electronic system providers | Government Regulation No. 71 of 2019 on Electronic Systems and Transactions, plus Kominfo rules for PSE registration | May apply if operating an electronic system for Indonesian users | PSE assessment, registration review, security procedures, incident reporting |
| Cross-border data transfer | PDP Law and implementing rules when applicable | Applies if personal data is stored or processed outside Indonesia | Transfer impact review, contractual controls, safeguards |
| Cybersecurity | BSSN and Kominfo cybersecurity requirements, sectoral rules | Applies to system security and incident handling | Incident response, logging, vulnerability management, backup drills |

## Financial services, capital markets, and investment activity

| Legal domain | Examples of relevant Indonesian instruments | Applicability to app | Controls |
|---|---|---|---|
| Financial sector omnibus reform | Law No. 4 of 2023 on Financial Sector Development and Strengthening, P2SK Law | Relevant for financial services, market conduct, digital finance, and sectoral authority | Licensing analysis, product classification, regulatory perimeter memo |
| Capital markets | Capital Market Law No. 8 of 1995 and OJK capital market regulations | Relevant if providing securities recommendations, brokerage, investment management, advisory, research distribution, or order routing | Research disclaimer, licensing review, suitability controls, conflict disclosure |
| Investment advisory and financial planning | OJK regulations and licensing rules depending on service model | Relevant if the app gives personalized recommendations or portfolio advice | Suitability, risk profiling, advisory license review, human oversight |
| Mutual funds and SBN | OJK, Ministry of Finance, and distribution rules | Relevant if comparing or recommending reksa dana, SBN, or other products | Product risk disclosure, data source validation, no unauthorized distribution |
| Market data and exchange content | IDX data policies, vendor terms, and intellectual property rules | Relevant if using IDX market data, real-time feeds, or redistribution | Data license review, source attribution, caching rules, redistribution controls |
| Commodities and futures | Bappebti regulations, commodity futures laws | Relevant if providing futures, crypto asset, commodity derivative, or trading signals | Licensing review, product classification, risk disclosure |
| Banking and payment systems | Bank Indonesia rules and payment system regulations | Relevant only if payment, wallet, settlement, or BI-regulated services are added | BI licensing review, payment data security, operational risk controls |
| AML and CFT | PPATK requirements, AML CFT rules, FATF baseline | Relevant if onboarding users for transactions, accounts, payments, or regulated financial services | KYC, sanctions screening, transaction monitoring, suspicious report procedures |

## Consumer, trade, competition, tax, and advertising

| Legal domain | Examples of relevant Indonesian instruments | Applicability to app | Controls |
|---|---|---|---|
| Consumer protection | Law No. 8 of 1999 on Consumer Protection | Applies to user-facing products, claims, subscriptions, and marketing | Clear terms, refund policy, complaint handling, fair disclosure |
| Trade and e-commerce | Trade Law No. 7 of 2014, Government Regulation No. 80 of 2019 on Trading Through Electronic Systems | Applies if selling digital services to Indonesian consumers | Merchant identity, terms, invoices, consumer information |
| Competition | Law No. 5 of 1999 on Monopoly Practices and Unfair Business Competition | Relevant for partnerships, exclusivity, data-sharing arrangements | Competition review for partnerships and pricing |
| Advertising and marketing | Consumer, ITE, platform, and sectoral rules | Applies to claims about returns, speed, accuracy, and financial outcomes | Marketing review, no misleading performance claims |
| Tax | Indonesian tax laws and VAT rules for digital services | Applies to subscriptions, invoices, and revenue | Tax registration review, invoice process, VAT treatment |
| Intellectual property | Copyright, trademark, trade secret, and database rights | Applies to code, logo, content, data, reports, and brand | IP ownership, license inventory, trademark search, open-source compliance |

## Employment, outsourcing, and third parties

| Legal domain | Examples of relevant Indonesian instruments | Applicability to app | Controls |
|---|---|---|---|
| Employment and contractor law | Indonesian labor laws and outsourcing rules | Applies if hiring staff or contractors | Contracts, confidentiality, IP assignment |
| Third-party risk | OJK, BI, PDP, and general outsourcing principles depending on sector | Applies to cloud, data vendors, scrapers, analytics providers | Vendor due diligence, DPAs, SLAs, exit plan |
| Open-source licenses | MIT, Apache, GPL, BSD, and package licenses | Applies to dependencies | License review, attribution, SBOM |

## Practical legal gating questions

Before launch, answer these questions:

1. Does the app provide general research only, or personalized investment advice?
2. Does the app execute trades, route orders, hold funds, or connect to brokerage accounts?
3. Does the app redistribute licensed market data?
4. Does it process personal data, portfolio data, or financial profile data?
5. Is any data transferred outside Indonesia?
6. Does the platform charge subscription fees or commissions?
7. Are alerts framed as education, research, or recommendations?
8. Are analysts, influencers, or partners compensated for content?
9. Does the product touch crypto assets, futures, commodities, or derivatives?
10. Does the system require PSE registration or sectoral licensing?
