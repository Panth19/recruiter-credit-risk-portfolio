from pathlib import Path
import sys
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
P1 = ROOT / "01-counterparty-exposure-limit-monitor"
P2 = ROOT / "02-corporate-counterparty-scoring"
P3 = ROOT / "03-credit-risk-dashboard"
sys.path.insert(0, str(P1)); sys.path.insert(0, str(P2))
from exposure import simulate
from score import score

st.set_page_config(page_title="Counterparty & Credit Risk Portfolio", page_icon="📊", layout="wide")
st.title("Counterparty & Corporate Credit Risk Portfolio")
st.caption("Three interactive projects in one place | BASF internship portfolio demo")
project = st.selectbox("Choose a project", ["Counterparty Exposure Monitor", "Corporate Counterparty Scoring", "Credit Risk Dashboard"])

if project == "Counterparty Exposure Monitor":
    st.subheader("Monte Carlo exposure and limit monitoring")
    st.caption("Illustrative commodity and FX forward book; sample trades and market assumptions are synthetic.")
    trades = pd.read_csv(P1 / "data" / "trades.csv")
    limits = pd.read_csv(P1 / "data" / "limits.csv")
    with st.sidebar:
        st.header("Simulation settings")
        n_sims = st.select_slider("Scenarios", options=[1000, 2500, 5000, 10000], value=5000)
        horizon = st.slider("Horizon (months)", 6, 36, 24)
        rate_pct = st.slider("Flat discount rate (%)", 0.0, 10.0, 3.5, 0.5)
        seed = st.number_input("Random seed", 0, 1_000_000, 42)
    @st.cache_data(show_spinner="Simulating market paths and exposures…")
    def run_sim(trade_data, limit_data, n, months, rate, random_seed):
        return simulate(trade_data, limit_data, n, months, rate, random_seed)
    profile, summary, _ = run_sim(trades, limits, int(n_sims), int(horizon), rate_pct/100.0, int(seed))
    a,b,c = st.columns(3); a.metric("Counterparties", len(summary)); b.metric("PFE95 limit breaches", int(summary.breach.sum())); c.metric("Scenarios", f"{int(n_sims):,}")
    st.subheader("Limit summary")
    view = summary.copy(); view["Status"] = view.breach.map({True:"BREACH",False:"Within limit"})
    st.dataframe(view[["counterparty","credit_limit","peak_EPE","peak_PFE95","peak_PFE99","headroom_to_PFE95","Status"]], width="stretch")
    selected = st.selectbox("Exposure profile", summary.counterparty.tolist())
    p = profile[profile.counterparty==selected].set_index("year_fraction")
    st.line_chart(p[["EPE","PFE95","PFE99","credit_limit"]], y_label="USD")
    st.caption("Counterparty trades are netted, positive net exposure is measured, and PFE95 is compared with the stated limit. Collateral, wrong-way risk, CVA, stochastic rates, and basis risk are omitted.")
    with st.expander("Illustrative trade book"):
        st.dataframe(trades, width="stretch"); st.dataframe(limits, width="stretch")

elif project == "Corporate Counterparty Scoring":
    st.subheader("Financial statement screening")
    st.caption("Real SEC EDGAR filings | Altman Z double-prime screening proxy, not a default prediction or agency rating")
    df = pd.read_csv(P2 / "data" / "annual_fundamentals.csv")
    d = score(df).dropna(subset=["z_double_prime"])
    years = sorted(d.year.unique()); year = st.selectbox("Fiscal year", years, index=len(years)-1)
    period = d[d.year==year].sort_values("z_double_prime")
    company = st.selectbox("Company", period.company.tolist())
    row = period[period.company==company].iloc[0]
    a,b,c = st.columns(3); a.metric("Book-equity Z double-prime", f"{row.z_double_prime:.2f}"); b.metric("Screening band", str(row.band)); c.metric("Current ratio", f"{row.current_assets/row.current_liabilities:.2f}" if row.current_liabilities else "n/a")
    st.subheader("Company-year screen")
    st.dataframe(period[["company","year","z_double_prime","band","assets","total_liabilities","equity","revenue"]], width="stretch")
    st.subheader("Score trend")
    st.line_chart(d[d.company==company].set_index("year")["z_double_prime"], y_label="Z double-prime")
    st.info("The zone cutoffs are a coarse screen using book equity. These filings do not provide verified default labels or agency ratings; interpret with analyst review and external credit evidence.")

else:
    st.subheader("Receivables concentration view")
    st.caption("Real SEC EDGAR financials | the filers’ own receivables are only an exposure-scale proxy")
    d = pd.read_csv(P3 / "data" / "annual_fundamentals.csv")
    d["receivables"] = pd.to_numeric(d.receivables, errors="coerce")
    d["sector"] = d.company.map({"Apple Inc.":"Technology","MICROSOFT CORP":"Technology","AMAZON.COM, INC.":"Consumer / Technology","Walmart Inc.":"Consumer staples","COCA COLA CO":"Consumer staples","Exxon Mobil Corporation":"Energy","CATERPILLAR INC":"Industrials","THE BOEING COMPANY":"Industrials","FedEx Corporation":"Industrials","Ford Motor Co":"Automotive","GENERAL MOTORS COMPANY":"Automotive","Intel Corporation":"Technology"})
    d["z_double_prime"] = .717*(d.current_assets-d.current_liabilities)/d.assets + .847*d.retained_earnings/d.assets + 3.107*d.ebit/d.assets + .420*d.equity/d.total_liabilities + .998*d.revenue/d.assets
    d["risk_band"] = pd.cut(d.z_double_prime,[-float("inf"),1.23,2.90,float("inf")],labels=["Higher risk proxy","Watch proxy","Lower risk proxy"])
    years = sorted(d.year.dropna().unique()); year = st.selectbox("Fiscal year", years, index=len(years)-1)
    period = d[(d.year==year)&d.receivables.notna()].copy()
    sectors = sorted(period.sector.dropna().unique()); selected_sectors = st.multiselect("Sector", sectors, default=sectors)
    period = period[period.sector.isin(selected_sectors)]
    total = period.receivables.sum()
    a,b,c = st.columns(3); a.metric("Companies with receivables", len(period)); b.metric("Aggregate receivables proxy", f"${total/1e9:,.1f}B"); c.metric("Largest company share", f"{period.receivables.max()/total:.1%}" if total else "n/a")
    st.subheader("Receivables by company"); st.bar_chart(period.set_index("company").receivables.sort_values(ascending=False), y_label="USD")
    st.subheader("Sector concentration")
    sector_table = period.groupby("sector", observed=True).receivables.sum().sort_values(ascending=False).to_frame("receivables_proxy_usd")
    sector_table["share"] = sector_table.receivables_proxy_usd / total if total else 0
    st.dataframe(sector_table, width="stretch")
    st.subheader("Company view"); st.dataframe(period[["company","sector","year","receivables","z_double_prime","risk_band","assets","total_liabilities"]], width="stretch")
    st.info("Public filings do not disclose your own bilateral exposures, limits, or internal ratings. Receivables are the filers’ balances, not exposure to your portfolio. Sector and risk bands are manually mapped proxies, not agency ratings.")

st.divider()
st.caption("Portfolio demo for learning and discussion. Project 1 inputs are synthetic; Projects 2 and 3 use SEC-reported company facts and clearly labeled proxies.")
