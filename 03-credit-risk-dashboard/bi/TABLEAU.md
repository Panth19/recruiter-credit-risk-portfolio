# Tableau build guide

Connect to `sec_company_year_credit_risk.csv`. Set `cik` to String and `year` to Number (whole). Use `company` and `sector` as dimensions; set amount and ratio fields to appropriate measures.

## Calculated fields

```text
// Receivables Proxy (USD)
[exposure_proxy]

// Receivables Proxy Share
SUM([exposure_proxy]) / WINDOW_SUM(SUM([exposure_proxy]))

// Top Issuer Share
{ FIXED [year] : MAX({ FIXED [year], [cik] : SUM([exposure_proxy]) }) }
/
{ FIXED [year] : SUM([exposure_proxy]) }

// Higher Risk Proxy Flag
IF [risk_band] = "Higher risk proxy" THEN 1 ELSE 0 END
```

For `Receivables Proxy Share`, set Compute Using to the displayed company or sector dimension. The LOD-based Top Issuer Share is year-scoped; use context filters if intended filters should affect the result.

## Suggested dashboard

Build “Credit Risk Snapshot” with a year filter, KPI text for issuer count and receivables proxy, a ranked issuer bar chart, sector concentration chart, and detail table showing issuer, sector, assets, liabilities/assets, Z″ and risk band. Add “Issuer Trends” with year on columns and Z″/leverage by issuer.

**Interpretation note:** Receivables are the SEC filer’s own balance and only a scale proxy, not bilateral counterparty exposure. Z″ bands are formula screening proxies, not agency ratings or default probabilities. Sector labels are manual project mappings.

