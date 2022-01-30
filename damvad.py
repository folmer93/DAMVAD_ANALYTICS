# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import os
import gc
import matplotlib.pyplot as plt
gc.collect()


#%% Import Data

os.chdir('C:/Users/pfolm/OneDrive/Skrivebord/damvad')
df = pd.read_csv('full202052.dat', header=(0)) #, sep='\s\s+', engine='python')

# Removing all totals for period "TO"
df = df[df['PRODUCT_SECTION'] != 'TO'].copy()

df1 = df[:100000].copy()

#%% Plot 1 - Trade reports for Denmark in Euro per trading partner

# Filter trade reports declared by Denmark
dk = df[df['DECLARANT_ISO'] == 'DK'].copy()
# All trades are reported by both the declarant (assumed to be the exporter) 
# and the trading partner (assumed to be the importer)

# Therefore if filtering all reports where DK is the partner as below, we will see an identical dataset
# dk = df[df['PARTNER_ISO'] == 'DK'].copy()

# Removing all/any blanks from the two variables needed
dk = dk.dropna(subset=['PARTNER_ISO','VALUE_IN_EUROS'])

# Group by reports by product section and summarize the trade value 
dk_top = dk.groupby(['PARTNER_ISO'])['VALUE_IN_EUROS'].sum().reset_index().sort_values(by=['VALUE_IN_EUROS'], ascending=False).reset_index(drop=True)
dk_top['pct'] = (dk_top['VALUE_IN_EUROS'] / dk_top['VALUE_IN_EUROS'].sum()) * 100

# Get top 15
dk_top15 = dk_top[:15].copy()



#%% Plot 1: TOP 15 TRADE PARTNERS OF DENMARK


fig, ax = plt.subplots()
explode = [0.05] * len(dk_top15)
explode[7:15] = [0.4]*8
ax.pie(dk_top15['VALUE_IN_EUROS'], labels=dk_top15['PARTNER_ISO'],explode=explode,autopct='%1.1f%%', labeldistance=1.1, shadow=True)
ax.set_title('   '+'TOP 15 TRADE PARTNERS OF DENMARK\n(% of total volume in euro)',fontsize=12)
plt.tight_layout()


#%% Plot 2: Bar chart

# Top traded product sections measured in real volume (kg)
prod_volume = df.groupby(['PRODUCT_SECTION'])['QUANTITY_IN_KG'].sum().reset_index().sort_values(by=['QUANTITY_IN_KG'], ascending=False).reset_index(drop=True)
# Getting all trades for productsection 05
p5 = df[df['PRODUCT_SECTION'] == '05'].copy()
# Removing all/any blanks
p5 = p5.dropna(subset=['DECLARANT_ISO','VALUE_IN_EUROS'])
# Top declarants of productsection 05
p5_top = p5.groupby(['DECLARANT_ISO'])[['QUANTITY_IN_KG','VALUE_IN_EUROS']].sum().reset_index().sort_values(by=['QUANTITY_IN_KG'], ascending=False).reset_index(drop=True)
# Let's convert Kg into thousands of tonnes and Euros into millions to get some more chart frindly figures
p5_top['QUANTITY_1000T'] = p5_top['QUANTITY_IN_KG']/1000000
p5_top['BILLION_EUROS'] = p5_top['VALUE_IN_EUROS']/1000000000

# Get top 10
p5_top = p5_top[:10]



#%%


labels = p5_top['DECLARANT_ISO']
x = np.arange(len(labels))
ax1 = plt.subplot()
w = 0.35
ax1.set_title('Top declarants of product-section 5 in tonnes(000)')
#plt.xticks(), will label the bars on x axis with the respective country names.
plt.xticks(x + w /2, p5_top['DECLARANT_ISO'], rotation='vertical')
tons =ax1.bar(x, p5_top['QUANTITY_1000T'], width=w, color='b', align='center')
# Create second axis
ax2 = ax1.twinx()
euro =ax2.bar(x + w, p5_top['BILLION_EUROS'], width=w,color='g',align='center')

#Set the Y axis label as GDP.
ax1.set_ylabel('Thousand Tons')
ax2.set_ylabel('Billions of Euro')

#To set the legend on the plot we have used plt.legend()
plt.legend([tons, euro],['Thousand Tons', 'Billions of Euro'])
#To show the plot finally we have used plt.show().
plt.show()


