# Credit Risk Dashboard

Standalone Streamlit dashboard using real annual SEC EDGAR company facts for 12 U.S. issuers. Shows receivables concentration by manually mapped sector and a statement-based risk-band proxy.

## Run

```bash
pip install -r requirements.txt
python build_data.py
streamlit run app.py
```

`data/annual_fundamentals.csv` is derived; accompanying JSON files are SEC source data.

**Data boundary:** public filings do not contain your counterparty book, limits, or internal ratings. The dashboard uses each filer's own accounts receivable as an exposure-scale proxy; this is not actual bilateral exposure or EAD. Sector labels are manually mapped, and risk bands are formula proxies rather than agency ratings.

## BI reporting pack

The bi/ folder contains the 96-row SEC company-year model, its data dictionary, a native Power BI Desktop report, DAX measure definitions, and Tableau calculated fields and dashboard layout. The Streamlit app includes a CSV download. No native Tableau workbook is included. See bi/README.md for interpretation limits.

Source: [SEC EDGAR company facts API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).

## Recruiter BI links

- [Download the Power BI Desktop report (.pbix)](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/Credit_Risk_Dashboard_PowerBI.pbix)
- [View the Tableau build guide](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/TABLEAU.md)
- [Download the SEC company-year data](https://github.com/Panth19/recruiter-credit-risk-portfolio/blob/main/03-credit-risk-dashboard/bi/sec_company_year_credit_risk.csv)

The Power BI report is downloadable; it is not published as a Power BI Service link. The Tableau item is a build guide, not a native Tableau workbook.
