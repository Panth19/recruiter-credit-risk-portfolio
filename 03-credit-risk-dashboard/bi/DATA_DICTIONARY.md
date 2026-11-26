# Data dictionary

One record represents one SEC filer and fiscal year. Currency-valued fundamentals are USD as normalized by this project’s SEC company-facts extraction; missing values remain blank.

| Field | Meaning |
|---|---|
| `company`, `cik`, `year` | Issuer name, SEC Central Index Key, and fiscal year. |
| `sector` | Manual project grouping, not an official SEC classification. |
| `assets`, `current_assets`, `current_liabilities`, `total_liabilities`, `equity`, `retained_earnings`, `ebit`, `revenue`, `net_income`, `receivables`, `cash` | Selected annual fundamentals from SEC EDGAR company facts. |
| `working_capital` | Current assets minus current liabilities. |
| `current_ratio` | Current assets divided by current liabilities; blank if denominator is absent or zero. |
| `liabilities_to_assets` | Total liabilities divided by total assets. |
| `receivables_to_assets` | Receivables divided by total assets. |
| `exposure_proxy` | Equal to reported receivables, for scale/concentration demonstration only. Not bilateral exposure. |
| `z_double_prime` | 0.717×WC/assets + 0.847×retained earnings/assets + 3.107×EBIT/assets + 0.420×equity/total liabilities + 0.998×revenue/assets. Missing required components yield blank. |
| `risk_band` | Higher risk proxy at Z″ ≤ 1.23; Watch proxy at 1.23 < Z″ ≤ 2.90; Lower risk proxy above 2.90. Screening bands, not ratings or PDs. |

Use ratios as point-in-time issuer-year values. Do not aggregate ratios by summing them. Use amount fields for aggregation and recompute ratios from summed numerators/denominators only when analytically meaningful.

