import json,glob,os
import pandas as pd
TAGS={
'assets':['Assets'], 'current_assets':['AssetsCurrent'], 'current_liabilities':['LiabilitiesCurrent'],
'total_liabilities':['Liabilities'], 'equity':['StockholdersEquity'], 'retained_earnings':['RetainedEarningsAccumulatedDeficit'],
'ebit':['OperatingIncomeLoss'], 'revenue':['RevenueFromContractWithCustomerExcludingAssessedTax','Revenues','SalesRevenueNet'],
'net_income':['NetIncomeLoss'], 'receivables':['AccountsReceivableNetCurrent'], 'cash':['CashAndCashEquivalentsAtCarryingValue']}
def build(data_dir='data'):
 rows=[]
 for path in glob.glob(os.path.join(data_dir,'*.json')):
  co=json.load(open(path,encoding='utf8')); facts=co['facts'].get('us-gaap',{}); annual={}
  for metric,tags in TAGS.items():
   for tag in tags:
    if tag not in facts: continue
    units=facts[tag]['units']; unit='USD' if 'USD' in units else next(iter(units),None)
    if not unit: continue
    candidates=[z for z in units[unit] if z.get('form')=='10-K' and z.get('fy') and 2018<=int(z['fy'])<=2025 and (not z.get('fp') or z.get('fp')=='FY')]
    byyear={}
    for z in candidates:
     yr=int(z['fy']); end=z.get('end','')
     if metric not in ('assets','current_assets','current_liabilities','total_liabilities','equity','retained_earnings','receivables','cash') and z.get('start'):
      days=(pd.Timestamp(end)-pd.Timestamp(z['start'])).days
      if not 330<=days<=400: continue
     if yr not in byyear or z.get('filed','')>byyear[yr].get('filed',''): byyear[yr]=z
    if byyear:
     annual[metric]={yr:z['val'] for yr,z in byyear.items()}; break
  for year in sorted(set().union(*(set(v) for v in annual.values()))):
   r={'company':co['entityName'],'cik':str(co['cik']).zfill(10),'year':year}
   r.update({k:v.get(year) for k,v in annual.items()}); rows.append(r)
 df=pd.DataFrame(rows)
 for c in TAGS: 
  if c not in df: df[c]=float('nan')
 return df
if __name__=='__main__':
 d=build(); d.to_csv('data/annual_fundamentals.csv',index=False); print(f'Wrote {len(d)} company-year rows')
