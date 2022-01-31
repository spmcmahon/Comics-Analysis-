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


#filter initial table to only include top pubs:

top_graphics = graphics[graphics.publisher.isin(top_pubs)]





# create pivot table for market share values by year and publisher

market_shares = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'est_gross', aggfunc= sum)
market_shares = market_shares.fillna(0)




# average overall market shares all and indy 

overall_totms = ms_all.apply('mean', axis = 0)

overall_totms_df = pd.DataFrame(overall_ms).reset_index().rename(columns = {0:'market_share'})



indy = market_shares.drop(columns = ['Marvel', 'DC'])
ms_indy = indy.apply(lambda x: 100*x/x.sum(), axis = 1)
overall_indyms = ms_indy.apply('mean', axis = 0)

overall_indyms_df = pd.DataFrame(overall_indyms).reset_index().rename(columns = {0:'market_share'})





# pie charts of market share (all and indy subsection)

pie_all = overall_totms_df.plot.pie(y='market_share', ylabel = 'publisher')

pie_indy = overall_indyms_df.plot.pie(y='market_share', ylabel = 'publisher')





# market shares by year trend: all and indy (zoomed in)

ms_all = market_shares.apply(lambda x: 100*x/x.sum(), axis = 1)

ms_indy = ms_all.drop(columns = ['Marvel', 'DC'])

plot_ms = sns.lineplot(data = ms_all)
plot_ms_indy = sns.lineplot(data = ms_indy)

# number of titles by publisher 

tot_titles = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'trade_paperback_title', aggfunc='count')
tot_titles = tot_titles.fillna(0)


plot_tot_all = sns.lineplot(data=tot_titles)
plot_tot_indy = sns.lineplot(data=tot_titles.drop(columns = ['Marvel', 'DC']))


# avg gross of individual titles by publisher

avg_gross = pd.pivot_table(data = top_graphics, index = 'year', columns = 'publisher', values = 'est_gross', aggfunc = 'mean')
avg_gross = avg_gross.fillna(0)

plot_avgross = sns.lineplot(data=avg_gross)


# violin or box plots of avg. gross by publisher


violin_gross = sns.violinplot(data = top_graphics, x='publisher', y='est_gross')

# bubble chart of monthly average number of titles in the top 300 for comic books 
 
top_300 = pd.read_csv('top_300.csv')








