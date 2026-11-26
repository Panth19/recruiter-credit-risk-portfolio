# Power BI and Tableau reporting pack

This folder extends the SEC-based Credit Risk Dashboard with a reusable company-year model for BI tools. It contains the same 12 issuers and 96 company-years as the Streamlit project, with derived ratios and risk bands. The Streamlit app offers the dataset as a CSV download.

## Files

- `sec_company_year_credit_risk.csv` — import-ready flat table derived from SEC EDGAR XBRL snapshot.
- `POWER_BI.md` — suggested model, DAX measures, and report layout.
- `TABLEAU.md` — calculated fields and dashboard layout.
- `DATA_DICTIONARY.md` — field meanings, formulas, and caveats.

Import the CSV into Power BI Desktop or Tableau. Treat each row as one issuer for one fiscal year. Use `company` as issuer and `year` as time. Do not sum ratio fields across companies.

## Data and interpretation

Values come from public SEC filings. Sector mapping is a manually maintained project mapping. Receivables belong to the reporting issuer and are only a scale proxy; they are not the user's bilateral exposure to that issuer. Altman Z double-prime and its bands are screening proxies, not agency ratings or calibrated default probabilities. The model does not represent BASF or any employer's internal data.

Power BI DAX and Tableau calculation definitions are source instructions. This repository does not contain a native `.pbix` or `.twb/.twbx` workbook.

