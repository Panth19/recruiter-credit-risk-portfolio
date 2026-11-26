import pandas as pd
from build_data import build
def score(df):
 d=df.copy(); d['working_capital']=d.current_assets-d.current_liabilities
 d['z_double_prime']=.717*d.working_capital/d.assets+.847*d.retained_earnings/d.assets+3.107*d.ebit/d.assets+.420*d.equity/d.total_liabilities+.998*d.revenue/d.assets
 d['band']=pd.cut(d.z_double_prime,[-float('inf'),1.23,2.90,float('inf')],labels=['Distress zone','Grey zone','Lower-risk zone'])
 return d
if __name__=='__main__':
 d=score(build()); d.to_csv('data/scored_company_years.csv',index=False); print(f'Wrote {len(d)} company-year rows')
