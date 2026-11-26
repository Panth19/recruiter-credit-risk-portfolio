import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))
from score import score

st.set_page_config(page_title="Corporate Credit Screen | Portfolio Lab", page_icon="◈", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
.stApp{background:#f7f9fa;color:#142b3b;font-family:'DM Sans',sans-serif}.block-container{max-width:1380px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:#142b3b!important;letter-spacing:-.035em}
.hero{background:linear-gradient(115deg,#102b3d,#1d4658 72%,#286577);border-radius:18px;padding:28px 34px;color:white;margin-bottom:22px;border-bottom:4px solid #d71920}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#c7dbe2;margin-bottom:9px}.hero h1{color:white!important;font-size:31px;margin:0 0 8px}.hero p{color:#d7e3e8;margin:0;font-size:14px;max-width:900px}
.section-kicker{color:#d71920;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin:24px 0 5px}
[data-testid="stMetric"]{background:white;border:1px solid #e3e9ed;padding:15px 18px;border-radius:12px;box-shadow:0 2px 8px #16364a0a}[data-testid="stMetricLabel"]{color:#647987!important;font-size:12px}[data-testid="stMetricValue"]{color:#142b3b!important;font-family:'Manrope',sans-serif}
[data-testid="stSidebar"]{background:#eef3f5;border-right:1px solid #dfe7eb}[data-testid="stDataFrame"]{border:1px solid #e3e9ed;border-radius:10px;overflow:hidden}
.note{background:#edf3f5;border-left:3px solid #d71920;border-radius:4px 10px 10px 4px;padding:13px 16px;color:#405a69;font-size:13px;margin:10px 0 18px}
</style>
<div class="hero"><div class="eyebrow">Corporate credit · Public filing analysis</div><h1>Counterparty financial screen</h1><p>Explore reported balance sheet and income statement signals for listed companies, with transparent ratio trends and an interpretable Z double-prime screening proxy.</p></div>
""", unsafe_allow_html=True)

d = score(pd.read_csv(APP_DIR / "data" / "annual_fundamentals.csv")).dropna(subset=["z_double_prime"])
with st.sidebar:
    st.markdown("### Screen controls")
    years = sorted(d.year.unique())
    year = st.selectbox("Fiscal year", years, index=len(years) - 1)
    s = d[d.year == year].sort_values("z_double_prime")
    co = st.selectbox("Issuer", s.company.tolist())
    st.divider()
    st.caption("Underlying source: SEC EDGAR company facts. Results are research screens, not ratings.")
r = s[s.company == co].iloc[0]
z = float(r.z_double_prime)
current_ratio = r.current_assets / r.current_liabilities if r.current_liabilities else float("nan")
debt_assets = r.total_liabilities / r.assets if r.assets else float("nan")
st.markdown('<div class="section-kicker">Issuer snapshot</div>', unsafe_allow_html=True)
a,b,c,dcol = st.columns(4)
a.metric("Z double-prime", f"{z:.2f}", help="A formula-based screening proxy; not a rating or a calibrated probability of default.")
b.metric("Screening zone", str(r.band))
c.metric("Current ratio", f"{current_ratio:.2f}" if pd.notna(current_ratio) else "n/a")
dcol.metric("Liabilities / assets", f"{debt_assets:.0%}" if pd.notna(debt_assets) else "n/a")

left, right = st.columns([1.25, 1], gap="large")
with left:
    st.markdown('<div class="section-kicker">Peer context</div>', unsafe_allow_html=True)
    st.subheader(f"Issuer screen · FY {year}")
    st.dataframe(s[["company", "year", "z_double_prime", "band", "assets", "total_liabilities", "equity", "revenue"]], use_container_width=True, hide_index=True, column_config={
        "z_double_prime": st.column_config.NumberColumn("Z″ proxy", format="%.2f"),
        "assets": st.column_config.NumberColumn("Assets (USD)", format="$%.2f"),
        "total_liabilities": st.column_config.NumberColumn("Liabilities (USD)", format="$%.2f"),
        "equity": st.column_config.NumberColumn("Book equity (USD)", format="$%.2f"),
        "revenue": st.column_config.NumberColumn("Revenue (USD)", format="$%.2f"),
    })
with right:
    st.markdown('<div class="section-kicker">Historical signal</div>', unsafe_allow_html=True)
    trend = d[d.company == co].set_index("year")["z_double_prime"]
    st.subheader("Z double-prime trend")
    st.line_chart(trend, color="#d71920", height=300)
    st.caption("Lower values indicate weaker screening signals under the selected proxy convention.")

with st.expander("What drives this screen?"):
    st.markdown("The Z double-prime formula combines working capital, retained earnings, EBIT, book equity relative to liabilities, and revenue, each scaled by assets where specified. This dashboard presents the overall score and the source statement metrics so the output can be challenged rather than treated as a black box.")
st.markdown('<div class="note"><b>Interpretation boundary:</b> SEC filings are real public data, but this ratio screen is not calibrated to observed defaults, agency ratings or recoveries. It omits qualitative credit analysis, guarantees, liquidity access, market signals and counterparty-specific exposure. Use it as an initial research aid only.</div>', unsafe_allow_html=True)
st.caption("Corporate Credit Lab · Filing values and company fiscal years follow source records.")

