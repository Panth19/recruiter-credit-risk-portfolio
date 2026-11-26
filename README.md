# Counterparty and Corporate Credit Risk Portfolio

Three public Streamlit demos aligned with corporate counterparty risk and credit analysis.

## Best match for Counterparty Risk Management

**Project 1, Counterparty Exposure and Limit Monitor, is the closest match to the BASF internship.** It demonstrates a daily counterparty-risk workflow: revalue forward trades under market scenarios, net exposures by counterparty, calculate EPE/PFE, compare peak PFE with limits, and prioritize names with low headroom. The app is a model demonstration; its trade book, market inputs and limits are synthetic, so it does not claim BASF or real client portfolio experience.

Projects 2 and 3 complement it with real SEC EDGAR company fundamentals and credit-reporting views. They show corporate financial statement analysis and concentration reporting, while explicitly treating receivables and Z double-prime as proxies. For a recruiter, start with Project 1, then use Projects 2 and 3 to show statement analysis and reporting skills.

| Project | Demonstration | Live app |
|---|---|---|
| Counterparty Exposure and Limit Monitor | Correlated Monte Carlo pricing, netting, EPE/PFE, and limit breach flags | [Open app](https://recruiter-credit-risk-portfolio-xxewrm6dnrxutaprqfxonb.streamlit.app/) |
| Corporate Counterparty Scoring | SEC financial statement ratios and transparent Z double-prime screening | [Open app](https://corporate-counterparty-screen.streamlit.app/) |
| Credit Risk Dashboard | SEC-based receivables scale proxy and sector concentration view | [Open app](https://credit-risk-concentration-dashboard.streamlit.app/) |

Projects 2 and 3 use a compact CSV snapshot derived from SEC EDGAR XBRL company facts (12 public issuers, 96 company-years). Project 1 uses synthetic illustrative trades, market assumptions, and limits. See each project README for assumptions and limitations.

The Credit Risk Dashboard also includes an SEC-based BI reporting pack: import-ready company-year data, Power BI DAX measures, Tableau calculations, and a data dictionary in the project bi/ folder. The Streamlit dashboard offers a CSV download.

## Run locally

```bash
pip install -r requirements.txt
streamlit run 01-counterparty-exposure-limit-monitor/app.py
```

To run Projects 2 or 3, replace the entrypoint path with the corresponding app.py. Streamlit Community Cloud supports multiple apps in one repository; select each app path during deployment.

The Credit Risk Dashboard includes the native Power BI Desktop file at 03-credit-risk-dashboard/bi/Credit_Risk_Dashboard_PowerBI.pbix, plus Tableau calculation and layout instructions.

## BI project links

- [Download the Power BI Desktop report (.pbix)](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/Credit_Risk_Dashboard_PowerBI.pbix)
- [View the Tableau build guide](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/TABLEAU.md)
- [Download the SEC company-year dataset](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/sec_company_year_credit_risk.csv)

The Power BI file is downloadable, not a public Power BI Service report. The Tableau item is a build guide; a native Tableau workbook is not included.

