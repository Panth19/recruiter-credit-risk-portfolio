import streamlit as st
from pathlib import Path
import sys
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))
from score import score
import pandas as pd
st.set_page_config(page_title='Corporate Counterparty Scoring',layout='wide')
st.title('Corporate Counterparty Scoring')
st.caption('SEC EDGAR reported fundamentals | analytical screening proxy, not a rating or default prediction')
d=score(pd.read_csv(APP_DIR / "data" / "annual_fundamentals.csv")).dropna(subset=['z_double_prime']); years=sorted(d.year.unique()); year=st.selectbox('Fiscal year',years,index=len(years)-1); s=d[d.year==year].sort_values('z_double_prime'); co=st.selectbox('Company',s.company.tolist()); r=s[s.company==co].iloc[0]
a,b,c=st.columns(3); a.metric('Book-equity Z double-prime',f"{r.z_double_prime:.2f}"); b.metric('Screening band',str(r.band)); c.metric('Current ratio',f"{r.current_assets/r.current_liabilities:.2f}" if r.current_liabilities else 'n/a')
st.subheader('Company-year screen'); st.dataframe(s[['company','year','z_double_prime','band','assets','total_liabilities','equity','revenue']],use_container_width=True); st.subheader('Trend'); st.line_chart(d[d.company==co].set_index('year')['z_double_prime'])
st.info('The score uses SEC-reported items and book equity. Zone cutoffs are a coarse screening convention. This is not calibrated to observed defaults, ratings, or recoveries; use analyst review and external credit evidence before decisions.')
