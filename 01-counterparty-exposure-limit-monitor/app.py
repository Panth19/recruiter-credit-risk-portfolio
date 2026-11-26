import streamlit as st
import pandas as pd
from pathlib import Path
import sys
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))
from exposure import simulate

st.set_page_config(page_title="Counterparty Exposure Monitor", layout="wide")
st.title("Counterparty Exposure and Limit Monitor")
st.caption("Monte Carlo forward exposure simulation | USD | illustrative sample book")
trades = pd.read_csv(APP_DIR / "data" / "trades.csv")
limits = pd.read_csv(APP_DIR / "data" / "limits.csv")
with st.sidebar:
    st.header("Simulation settings")
    n_sims = st.select_slider("Scenarios", options=[1000, 2500, 5000, 10000], value=5000)
    horizon = st.slider("Horizon (months)", 6, 36, 24)
    rate = st.slider("Flat discount rate", 0.0, 0.10, 0.035, 0.005, format="%.1f%%")
    seed = st.number_input("Random seed", 0, 1_000_000, 42)
profile, summary, paths = simulate(trades, limits, int(n_sims), int(horizon), float(rate), int(seed))
breaches = int(summary.breach.sum())
a,b,c = st.columns(3); a.metric("Counterparties", len(summary)); b.metric("PFE limit breaches", breaches); c.metric("Scenarios", f"{int(n_sims):,}")
st.subheader("Counterparty limit summary")
view = summary.copy(); view["status"] = view.breach.map({True:"BREACH",False:"Within limit"})
st.dataframe(view[["counterparty","credit_limit","peak_EPE","peak_PFE95","peak_PFE99","headroom_to_PFE95","status"]],use_container_width=True)
selected = st.selectbox("Exposure profile", summary.counterparty.tolist())
p = profile[profile.counterparty==selected].set_index("year_fraction")
st.subheader(f"{selected}: expected and potential future exposure")
st.line_chart(p[["EPE","PFE95","PFE99","credit_limit"]])
st.caption("Exposure is floored at zero after netting this counterparty�s trades. PFE is the 95th percentile of the simulated positive net exposure at each date. Limit breach flag uses peak PFE95 over the modeled horizon.")
with st.expander("Trade book and limits"):
    st.write("Illustrative positions (editable CSV files in data/)"); st.dataframe(trades,use_container_width=True); st.dataframe(limits,use_container_width=True)
with st.expander("Model assumptions and limitations"):
    st.markdown("""- The sample trades, starting spots, volatilities, correlations, and limits are **synthetic examples**, not market quotes or a real portfolio.
- Correlated geometric Brownian motion with flat annualized volatilities and zero price drift; flat USD discount rate.
- Forward mark is the discounted contractual delivery value; USD notional for EURUSD, price units for commodity contracts.
- Counterparty-level netting is assumed. No collateral, margin period of risk, CVA, wrong-way risk, stochastic rates, basis risk, or default simulation.
- EPE/PFE are Monte Carlo estimates and depend on model inputs and scenario count. Calibrate curves/volatilities, conventions, agreements, and netting sets before operational use.""")

