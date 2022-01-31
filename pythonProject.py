pythonProject.py



# import libraries 

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# creating database for graphic novel sales 2009 - 2019

G09 = pd.read_csv('graphics_2009.csv')
G10 = pd.read_csv('graphics_2010.csv')
G11 = pd.read_csv('graphics_2011.csv')
G12 = pd.read_csv('graphics_2012.csv')
G13 = pd.read_csv('graphics_2013.csv')
G14 = pd.read_csv('graphics_2014.csv')
G15 = pd.read_csv('graphics_2015.csv')
G16 = pd.read_csv('graphics_2016.csv')
G17 = pd.read_csv('graphics_2017.csv')
G18 = pd.read_csv('graphics_2018.csv')
G19 = pd.read_csv('graphics_2019.csv')


all_graphics = [G09, G10, G11, G12, G13, G14, G15, G16, G17, G18, G19]


for df in all_graphics: 
	df.columns = ['unit_rank', 'dollar_rank', 'trade_paperback_title', 'price', 'publisher', 'est_units', 'year']

graphics = pd.concat(all_graphics).reset_index(drop=True)


# cleaning up a bit, need to convert some datatypes: 
graphics['est_units'] = graphics['est_units'].str.replace(',', '').astype(int)
graphics['price'] = graphics['price'].str.replace('$', '').astype(float)


graphics['est_gross'] = graphics['price'] * graphics['est_units']


# Data Manipulation and EDA:


# looking at market share percentages by volume

msg_all = graphics.groupby('publisher')[['trade_paperback_title']].count()/10500
msg_all = msg_all.reset_index().rename(columns={'trade_paperback_title': 'market_share'})


# looking at market share by est_gross 

for df in all_graphics: 
	df.est_units = df.est_units.str.replace(',', '').astype(int)
	df.price = df.price.str.replace('$', '').astype(float)
	df['est_gross'] = df.price * df.est_units



msg_09 = G09.groupby('publisher')[['est_gross']].sum() / sum(G09.est_gross) * 100
msg_10 = G10.groupby('publisher')[['est_gross']].sum() / sum(G10.est_gross) * 100
msg_11 = G11.groupby('publisher')[['est_gross']].sum() / sum(G11.est_gross) * 100
msg_12 = G12.groupby('publisher')[['est_gross']].sum() / sum(G12.est_gross) * 100
msg_13 = G13.groupby('publisher')[['est_gross']].sum() / sum(G13.est_gross) * 100
msg_14 = G14.groupby('publisher')[['est_gross']].sum() / sum(G14.est_gross) * 100
msg_15 = G15.groupby('publisher')[['est_gross']].sum() / sum(G15.est_gross) * 100
msg_16 = G16.groupby('publisher')[['est_gross']].sum() / sum(G16.est_gross) * 100
msg_17 = G17.groupby('publisher')[['est_gross']].sum() / sum(G17.est_gross) * 100
msg_18 = G18.groupby('publisher')[['est_gross']].sum() / sum(G18.est_gross) * 100
msg_19 = G19.groupby('publisher')[['est_gross']].sum() / sum(G19.est_gross) * 100


msg_years = [msg_09, msg_10, msg_11, msg_12, msg_13, msg_14, msg_15, msg_16, msg_17, msg_18, msg_19]

for df in msg_years: 
	df = df.reset_index().rename(columns = {'est_gross':'market_share'})
	

big_pubs = ['Marvel', 'DC']

indie_graphics = top_graphics[~top_graphics.publisher.isin(big_pubs)]




# who are the top sellers: 

top_sellers = graphics.groupby('publisher')[['est_gross']].sum().reset_index().sort_values('est_gross', ascending=False)

top_pubs = list(top_sellers.iloc[:14,0])

top_pubs.remove('Archie')	# owned by Warner Bros
top_pubs.remove('Top Shelf') # now owned by IDW


#filter initial table to only include top pubs:

top_graphics = graphics[graphics.publisher.isin(top_pubs)]



# create pivot table for market share values by year and publisher

market_shares = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'est_gross', aggfunc= sum)
market_shares = market_shares.fillna(0)




# average overall market shares all and indy 

overall_totms = ms_all.apply('mean', axis = 0)

overall_totms_df = pd.DataFrame(overall_totms).reset_index().rename(columns = {0:'market_share'})
overall_totms_df = overall_totms_df.sort_values('market_share', ascending=False)

# extracted for pie chart (see below)

allms_pubs = ['DC', 'Marvel', 'Image', 'Dark Horse', 'Other']
allms_pcts = [36, 32, 17, 6, 9]
explode = (0,0,0,0,0.1)


# possible subsection / zoom in 
indy = market_shares.drop(columns = ['Marvel', 'DC'])
ms_indy = indy.apply(lambda x: 100*x/x.sum(), axis = 1)
overall_indyms = ms_indy.apply('mean', axis = 0)

overall_indyms_df = pd.DataFrame(overall_indyms).reset_index().rename(columns = {0:'market_share'})
overall_indyms_df = overall_indyms_df.sort_values('market_share', ascending=False)


# market shares by year trend: all and indy (zoomed in)

ms_all = market_shares.apply(lambda x: 100*x/x.sum(), axis = 1)

ms_indy = ms_all.drop(columns = ['Marvel', 'DC'])



# number of titles by publisher 

tot_titles = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'trade_paperback_title', aggfunc='count')
tot_titles = tot_titles.fillna(0)



# avg gross of individual titles by publisher

avg_gross = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'est_gross', aggfunc = 'mean')
avg_gross = avg_gross.fillna(0)







# PLOTS

from matplotlib.colors import ListedColormap
cmap = ListedColormap(sns.color_palette())

# pie chart of market share 

# all 
fig1, ax1 = plt.subplots()
ax1.pie(allms_pcts, explode=explode, labels=allms_pubs, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

ax1.set_title('Market Share')



# market shares by year (all and indy subsection)

plot_ms = sns.lineplot(data = ms_all)  # ms1

plot_ms_indy = sns.lineplot(data = ms_indy.drop(columns = ['Image', 'Dark Horse']))  #ms2


# annual number of titles by publisher by year

plot_tot_all = sns.lineplot(data=tot_titles)


 # avg est gross of titles by publisher by year 

plot_avgross = sns.lineplot(data=avg_gross)


# bar plot of avg gross per title 


means_df = pd.DataFrame(top_graphics.groupby('publisher')['est_gross'].mean()).sort_values('est_gross', ascending=False)
stds_df = pd.DataFrame(top_graphics.groupby('publisher')['est_gross'].std()).sort_values('est_gross', ascending=False)

means_df = means_df.rename(columns = {'est_gross' : 'mn_gross'}).reset_index()
mean_bar = means_df.plot(x='publisher', y='mn_gross', kind='bar', xlabel='Publisher', ylabel='Average Gross Per Title (in Dollars)')
mean_bar.set_xticklabels(mean_bar.get_xticklabels(), rotation = 30)


# violin plot 

violin = sns.violinplot(data = top_graphics, x='publisher', y='est_gross')
violin.set_xticklabels(violin.get_xticklabels(),rotation = 30)
violin.set_ylabel('Gross Per Title (in Dollars)')
violin.set_xlabel('Publisher')


