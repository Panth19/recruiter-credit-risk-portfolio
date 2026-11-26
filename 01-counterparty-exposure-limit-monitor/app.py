import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))
from exposure import simulate

st.set_page_config(page_title="Counterparty Risk | Portfolio Lab", page_icon="◈", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--ink:#142b3b;--muted:#637887;--accent:#d71920;--line:#e3e9ed;--wash:#f4f7f8}
.stApp{background:#f7f9fa;color:var(--ink);font-family:'DM Sans',sans-serif}
.block-container{max-width:1380px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:var(--ink)!important;letter-spacing:-.035em}
.hero{background:linear-gradient(115deg,#102b3d 0%,#1d4658 70%,#286577 100%);border-radius:18px;padding:28px 34px;color:white;margin:0 0 22px;border-bottom:4px solid #d71920}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#c7dbe2;margin-bottom:9px}
.hero h1{color:white!important;font-size:31px;margin:0 0 8px;line-height:1.2}.hero p{color:#d7e3e8;margin:0;font-size:14px;max-width:850px}
.section-kicker{color:#d71920;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin:24px 0 5px}
[data-testid="stMetric"]{background:white;border:1px solid var(--line);padding:15px 18px;border-radius:12px;box-shadow:0 2px 8px #16364a0a}
[data-testid="stMetricLabel"]{color:#647987!important;font-size:12px}
[data-testid="stMetricValue"]{color:#142b3b!important;font-family:'Manrope',sans-serif}
[data-testid="stSidebar"]{background:#eef3f5;border-right:1px solid #dfe7eb}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:10px;overflow:hidden}
.note{background:#edf3f5;border-left:3px solid #d71920;border-radius:4px 10px 10px 4px;padding:13px 16px;color:#405a69;font-size:13px;margin:10px 0 18px}
div[data-testid="stPlotlyChart"]{background:white;border:1px solid var(--line);border-radius:12px;padding:8px}
</style>
<div class="hero"><div class="eyebrow">Counterparty risk · Quantitative case study</div><h1>Exposure &amp; limit monitor</h1><p>Simulate forward portfolio exposure through time, compare potential future exposure with counterparty limits, and focus review on the names with the least headroom.</p></div>
""", unsafe_allow_html=True)

trades = pd.read_csv(APP_DIR / "data" / "trades.csv")
limits = pd.read_csv(APP_DIR / "data" / "limits.csv")
with st.sidebar:
    st.markdown("### Model controls")
    st.caption("Change the scenario design and rerun the exposure profile.")
    n_sims = st.select_slider("Monte Carlo paths", options=[1000, 2500, 5000, 10000], value=5000)
    horizon = st.slider("Exposure horizon (months)", 6, 36, 24)
    rate_pct = st.slider("Flat discount rate", 0.0, 10.0, 3.5, 0.5, format="%.1f%%")
    seed = st.number_input("Random seed", 0, 1_000_000, 42)
    st.divider()
    st.caption("Sample trades and limits are illustrative. See methodology below.")

profile, summary, paths = simulate(trades, limits, int(n_sims), int(horizon), float(rate_pct / 100), int(seed))
summary = summary.copy()
summary["headroom_pct"] = summary["headroom_to_PFE95"] / summary["credit_limit"].replace(0, pd.NA)
summary["status"] = summary.breach.map({True: "Review required", False: "Within limit"})
breaches = int(summary.breach.sum())
total_limit = summary.credit_limit.sum()
total_pfe = summary.peak_PFE95.sum()
st.markdown('<div class="section-kicker">Portfolio overview</div>', unsafe_allow_html=True)
a, b, c, d = st.columns(4)
a.metric("Counterparties", f"{len(summary):,}")
b.metric("PFE95 limit breaches", f"{breaches}", delta="Review required" if breaches else "No breaches in this run", delta_color="inverse" if breaches else "normal")
c.metric("Peak PFE95 / total limits", f"{total_pfe / total_limit:.0%}" if total_limit else "n/a")
d.metric("Monte Carlo paths", f"{int(n_sims):,}", help="Number of correlated market scenarios per simulation date.")

left, right = st.columns([1.45, 1], gap="large")
with left:
    st.markdown('<div class="section-kicker">Limit watchlist</div>', unsafe_allow_html=True)
    st.subheader("Who needs attention?")
    view = summary.sort_values("headroom_to_PFE95").copy()
    st.dataframe(view[["counterparty", "credit_limit", "peak_EPE", "peak_PFE95", "peak_PFE99", "headroom_to_PFE95", "status"]], use_container_width=True, hide_index=True, column_config={
        "credit_limit": st.column_config.NumberColumn("Credit limit", format="$%.2f"),
        "peak_EPE": st.column_config.NumberColumn("Peak EPE", format="$%.2f"),
        "peak_PFE95": st.column_config.NumberColumn("Peak PFE 95%", format="$%.2f"),
        "peak_PFE99": st.column_config.NumberColumn("Peak PFE 99%", format="$%.2f"),
        "headroom_to_PFE95": st.column_config.NumberColumn("Headroom to PFE95", format="$%.2f"),
    })
with right:
    st.markdown('<div class="section-kicker">Counterparty profile</div>', unsafe_allow_html=True)
    selected = st.selectbox("Inspect exposure path", summary.counterparty.tolist(), label_visibility="collapsed")
    counterparty_row = summary[summary.counterparty == selected].iloc[0]
    st.caption(f"Limit utilization at peak PFE95: {counterparty_row.peak_PFE95 / counterparty_row.credit_limit:.0%}" if counterparty_row.credit_limit else "No limit configured")
    p = profile[profile.counterparty == selected].set_index("year_fraction")
    st.line_chart(p[["EPE", "PFE95", "PFE99", "credit_limit"]], color=["#1d6577", "#d71920", "#db8933", "#82949e"], height=330)

st.markdown('<div class="note"><b>How to read this:</b> EPE is the mean positive net exposure at each future date. PFE is the 95th or 99th percentile. The breach flag compares peak PFE95 with the counterparty limit over the modeled horizon.</div>', unsafe_allow_html=True)
with st.expander("Trade book and counterparty limits"):
    st.caption("Illustrative inputs provided with the project; edit the CSVs in the repository to change the book.")
    t1, t2 = st.tabs(["Trades", "Limits"])
    with t1: st.dataframe(trades, use_container_width=True, hide_index=True)
    with t2: st.dataframe(limits, use_container_width=True, hide_index=True)
with st.expander("Methodology, assumptions & limitations"):
    st.markdown("""**Model outline.** Correlated geometric Brownian motion simulates market risk factors. Forward trades are revalued at each date, netted by counterparty, and floored at zero before EPE and PFE statistics are calculated.

**Assumptions.** Sample trades, starting prices, volatilities, correlations and limits are synthetic illustrations. The model uses flat annualized volatility, zero price drift and a flat USD discount rate. Counterparty level netting is assumed.

**Not included.** Collateral and margin period of risk, CVA, wrong way risk, stochastic rates, basis risk, default simulation, legal netting validation or production market data. Results are teaching estimates and are not a credit decision or risk system output.""")
st.caption("Portfolio Risk Lab · Model outputs depend on the selected assumptions and path count.")

