# -*- coding: utf-8 -*-


###############################################################################
##### PACKAGES
###############################################################################


import pandas as pd
import numpy as np
import os
import gc
import matplotlib.pyplot as plt
gc.collect()



###############################################################################
##### Importing Data
###############################################################################


os.chdir('C:/Users/pfolm/OneDrive/Skrivebord/damvad')
df = pd.read_csv('full202052.dat', header=(0)) #, sep='\s\s+', engine='python')

# Removing all included totals for period "TO"
df = df[df['PRODUCT_SECTION'] != 'TO'].copy()


###############################################################################
##### PLOT 1: TOP TRADING PARTNERS FOR DENMARK MEASURED IN EUROS
###############################################################################


# Filter trade reports declared by Denmark
dk = df[df['DECLARANT_ISO'] == 'DK'].copy()

# Removing all/any blanks from the needed variables
dk = dk.dropna(subset=['PARTNER_ISO','VALUE_IN_EUROS'])

# Group by reports by product_section and summarize the trade value 
dk_top = dk.groupby(['PARTNER_ISO'])['VALUE_IN_EUROS'].sum().reset_index().sort_values(by=['VALUE_IN_EUROS'], ascending=False).reset_index(drop=True)
dk_top['pct'] = (dk_top['VALUE_IN_EUROS'] / dk_top['VALUE_IN_EUROS'].sum()) * 100

# Get top 15
dk_top15 = dk_top[:15].copy()



###############################################################################
##### Pie Plot: TOP 15 TRADE PARTNERS OF DENMARK
###############################################################################


fig, ax = plt.subplots()
explode = [0.05] * len(dk_top15)
explode[7:15] = [0.4]*8
ax.pie(dk_top15['VALUE_IN_EUROS'], labels=dk_top15['PARTNER_ISO'],explode=explode,autopct='%1.1f%%', labeldistance=1.1, shadow=True)
ax.set_title('   '+'TOP 15 TRADE PARTNERS OF DENMARK\n(% of total volume in euro)',fontsize=12)
plt.tight_layout()


##########
# Findings
# Not surprisingly we find that Germany is Denmarks biggest trade partner, along with other neighboring countries 
##########


###############################################################################
##### PLOT 2: TOP TRADERS OF PRODUCT-SECTION 5
###############################################################################

# If we rank all the product_sections for the period, by their summarized trade-volume in kg, we find that product_section 5 tops the list
# Its likely that Product_section 5 represents a selection of commodities
# Lets see who trades this product_section the most


# Top traded product sections measured in real volume (kg)
prod_volume = df.groupby(['PRODUCT_SECTION'])['QUANTITY_IN_KG'].sum().reset_index().sort_values(by=['QUANTITY_IN_KG'], ascending=False).reset_index(drop=True)

# Getting all trades for productsection 05
p5 = df[df['PRODUCT_SECTION'] == '05'].copy()

# Removing all/any blanks
p5 = p5.dropna(subset=['DECLARANT_ISO', 'QUANTITY_IN_KG','VALUE_IN_EUROS'])

# Top declarants of productsection 05
p5_top = p5.groupby(['DECLARANT_ISO'])[['QUANTITY_IN_KG','VALUE_IN_EUROS']].sum().reset_index().sort_values(by=['QUANTITY_IN_KG'], ascending=False).reset_index(drop=True)

# Let's convert Kg into thousands of tonnes and Euros into millions to get some more chart frindly figures
p5_top['QUANTITY_1000T'] = p5_top['QUANTITY_IN_KG']/1000000
p5_top['BILLION_EUROS'] = p5_top['VALUE_IN_EUROS']/1000000000

# Get top 10
p5_top = p5_top[:10]


###############################################################################
##### Double axis barchart (Volume and value) of the Top traders of product-section 5 
###############################################################################


labels = p5_top['DECLARANT_ISO']
x = np.arange(len(labels))
ax1 = plt.subplot()
w = 0.35
ax1.set_title('Top declarants of product-section 5 in tonnes(000)')
#plt.xticks(), will label the bars on x axis with the respective country ISO's
plt.xticks(x + w /2, p5_top['DECLARANT_ISO'], rotation='vertical')
tons =ax1.bar(x, p5_top['QUANTITY_1000T'], width=w, color='b', align='center')
# Create second axis
ax2 = ax1.twinx()
euro =ax2.bar(x + w, p5_top['BILLION_EUROS'], width=w,color='g',align='center')

#Set the Y axis label for value in euro
ax1.set_ylabel('Thousand Tons')
ax2.set_ylabel('Billions of Euro')

#To set the legend on the plot we have used plt.legend()
plt.legend([tons, euro],['Thousand Tons', 'Billions of Euro'])
#To show the plot finally we have used plt.show().
plt.show()

##########
# Findings
# We see that the netherlands declares most trades in terms of both volume and value of product_section 5
# Could product_section_5 perhaps represent gas and oil products (Shell)?
# My findings are that the Netherlands and Germany are the top traders for this product_section in terms of physical volume. 
# In this regard it can furtmore be observed that the Netherlands recieves a higher price per kilo than Germany, recieving on average 12.2% more per kilogram.
##########

