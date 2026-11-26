# Credit Risk Dashboard

Standalone Streamlit dashboard using real annual SEC EDGAR company facts for 12 U.S. issuers. Shows receivables concentration by manually mapped sector and a statement-based risk-band proxy.

## Run

```bash
pip install -r requirements.txt
python build_data.py
streamlit run app.py
```

`data/annual_fundamentals.csv` is derived; accompanying JSON files are SEC source data.

**Data boundary:** public filings do not contain your counterparty book, limits, or internal ratings. The dashboard uses each filer own accounts receivable as an exposure-scale proxy; this is not actual bilateral exposure or EAD. Sector labels are manually mapped, risk bands are formula proxies rather than agency ratings.

Source: [SEC EDGAR company facts API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).

## BI reporting pack

The `bi/ folder contains a 96-row SEC-based company-year CSV, data dictionary, Power BI DAX measures and page plan, and Tableau calculated fields and dashboard plan. The Streamlit app includes a CSV download for importing into either BI tool. These are build-ready definitions; no native .pbix or .twb/.twbx workbook is included. See `bi/README.md for interpretation limits.

