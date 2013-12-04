# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 13:17:34 2013

A reproduction of Hidalgo & Hausmann (2009): The building blocks of
economic complexity

@author: Rob
"""

#%%
import config
import pandas as pd

__RCA_cutoff__ = 1
__iterations__ = 10

#%%
data = pd.read_csv(config.csv_file,dtype={'commodity_code':'object'})
#data = data[data.from_iso3.isin(['USA','FRA','ABW','DEU','GBR','IND']) & 
#            data.commodity_code.isin(['0406','1005','2711','8407','9002'])]

#%%
# Calculate Revealed Comparative Advantage (p10571)

# Total world trade by commodity_code:
wt = data.groupby(['trade_year', 
                   'commodity_code'])['trade_value'].aggregate(sum)

# Share of world trade:
swt = wt.astype('float64').div(wt.sum())

# Country export basket sizes:
data['eb'] = data.groupby(['trade_year', 
                   'from_iso3'])['trade_value'].transform(sum)
      
# Share of export basket:            
data['seb'] = data['trade_value'].astype('float32') / data['eb']

# Revealed comparative advantage 
# (share of export basket / share of world trade):
data = data.set_index(['trade_year','commodity_code'])
data['swt'] = swt
data = data.reset_index()
data['rca'] = data.seb / data.swt

# M_cp
rca = data.set_index(['trade_year','from_iso3',
                      'commodity_code'])['rca'].sum(level=[0,1,2])
mcp = (rca.unstack(2) > __RCA_cutoff__) * 1.0

#%%
kc = [mcp.sum(1)]
kp = [mcp.sum(0)]

for i in range(1,__iterations__):
    kc.append((mcp * kp[i - 1]).sum(1)/kc[0])
    kp.append((mcp.mul(kc[i - 1],0)).sum(0)/kp[0])

#%%
#kc = pd.DataFrame(kc).transpose()
#kp = pd.DataFrame(kp).transpose()