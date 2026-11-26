from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
st.set_page_config(page_title="Portfolio Concentration | Credit Risk Lab", page_icon="◈", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
.stApp{background:#f7f9fa;color:#142b3b;font-family:'DM Sans',sans-serif}.block-container{max-width:1380px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:#142b3b!important;letter-spacing:-.035em}
.hero{background:linear-gradient(115deg,#102b3d,#1d4658 72%,#286577);border-radius:18px;padding:28px 34px;color:white;margin-bottom:22px;border-bottom:4px solid #d71920}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#c7dbe2;margin-bottom:9px}.hero h1{color:white!important;font-size:31px;margin:0 0 8px}.hero p{color:#d7e3e8;margin:0;font-size:14px;max-width:920px}
.section-kicker{color:#d71920;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin:24px 0 5px}
[data-testid="stMetric"]{background:white;border:1px solid #e3e9ed;padding:15px 18px;border-radius:12px;box-shadow:0 2px 8px #16364a0a}[data-testid="stMetricLabel"]{color:#647987!important;font-size:12px}[data-testid="stMetricValue"]{color:#142b3b!important;font-family:'Manrope',sans-serif}
[data-testid="stSidebar"]{background:#eef3f5;border-right:1px solid #dfe7eb}[data-testid="stDataFrame"]{border:1px solid #e3e9ed;border-radius:10px;overflow:hidden}
.note{background:#edf3f5;border-left:3px solid #d71920;border-radius:4px 10px 10px 4px;padding:13px 16px;color:#405a69;font-size:13px;margin:10px 0 18px}
</style>
<div class="hero"><div class="eyebrow">Corporate credit · Concentration reporting</div><h1>Issuer receivables &amp; sector monitor</h1><p>Explore real SEC-reported company fundamentals and compare receivables scale across issuers and sectors. Designed to demonstrate portfolio reporting and concentration analysis for credit-risk workflows.</p></div>
""", unsafe_allow_html=True)

d = pd.read_csv(APP_DIR / "data" / "annual_fundamentals.csv")
d["receivables"] = pd.to_numeric(d.receivables, errors="coerce")
d["exposure_proxy"] = d.receivables
d["sector"] = d.company.map({"Apple Inc.": "Technology", "MICROSOFT CORP": "Technology", "AMAZON.COM, INC.": "Consumer / Technology", "Walmart Inc.": "Consumer staples", "COCA COLA CO": "Consumer staples", "Exxon Mobil Corporation": "Energy", "CATERPILLAR INC": "Industrials", "THE BOEING COMPANY": "Industrials", "FedEx Corporation": "Industrials", "Ford Motor Co": "Automotive", "GENERAL MOTORS COMPANY": "Automotive", "Intel Corporation": "Technology"})
d["z_double_prime"] = .717 * (d.current_assets - d.current_liabilities) / d.assets + .847 * d.retained_earnings / d.assets + 3.107 * d.ebit / d.assets + .420 * d.equity / d.total_liabilities + .998 * d.revenue / d.assets
d["risk_band"] = pd.cut(d.z_double_prime, [-float("inf"), 1.23, 2.90, float("inf")], labels=["Higher risk proxy", "Watch proxy", "Lower risk proxy"])
bi_data = pd.read_csv(APP_DIR / "bi" / "sec_company_year_credit_risk.csv")

with st.sidebar:
    st.markdown("### Report filters")
    years = sorted(d.year.dropna().unique())
    y = st.selectbox("Fiscal year", years, index=len(years) - 1)
    x = d[(d.year == y) & d.exposure_proxy.notna()].copy()
    sectors = sorted(x.sector.dropna().unique())
    selected_sectors = st.multiselect("Sector", sectors, default=sectors)
    x = x[x.sector.isin(selected_sectors)]
    st.divider()
    st.download_button("Download BI dataset (CSV)", bi_data.to_csv(index=False).encode("utf-8"), file_name="sec_company_year_credit_risk.csv", mime="text/csv", use_container_width=True)
    st.caption("Import-ready for Power BI or Tableau.")

total = x.exposure_proxy.sum()
largest = x.exposure_proxy.max() / total if total else 0
top3 = x.nlargest(3, "exposure_proxy").exposure_proxy.sum() / total if total else 0
st.markdown('<div class="section-kicker">Selected filing universe</div>', unsafe_allow_html=True)
a,b,c,dcol = st.columns(4)
a.metric("Issuer-year records", f"{len(x):,}")
b.metric("Receivables scale proxy", f"${total / 1e9:,.1f}B")
c.metric("Largest issuer share", f"{largest:.1%}" if total else "n/a")
dcol.metric("Top three issuer share", f"{top3:.1%}" if total else "n/a")

left, right = st.columns([1.4, 1], gap="large")
with left:
    st.markdown('<div class="section-kicker">Issuer concentration</div>', unsafe_allow_html=True)
    st.subheader(f"Receivables by issuer · FY {y}")
    chart = x.sort_values("exposure_proxy", ascending=True).set_index("company")["exposure_proxy"] / 1e9
    st.bar_chart(chart, color="#1d6577", horizontal=True, height=390, x_label="Receivables (USD billions)")
with right:
    st.markdown('<div class="section-kicker">Sector mix</div>', unsafe_allow_html=True)
    st.subheader("Share of selected total")
    sec = x.groupby("sector", observed=True).exposure_proxy.sum().sort_values(ascending=False).to_frame("Receivables (USD)")
    sec["Share"] = sec["Receivables (USD)"] / sec["Receivables (USD)"].sum()
    st.dataframe(sec, use_container_width=True, column_config={"Receivables (USD)": st.column_config.NumberColumn(format="$%.0f"), "Share": st.column_config.NumberColumn(format="%.1%")})
    st.caption("Issuer-reported receivables aggregated by the dashboard's manually assigned sector labels.")

with st.expander("Issuer detail"):
    st.dataframe(x[["company", "sector", "year", "receivables", "z_double_prime", "risk_band", "assets", "total_liabilities"]].sort_values("receivables", ascending=False), use_container_width=True, hide_index=True, column_config={
        "receivables": st.column_config.NumberColumn("Receivables (USD)", format="$%.0f"),
        "z_double_prime": st.column_config.NumberColumn("Z″ screening proxy", format="%.2f"),
        "assets": st.column_config.NumberColumn("Assets (USD)", format="$%.0f"),
        "total_liabilities": st.column_config.NumberColumn("Liabilities (USD)", format="$%.0f"),
    })
st.markdown('<div class="note"><b>Important scope note:</b> Receivables are the reporting company’s own balance sheet asset. They are not BASF’s bilateral counterparty exposures, trade receivables owed to BASF, or internal credit-limit utilization. Real SEC XBRL data supports the reporting demonstration; it does not represent an actual portfolio.</div>', unsafe_allow_html=True)
st.caption("Credit Risk Reporting Lab · Sector mappings are manual; Z″ bands are formula screening proxies.")

