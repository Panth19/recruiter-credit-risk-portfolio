# Power BI build guide

## Model

Load `sec_company_year_credit_risk.csv` as `CompanyYear`. For this compact public-data demo, a single fact-like table is sufficient. Set `year` to Whole Number, `cik` to Text, amount fields to Decimal Number, and ratios to Decimal Number.

## Measures

```DAX
Issuer Count = DISTINCTCOUNT(CompanyYear[cik])

Receivables Proxy (USD) = SUM(CompanyYear[exposure_proxy])

Average Z Double Prime = AVERAGE(CompanyYear[z_double_prime])

Higher Risk Proxy Issuers =
    CALCULATE(
        DISTINCTCOUNT(CompanyYear[cik]),
        CompanyYear[risk_band] = "Higher risk proxy"
    )

Top Issuer Share =
    DIVIDE(
        MAXX(VALUES(CompanyYear[cik]), [Receivables Proxy (USD)]),
        [Receivables Proxy (USD)]
    )

Sector Concentration Share =
    DIVIDE(
        [Receivables Proxy (USD)],
        CALCULATE([Receivables Proxy (USD)], REMOVEFILTERS(CompanyYear[sector]))
    )
```

Top Issuer Share respects active year and other filters. For a separate issuer dimension, update the `VALUES` column accordingly.

## Suggested report pages

1. **Portfolio snapshot:** year slicer; issuer count, receivables proxy, top issuer share cards; issuer bar chart.
2. **Concentration:** sector share chart, issuer ranking, sector and year slicers.
3. **Financial screen:** issuer-year table with leverage, current ratio, Z″ and risk band; conditional formatting by band.

Add a visible note: “Receivables are the SEC filer’s own balance and a scale proxy, not bilateral counterparty exposure. Z″ bands are screening proxies, not ratings or PDs.”

