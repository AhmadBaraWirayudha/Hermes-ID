# Indonesia Geopolitical Risk Framework

This framework helps Hermes Analytics ID interpret market signals in a geopolitical context. It is analytical guidance, not political advice.

## Key risk dimensions

| Dimension | Market relevance | Example indicators |
|---|---|---|
| Domestic political stability | Affects fiscal policy, infrastructure, subsidies, investor confidence | election cycle, cabinet changes, budget policy, policy continuity |
| Monetary policy | Affects rates, IDR, bonds, equity valuations | Bank Indonesia rate decisions, inflation, FX reserves, current account |
| Commodity policy | Affects nickel, coal, palm oil, CPO, mineral exports | export restrictions, domestic market obligations, royalty changes |
| China and US strategic competition | Affects investment, supply chains, technology, minerals | FDI flows, sanctions, trade restrictions, battery supply chain shifts |
| ASEAN regional dynamics | Affects trade, logistics, and regional demand | ASEAN agreements, regional growth, cross-border infrastructure |
| Maritime security | Affects shipping, energy, and investor risk | South China Sea tensions, piracy risk, port disruptions |
| Climate and natural hazards | Affects agriculture, logistics, insurance, and inflation | El Nino, floods, earthquakes, haze, crop yields |
| Food and energy security | Affects inflation and social stability | rice imports, fuel subsidies, coal supply, CPO prices |
| Regulatory nationalism | Affects foreign investment and market access | local content rules, data localization, resource downstreaming |
| Digital sovereignty | Affects cloud, data, and cross-border platforms | PSE rules, PDP enforcement, cross-border data controls |

## Indonesia market implications

### Equity market

- Sensitive to global rates, IDR movement, commodity cycles, and domestic consumption.
- Banking, telecom, consumer, mining, and energy sectors may respond differently to policy shocks.

### Bond market

- Sensitive to inflation, Bank Indonesia policy, fiscal credibility, and foreign inflows.
- SBN demand may shift with global yield changes.

### Currency

- IDR may react to US dollar strength, current account dynamics, commodity exports, and foreign portfolio flows.

### Commodities

- Nickel is linked to battery supply chains and downstreaming policy.
- Palm oil and CPO are linked to food inflation, export policy, biodiesel mandates, and climate.
- Coal is linked to energy security, China and India demand, and domestic market obligations.

## Risk scoring model

Score each dimension from 1 to 5.

| Score | Meaning |
|---|---|
| 1 | low risk |
| 2 | manageable risk |
| 3 | moderate risk |
| 4 | high risk |
| 5 | severe risk |

Suggested fields:

```text
risk_date
risk_dimension
score
trigger
market_channel
affected_assets
confidence
source
analyst_note
```

## Monitoring cadence

- daily for severe events
- weekly for active macro and market events
- monthly for strategic geopolitical review
- event-driven for elections, sanctions, major regulations, war, climate shocks, or commodity bans
