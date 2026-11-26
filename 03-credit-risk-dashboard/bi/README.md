# Power BI and Tableau reporting pack

This folder extends the SEC-based Credit Risk Dashboard with a reusable company-year model for BI tools. It covers 12 issuers and 96 company-years, with derived ratios and risk bands. The Streamlit app offers the dataset as a CSV download.

## Files

- `sec_company_year_credit_risk.csv` — import-ready flat table derived from the SEC EDGAR XBRL snapshot.
- `Credit_Risk_Dashboard_PowerBI.pbix` — native Power BI Desktop report with an issuer-year detail page.
- `POWER_BI.md` — DAX measures and report interpretation guide.
- `TABLEAU.md` — Tableau calculated fields and dashboard layout.
- `DATA_DICTIONARY.md` — field meanings, formulas, and caveats.

Import the CSV into Power BI Desktop or Tableau. Treat each row as one issuer for one fiscal year. Use `company` as issuer and `year` as time. Do not sum ratio fields across companies.

## Data and interpretation

Values come from public SEC filings. Sector mapping is a manually maintained project mapping. Receivables belong to the reporting issuer and are only a scale proxy; they are not the user's bilateral exposure to that issuer. Altman Z double-prime and its bands are screening proxies, not agency ratings or calibrated default probabilities. The model does not represent BASF or any employer's internal data.

The PBIX was authored in Power BI Desktop. The Tableau calculations and dashboard layout are build instructions; a native Tableau workbook is not included.
