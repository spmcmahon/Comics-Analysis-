pythonProject.py

"""


Our goal: 

Based on distributor sales data, identify titles which may be of interest
for rights aquisition and adaptation by film/media companies 


About the data source: 


The monthly sales data for comics on Comichron comes from comic book distributors* who serve comics shops in North America.
https://www.comichron.com/monthlycomicssales.html

From February 2003 to April 2020 ** 

* majority of reporting is from Diamond Comics Distributors who publishes distribution info on the top 300 comics 

** April 2020 - October 2021 reporting changed again 
** Prior to February 2003 distributors only reported pre-orders, not final sales numbers, so the data is not quite comparable 


Fields:	units (sales rank for number of units ordered), 
		dollars (rank for dollar amount sold), 
		Title 
		Issue
		Publisher
		Price
		Estimated units 
		Year

Some more recent data includes an 'On sale' column indicating when the title was first released 


WHAT IT DOES NOT TELL US: 

this only addresses physical book sales to shops, 
	It does not track how many were ultimately sold, where, or how quickly.  
	It does not track after market reselling (i.e. ebay or other collector sites)
	It does not incorporate online sales.
	It does not take into account sales of associated merchandising or media.
	It also does not have any information regarding reception (critical or audience). 

	We are not able to track anything according the a specific character or timeline/continuity.
	Does not contain publishing information such as release date, author, artists, etc. 
	 - cross reference GCD for this information 


From this data we can hopefully get a general feel for which titles were successful based on demand, 
and track the demand across the lifetime of a series.  


Data collection: 


Data exists on site as tabular data (spreadsheets) - 
copy and export to csv file which can be interpreted by python/pandas


"""


# import libraries 

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# loading csv files for idividual comic book sales 2009 - 2019

C09 = pd.read_csv('comics_2009.csv')
C10 = pd.read_csv('comics_2010.csv')
C11 = pd.read_csv('comics_2011.csv')
C12 = pd.read_csv('comics_2012.csv')
C13 = pd.read_csv('comics_2013.csv')
C14 = pd.read_csv('comics_2014.csv')
C15 = pd.read_csv('comics_2015.csv')
C16 = pd.read_csv('comics_2016.csv')
C17 = pd.read_csv('comics_2017.csv')
C18 = pd.read_csv('comics_2018.csv')
C19 = pd.read_csv('comics_2019.csv')


# loading csv files for graphic novel sales 2009 - 2019

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

# adustments for years 2018 and 2019: remove 'On sale' column from comics 

C18 = C18.drop(columns=['On sale'])
C19 = C19.drop(columns=['On sale'])

# concatinate all years into single dataframe


all_comics = [C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19]
all_graphics = [G09, G10, G11, G12, G13, G14, G15, G16, G17, G18, G19]


for df in all_comics: 
	df.columns = ['unit_rank', 'dollar_rank', 'comic_book_title', 'issue', 'price', 'publisher', 'est_units', 'year']
for df in all_graphics: 
	df.columns = ['unit_rank', 'dollar_rank', 'trade_paperback_title', 'price', 'publisher', 'est_units', 'year']


comics = pd.concat(all_comics).reset_index(drop=True)

graphics = pd.concat(all_graphics).reset_index(drop=True)


# cleaning up a bit, need to convert some datatypes: 

comics['est_units'] = comics['est_units'].str.replace(',', '').astype(int)
graphics['est_units'] = graphics['est_units'].str.replace(',', '').astype(int)


comics['price'] = comics['price'].str.replace('$', '').astype(float)
graphics['price'] = graphics['price'].str.replace('$', '').astype(float)



# create estimated gross columns: 

comics['est_gross'] = comics['price'] * comics['est_units']
graphics['est_gross'] = graphics['price'] * graphics['est_units']


# looking at market share percentages

msc_all = comics.groupby('publisher')[['comic_book_title']].count()/10500
msg_all = graphics.groupby('publisher')[['trade_paperback_title']].count()/10500

msc_all = msc_all.reset_index().rename(columns={'comic_book_title':'market_share'})
msg_all = msg_all.reset_index().rename(columns={'trade_paperback_title': 'market_share'})

big_pubs = ['Marvel', 'DC']

indie_comics = comics[~comics.publisher.isin(big_pubs)]
indie_graphics = graphics[~graphics.publisher.isin(big_pubs)]

msc_indy = indie_comics.groupby('publisher')[['comic_book_title']].count()/622
msg_indy = indie_graphics.groupby('publisher')[['trade_paperback_title']].count()/3896

msc_indy = msc_indy.reset_index().rename(columns={'comic_book_title':'market_share'})
msg_indy = msg_indy.reset_index().rename(columns={'trade_paperback_title': 'market_share'})

mean_msci = msc_indy.sort_values('comic_book_title').agg(np.mean)
med_msci = msc_indy.sort_values('comic_book_title').agg(np.median)


# the indy graphics table has a lot of noise, let's filter out some outliers

mean_msgi = msg_indy.sort_values('market_share').agg(np.mean)['market_share']
med_msgi = msg_indy.sort_values('market_share').agg(np.median)['market_share']
std_msgi = msg_indy.sort_values('market_share').agg(np.std)['market_share']


msg_indy_r = msg_indy[msg_indy.market_share > mean_msgi]


# create pie plots for market shares all and indy 

# reformat msc_all and msg_all to Marvel, DC, Other

msc_3 = msc_all.
msg_3 = 



pie_msca = msc_3.plot.pie(y='market_share', ylabel = 'publisher')

pie_msga = msg_3.plot.pie(y='market_share', ylabel = 'publisher')

pie_msci = msc_indy.plot.pie(y='market_share')

pie_msgi = msg_indy_r.plot.pie(y='market_share')