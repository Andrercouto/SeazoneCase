'''This code's purpose is to model "Price_AV_Itapema.csv".'''

# Libraries needed
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import datetime
import zipfile_deflate64 as zipfile

# Loading Price_AV_Itapema.csv dataset
tag_hist_path = r"raw_data\Price_AV_Itapema.zip"
parentZip = zipfile.ZipFile(tag_hist_path, mode="r", compression=zipfile.ZIP_DEFLATED64)
df_prices =  pd.read_csv(parentZip.open('Price_AV_Itapema.csv', mode="r"))

# Checking the loaded DataFrame's size
print(f'The size of the loaded DataFrame is {sys.getsizeof(df_prices)/10**9}GB.')

# Checking the loaded DataFrame's shape
print(f'The loaded DataFrame has {df_prices.shape[0]} lines and {df_prices.shape[1]} columns.')

# Inspecting Data
df_prices.info()

'''The Dataframe is really large and, as it was already seen, there's only 2300 
 locations on it. All the registers concerning the same location and date will be dropped.'''
 
# Dropping duplicates
df_prices = df_prices.loc[df_prices[['date', 'airbnb_listing_id']].drop_duplicates().index]

# Checking the transformed DataFrame's size
print(f'The size of the transformed DataFrame is {sys.getsizeof(df_prices)/10**9}GB.')

'''The size is considerably smaller after removing the duplicates.
 The id column type is int64 and changing it to str is a good practice.'''

# Changing 'airbnb_listing_id' type
df_prices['airbnb_listing_id'] = df_prices['airbnb_listing_id'].astype(str)

# Checking NaN values on columns
df_prices.isna().sum()

'''Some columns are composed strictly by NaN value. They'll be dropped, such as 
 other columns that won't be used.'''
 
# Dropping columns
df_prices = df_prices.drop(['av_for_checkout', 'index', 'bookable', 'ano', 'mes', 'dia'],
                      axis=1)

'''A few registers has NaN values on "price" - which is the most critical column 
 of the Dataset - and they need to be dropped.'''
 
# Dropping registers
df_prices = df_prices.dropna(subset=['price'])

'''The "price" column type is float64, if there's no float values on the column
 its type could be turned into int64.'''

# Inspecting 'price' column
if (df_prices['price']%1).value_counts(dropna=False).loc[0] == len(df_prices):
    print('No float values on the "price" column.')
else:
    print('Float values found on the "price" column.')

# Changing column type    
df_prices['price'] = df_prices['price'].astype(int)

'''The columns 'av_for_checkin' and 'available' are both related to the availability
 of the place, so they must be similar. If it's the case the column can be dropped.'''
 
print(f"{(df_prices['av_for_checkin'] == df_prices['available']).sum()/len(df_prices)}% similarity.")

# Dropping column
df_prices = df_prices.drop(['av_for_checkin'], axis=1)

'''The columns "price" and "price_string" must also be very similar.'''

# Inspecting the price columns
df_prices[['price', 'price_string']].head(20)

# Inspecting the non-numeric values on 'price_string'
(df_prices['price_string'].str.slice(stop=2)).value_counts(dropna=False)

'''All registers has "R$" before the numeric part of the string. Registers with
"price_string" different from "price" must be excluded, for a matter of reliability'''

# Removing R$
df_prices['price_string'] = df_prices['price_string'].str.replace('[R$]', '').astype(int)

# Removing registers
df_prices = df_prices.loc[df_prices['price_string']==df_prices['price']]

# Dropping column
df_prices = df_prices.drop(['price_string'], axis=1)

# Checking the threatened DataFrame
df_prices.info()

# Investigating the 'price' column
df_prices['price'].describe()

'''A large price variation could be seen by the column's standard deviation.
 If the 'price' is related to 'minimum_stay' this difference is be expected (the 
 price - of the same place - would grow according to the number of staying days).'''
 
# Checking the correlation
df_prices['price'].corr(df_prices['minimum_stay'])

'''There's no relation, the outliers should be treated or droped from the Dataframe.
 The interquartile distance technique will be used to investigate them.''' 

# Applying the interquartile distance
quart_1 = np.percentile(df_prices['price'],25)
quart_3 = np.percentile(df_prices['price'],75)
interquartile_distance = quart_3 - quart_1
max_limit = np.percentile(df_prices['price'],75) + 1.5 * interquartile_distance
min_limit = np.percentile(df_prices['price'],25) - 1.5 * interquartile_distance
print(f'Max limit: {max_limit}, every price above this value is considered an outlier.')
print(f'Min limit: {min_limit}, every price bellow this value is considered an outlier.')
print(f"{len(df_prices.loc[df_prices['price']>max_limit])/len(df_prices)}% are outliers.")

'''The interquartile distance technique is one of the most used ways to find outliers.
 Sometimes outliers are a real problem for the datasets and need to be removed, 
 but maybe it's possible to find another solution that would lose a smaller number of
 registers investigating these values.''' 
 
# Plotting the distribution
plt.scatter(df_prices['price'].value_counts().index, df_prices['price'].value_counts(), s=.5)

'''It's noticed that are just a few values above 10000, could be useful compare
 these values to other registers from the same place. '''
 
# List of price outliers registers
outliers_index = df_prices[['price', 'airbnb_listing_id']].loc[df_prices['price']>10000].index

# List of all the locations which has price outliers
ids = df_prices['airbnb_listing_id'].loc[outliers_index].unique()

'''A DataFrame containing the maximum price of the place and the mode (the value
 in a set of the place's prices that appears the most often) will be created in order
 to investigate these registers.''' 
 
# Creating DataFrame 
outliers_df = df_prices.loc[df_prices['airbnb_listing_id'].isin(ids)].groupby('airbnb_listing_id')['price'].agg('max').to_frame()
outliers_df = outliers_df.rename(columns={'price': 'max_price'})
outliers_df['mode'] = df_prices.loc[df_prices['airbnb_listing_id'].isin(ids)].groupby('airbnb_listing_id')['price'].agg(pd.Series.mode)
outliers_df.head(20)
 
''' Cheking the Dataframe, it can be seen that the outliers occurs, most likely,
 because these values ​​were an attempt of defining a price interval. The number 450430 
 for example would probably indicate that the price is between 430 and 450.
 So, to treat this values, a mean between them (in the example case, between 430 and 450)
 will be set in the price column.'''
 
# Function for setting the right values on "price" column
def price_mean(value):
    price_1 = int(str(value)[:3])
    price_2 = int(str(value)[3:])
    correct_price = (price_1 + price_2)/2
    return correct_price

# Applying the function
df_prices['price'].loc[df_prices['price']>9999] = df_prices['price'].loc[df_prices['price']>9999].apply(lambda x: price_mean(x))

# Plotting the new distribution, which seems more accurate now
plt.scatter(df_prices['price'].value_counts().index, df_prices['price'].value_counts(), s=.1)

''' Once the dataset and it's columns are adjusted, the last part of the script
 consists in consolidate the informations on a new dataset (and save it) using the
 'airbnb_listing_id' as the index and containing some relevant paramethers.
 The parameters will be: average price, availability rate (% of availability),
 total revenue and the number of different listing dates'''
 
# Creating the Modeled DataFrame
condensed_prices = pd.DataFrame(index = list(df_prices.airbnb_listing_id.unique()))

# Adding Average Price column
condensed_prices['avg_price'] = df_prices.groupby('airbnb_listing_id')['price'].agg('mean')

# Adding Average Price column
condensed_prices['availability_rate'] = (df_prices['airbnb_listing_id'].loc[df_prices['available']==True].value_counts()/df_prices['airbnb_listing_id'].value_counts()).fillna(0)

# Adding Total Revenue column
condensed_prices['total_revenue'] = df_prices[['price', 'airbnb_listing_id']].loc[df_prices['available']==False].groupby('airbnb_listing_id')['price'].sum()

# Adding Number of different dates column
condensed_prices['n_of_diff_dates'] = df_prices['date'].value_counts()
 
# Saving the modeled file on 'modeled_data' folder
condensed_prices.to_csv(r'modeled_data\Modeled_Prices_AV_Itapema.csv')
 
 
 
 
