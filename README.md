# Counterparty and Corporate Credit Risk Portfolio

Three public Streamlit demos aligned with corporate counterparty risk and credit analysis.

| Project | Demonstration | Live app |
|---|---|---|
| Counterparty Exposure and Limit Monitor | Correlated Monte Carlo pricing, netting, EPE/PFE, and limit breach flags | [Open app](https://recruiter-credit-risk-portfolio-xxewrm6dnrxutaprqfxonb.streamlit.app/) |
| Corporate Counterparty Scoring | SEC financial statement ratios and transparent Z double-prime screening | [Open app](https://corporate-counterparty-screen.streamlit.app/) |
| Credit Risk Dashboard | SEC-based receivables scale proxy and sector concentration view | [Open app](https://credit-risk-concentration-dashboard.streamlit.app/) |

Projects 2 and 3 use a compact CSV snapshot derived from SEC EDGAR XBRL company facts (12 public issuers, 96 company-years). Project 1 uses synthetic illustrative trades, market assumptions, and limits. See each project README for assumptions and limitations.

## Run locally

```bash
pip install -r requirements.txt
streamlit run 01-counterparty-exposure-limit-monitor/app.py
```

To run Projects 2 or 3, replace the entrypoint path with the corresponding `app.py`. Streamlit Community Cloud supports multiple apps in one repository; select each app path during deployment.

The Credit Risk Dashboard also includes an SEC-based BI reporting pack: import-ready company-year data, Power BI DAX measures, Tableau calculations, and a data dictionary under `03-credit-risk-dashboard/bi/`. The Streamlit dashboard offers a CSV download.


The Credit Risk Dashboard includes the native Power BI Desktop file at `03-credit-risk-dashboard/bi/Credit_Risk_Dashboard_PowerBI.pbix`, plus Tableau calculation and layout instructions.

## BI project links

- [Download the Power BI Desktop report (.pbix)](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/Credit_Risk_Dashboard_PowerBI.pbix) — opens in Power BI Desktop or can be imported into the Power BI service.
- [View the Tableau build guide](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/TABLEAU.md) — calculated fields and dashboard layout for rebuilding the views in Tableau.
- [Download the SEC company-year dataset](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/sec_company_year_credit_risk.csv).

The Power BI file is a downloadable report, not a public Power BI Service report link. A native Tableau workbook is not included.
