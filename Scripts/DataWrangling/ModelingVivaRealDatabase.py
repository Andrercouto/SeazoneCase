'''The main purpose of this script is to extract, clean and enrich data from
 VivaReal_Itapema.csv.'''
    

# Libraries needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from sklearn.feature_extraction.text import CountVectorizer
import unidecode

# Loading Price_AV_Itapema.csv dataset
df_vivareal = pd.read_csv(
    r'raw_data\VivaReal_Itapema.csv',
    low_memory=False)


# Checking Columns
df_vivareal.info()

'''There are some columns that will not be used. It is important to establish 
that each register represents a location, represented by listing_id'''


# Separating  columns
to_delete_columns = ['link_name', 'link_url', 'listing_desc', 
            'address_country', 'address_state','address_city', 'unit_subtype',
            'address_street_number','address_complement', 'location_id', 
            'advertiser_id', 'advertiser_name', 'advertiser_phones',
            'advertiser_whatsapp', 'advertiser_url', 'portal', 'ano', 'mes', 'dia']
df_vivareal = df_vivareal.drop(to_delete_columns, 1)


# Checking the number of locations
df_vivareal['listing_id'].value_counts()

'''The dataset contains 13795 locations, but 17547 registers, the .drop_duplicates()
 function excludes any duplicated registers on the dataframe.'''

# Dropping duplicates
df_vivareal = df_vivareal.drop_duplicates()

# Checking the number of locations
df_vivareal['listing_id'].value_counts()

''' The dataframe still has more records than locations, and its cause must be 
investigated. For this, all the duplicated id's will be added to a new Dataframe.'''

# Checking which columns has different values for the same location
id_count = df_vivareal['listing_id'].value_counts()
df_duplicates = df_vivareal.loc[df_vivareal['listing_id'].isin(id_count.loc[id_count>1].index)]
for id in id_count.loc[id_count>1].index:
    check = df_duplicates.loc[df_duplicates['listing_id']==2543566736].reset_index(drop=True).T
    same_value = (check[0].dropna() == check[1].dropna()) # There's no id with more than 2 registers
    print(same_value.loc[same_value==False].index[0])

''' The duplicates occurs only because different values on the 'business_types'
 column for the same locations.'''

# Checking the different values
df_duplicates[['listing_id', 'business_types']].sort_values(by=['listing_id'])

''' The values on the column are just in a different order. These duplicates
 will be excluded.'''

# Dropping duplicated registers
df_vivareal = df_vivareal.loc[df_vivareal['listing_id'].drop_duplicates().index]

# Reordering the DataFrame
df_vivareal = df_vivareal.reset_index(drop=True)


''' Once there's just one line per location on the DataFrame, the columns
 must be checked to see if they need some kind of treatment.'''

# Checking Columns
df_vivareal.info()

# Checking the date column
df_vivareal['aquisition_date'].value_counts()

'''All register have the same date, so this column will be excluded'''

# Droping 'aquisition_date' column
df_vivareal = df_vivareal.drop(['aquisition_date'], 1)

'''The price (both sale and rental) are the most critical variable on the dataset.
 Registers with NaN values on both columns must be excluded. Is also needed to 
 check the rental period and if it's related in some with the rental price.'''

# Excluding registers without 'sale_price' and 'rental_price'
df_vivareal = df_vivareal.loc[(~df_vivareal['sale_price'].isna())|(~df_vivareal['rental_price'].isna())]

# Checking 'rental_periods'
df_vivareal['rental_period'].value_counts()

''' Theres two possible rental periods, daily and monthly and is important to
 know if the rental price concerns the rental period. The correlation coefficient
 between both columns will help checking if they're correlated.'''

# Creating an empty auxiliar column
df_vivareal['aux_rental_period'] = np.nan

# If rental period is monthly = 30, if daily = 1
df_vivareal['aux_rental_period'].loc[df_vivareal['rental_period']=='MONTHLY'] = 30
df_vivareal['aux_rental_period'].loc[df_vivareal['rental_period']=='DAILY'] = 1

# Checking the correlation
df_vivareal['aux_rental_period'].dropna().corr(df_vivareal['rental_price'].dropna())

''' The correlation rate has a high value (0.7), so the price considers the rental
 period. So the 'rental_price' for the registers with a MONTLHY period will be
 divided by 30 to transform them into a daily value.'''
 
# Transforming 'rental_price' register with monthly periods
df_vivareal['rental_price'].loc[df_vivareal['rental_period']=='MONTHLY'] = df_vivareal['rental_price'].loc[df_vivareal['rental_period']=='MONTHLY']/30

# Dropping columns
df_vivareal = df_vivareal.drop(['aux_rental_period', 'business_types', 'rental_period'], 1)

''' Once the price columns are the most critical, checking its the basic statistics
 and plotting histograms could help to its distribution.'''

# Checking price columns
df_vivareal[['sale_price', 'rental_price']].describe()

# Plotting 'sale_price' distribution
plt.hist(df_vivareal['sale_price'].dropna(), bins=40, alpha = 0.5, color= 'b')

# Plotting 'sale_price' distribution
plt.hist(df_vivareal['rental_price'].dropna(), bins=40, alpha = 0.5, color= 'r')

''' While is possible to see on the histograms that most of the rental prices
 are between 1000 and 2000, the sale's price histogram is useless cause of the
 presence of outliers which has a price highly above average. The main techniche
 to find these values is applying the quartile distance, which defines upper 
 and lower limits that will defines the outliers'''
 
# Finding the limits
quart_1 = np.percentile(df_vivareal['sale_price'].dropna(),25)
quart_3 = np.percentile(df_vivareal['sale_price'].dropna(),75)
interquartile_distance = quart_3 - quart_1
max_limit = np.percentile(df_vivareal['sale_price'].dropna(),75) + 1.5 * interquartile_distance
min_limit = np.percentile(df_vivareal['sale_price'].dropna(),25) - 1.5 * interquartile_distance
print(f'Max limit: {max_limit}, every price above this value is considered an outlier.')
print(f'Min limit: {min_limit}, every price bellow this value is considered an outlier.')

''' According to the interquartile distance technique, the maximum limit for outliers is 4mi,
 but it wouldn't be a price that SHOULD be considered outliers in the analysis. 
 So the values above it will be investigated more deeply.'''

# Plotting 'sale_price' outliers distribution
plt.hist(df_vivareal['sale_price'].loc[df_vivareal['sale_price']>max_limit], bins=40, alpha = 0.5, color= 'r')

''' There are clearly some outliers AMONG the prices above the upper limit.
 It's useful to segment and sort the price values into bins.'''
 
# Segmenting the outliers
pd.cut(df_vivareal['sale_price'].loc[df_vivareal['sale_price']>max_limit], 20).value_counts()

# Checkint outliers 90 percentile
np.percentile(df_vivareal['sale_price'].loc[df_vivareal['sale_price']>max_limit], 90)

''' 90% of the outliers has a smaller price than 12 mi, so it will defined as
 the maximum limit and exclude registes with prices above.'''

# Defining the maximum limit
defined_max_limit = np.percentile(df_vivareal['sale_price'].loc[df_vivareal['sale_price']>max_limit], 90)
 
# Excluding outliers
df_vivareal = df_vivareal.loc[(df_vivareal['sale_price']<defined_max_limit)|(df_vivareal['sale_price'].isna())] 
 
# Investigating price columns
df_vivareal[['sale_price', 'rental_price']].describe()

# Plotting 'sale_price' distribution
plt.hist(df_vivareal['sale_price'].dropna(), bins=40, alpha = 0.5, color= 'b')

# Plotting 'sale_price' distribution
plt.hist(df_vivareal['rental_price'].dropna(), bins=40, alpha = 0.5, color= 'r')
 
''' It's possible to get a better understanding of the 'sale_price' data by the
 histogram now. But there's some other columns which needs treatment,'''
 
# Checking NaN values
df_vivareal.isna().sum()

'''There's plenty of NaN values on 'yearly_iptu' and 'monthly_condo_fee',
 so these columns will be excluded.'''
 
# Dropping columns
df_vivareal = df_vivareal.drop(['yearly_iptu', 'monthly_condo_fee'], 1)

# Checking 'property_type'
df_vivareal['property_type'].value_counts()

''' Almost all registers has the 'UNIT' on the 'property_type' columns. The 
 other registers and the column will be dropped from the dataframe.'''

# Dropping registers and the 'property_type' column
df_vivareal = df_vivareal.loc[df_vivareal['property_type']=='UNIT'].drop(['property_type'], 1)

# Checking 'property_type'
df_vivareal['listing_type'].value_counts()

''' All the values from 'listing_type' are the same, so this column will be excluded'''

# Dropping 'listing_type' column
df_vivareal = df_vivareal.drop(['listing_type'], 1)

# Checking NaN values
df_vivareal.isna().sum()

''' Some registers has NaN values on the 'total_area', 'usable_area', 'bathrooms', 
'bedrooms', 'suites' and 'parking_spaces' columns. This registers will be excluded'''

# Dropping NaN values
df_vivareal = df_vivareal.dropna(subset = ['total_area', 'usable_area', 'bathrooms',
                                   'bedrooms', 'suites', 'parking_spaces'])

# Investigating these column
df_vivareal[['total_area', 'usable_area', 'bathrooms',
        'bedrooms', 'suites', 'parking_spaces']].describe()

''' By looking to columns' basic statistics, it's clear that some values are outliers
 which must be dropped. For this, a function will be created'''

# Creation of the function
def outliers_removal(df, column):
    
    '''This function removes the outliers from a dataframe in the choosen
    column'''
    
    q1 = np.percentile(df[column].loc[~df[column].isna()],25)
    q3 = np.percentile(df[column].loc[~df[column].isna()],75)
    iqrd = q3 - q1
    lower, upper = (q1 - (1.5 * iqrd), q3 + (1.5 * iqrd))
    print(f'Any register with values above {upper} and bellow {lower} on the "{column}" column will be dropped.')
    new_df = df.loc[(df[column]<upper)&(df[column]>lower)]
    print(f'{len(df) - len(new_df)} registers were dropped for having outliers on the "{column}" column.\n')
    
    return new_df

# Applying the function
df_vivareal = outliers_removal(df_vivareal, 'total_area')
df_vivareal = outliers_removal(df_vivareal, 'usable_area')
df_vivareal = outliers_removal(df_vivareal, 'bathrooms')
df_vivareal = outliers_removal(df_vivareal, 'bedrooms')
df_vivareal = outliers_removal(df_vivareal, 'suites')
df_vivareal = outliers_removal(df_vivareal, 'parking_spaces')

# Checking the DataFrame
df_vivareal.info()

''' On this part of the script, all the numeric/quantitative variables are
 already treated, but there are some information on the categorical variables
 that is relevant.'''

# Investigating 'address_neighborhood'
df_vivareal['address_neighborhood'].value_counts(dropna=False)

''' The neighborhood information must be treated. First of all, some equal values 
 were registered in a different way, for example: "Meia Praia", "MEIA PRAIA" and
 "meia praia". This values needs to be treated as a same value.'''

# Applying lower case
df_vivareal['address_neighborhood'] = df_vivareal['address_neighborhood'].str.lower()

# Excluding accents
df_vivareal['address_neighborhood'].loc[~df_vivareal['address_neighborhood'].isna()] = df_vivareal['address_neighborhood'].loc[~df_vivareal['address_neighborhood'].isna()].apply(lambda x: unidecode.unidecode(x))

# Correcting some particular cases
df_vivareal['address_neighborhood'].loc[df_vivareal['address_neighborhood']=='meia praia - frente mar'] = 'meia praia'
df_vivareal['address_neighborhood'].loc[df_vivareal['address_neighborhood']=='praia mar'] = 'jardim praia mar'

# Checking the column
df_vivareal['address_neighborhood'].value_counts(dropna=False)

''' The values are correct now. But the column has some NaN values. Could be
possible to acquire the neighborhood information by the "listing_title" column, once
some advertisers specify the locations' neighborhood on it. In order to acquiring 
this data, the title must be treated in the same way as the "address_neighborhood"'''

# Treating 'listing_title'
df_vivareal['listing_title'] = df_vivareal['listing_title'].str.lower()
df_vivareal['listing_title'].loc[~df_vivareal['listing_title'].isna()] = df_vivareal['listing_title'].loc[~df_vivareal['listing_title'].isna()].apply(lambda x: unidecode.unidecode(x))
 
# Creating a neighborhood_list
neighborhood_list = list(df_vivareal['address_neighborhood'].dropna().unique())

# Creating a function to find the elements on the title
def find_neighborhood(string, list_of_substrings = neighborhood_list):
    
    '''The present function will return the neighborhood if its present on the
    listing_title column.'''
    
    substring_found = ''
    for substring in list_of_substrings:
        if substring in string:
            substring_found += substring+','
            
    return substring_found
    
# Applying the function on registers with NaN on the 'address_neighborhood' column
df_vivareal['address_neighborhood'].loc[(df_vivareal['address_neighborhood'].isna())&(~df_vivareal['listing_title'].isna())] = df_vivareal['listing_title'].loc[(df_vivareal['address_neighborhood'].isna())&(~df_vivareal['listing_title'].isna())].apply(lambda x: find_neighborhood(x))

# Checking the column
df_vivareal['address_neighborhood'].value_counts(dropna=False)

''' Apparently, Itapema is both the city and the neighborhood. Will be assumed
that the titles with Itapema and another neighborhood are actually on the other
zone, on these cases, the "itapema" must be excluded. The "," also needs to be 
excluded.'''

# Removing wrong 'Itapema' values
df_vivareal['address_neighborhood'].loc[df_vivareal['address_neighborhood'].str.count(',') == 2] = df_vivareal['address_neighborhood'].loc[df_vivareal['address_neighborhood'].str.count(',') == 2].str.replace('itapema', '')

# Removing ","
df_vivareal['address_neighborhood'] = df_vivareal['address_neighborhood'].str.replace(',', '')

# Checking the column
df_vivareal['address_neighborhood'].value_counts(dropna=False)

''' After the treatment, the column still has 85 NaN values (its percentage dropped
 by 80%). These registers could be a problem for the model and should be excluded from 
 the dataframe. The "listing_title" is also not usefull anymore.
 The best way to add this information on the model is transforming each possible
 value on a binary column itself, where 1 = the place belongs to this neighborhood.'''

# Excluding Nan (in this case '') values
df_vivareal = df_vivareal.loc[df_vivareal['address_neighborhood']!='']

# Dropping 'listing_title' column
df_vivareal = df_vivareal.drop(['listing_title'], 1)

# Creating binary columns
for neighborhood in df_vivareal['address_neighborhood'].unique():
    df_vivareal[neighborhood] = 0
    df_vivareal[neighborhood].loc[df_vivareal['address_neighborhood']==neighborhood] = 1
    
# Removing address' columns
df_vivareal = df_vivareal.drop(['address_neighborhood', 'address_zipcode', 'address_street'], 1)

''' Once the places's neighborhood are correctly added, the amenities also needs
 to be included on the dataframe. The places amenities's are contained on a list
 and in order to quantify them, every possible amenitie will be represented by a
 binary column, where "1" indicates that the place has the amenitie. If the place
 doesn't have it, the value will be "0" '''

# Reidexing Dataframe
df_vivareal = df_vivareal.reset_index(drop=True)

# Removing characteres
for char_to_remove in ['[', ']', '{', '}', '"']:
    df_vivareal['amenities'] = df_vivareal['amenities'].apply(lambda x: x.replace(char_to_remove, "").replace(', ', ','))
    
# Applyying a CountVectorizer to create a amenities' dataframe
count_vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
cv_matrix = count_vectorizer.fit_transform(df_vivareal['amenities'])
df_amenities = pd.DataFrame(cv_matrix.toarray(), columns=count_vectorizer.get_feature_names_out()).drop('', 1)

# Merging the amenities' Dataframe to the original DataFrame
df_vivareal = df_vivareal.merge(df_amenities,  how='left', left_index=True, right_index=True)

# Dropping 'amenities' column
df_vivareal = df_vivareal.drop(['amenities'], 1)

# Setting 'listing_id' as the Dataframe index
df_vivareal = df_vivareal.set_index('listing_id')

# Checking other categorical variables
df_vivareal['usage_type'].value_counts()/df_vivareal['usage_type'].value_counts().sum()

'''Residential usage represents 99.3% of the registers, the other registers will be exluded'''

# Keeping only the Residential Usage places
df_vivareal = df_vivareal.loc[df_vivareal['usage_type']=='RESIDENTIAL'].drop(['usage_type'], 1)

# Checking other categorical variables
df_vivareal['unit_type'].value_counts()/df_vivareal['unit_type'].value_counts().sum()

'''Apartaments represents 95.6% of the registers, the other registers will be exluded'''

# Keeping only apartaments 
df_vivareal = df_vivareal.loc[df_vivareal['unit_type']=='APARTMENT'].drop(['unit_type'], 1)

''' Now that the Dataframe is finally modeled, it will be divided on two separate
 parts (concerning locations for Sale and Rent) and saved on the on 'modeled_data' folder'''

# Saving the modeled file on 'modeled_data' folder
df_vivareal.loc[~df_vivareal['sale_price'].isna()].drop(['rental_price'], 1).to_csv(r'modeled_data\Modeled_VivaReal_Data_Sale.csv')
df_vivareal.loc[~df_vivareal['rental_price'].isna()].drop(['sale_price'], 1).to_csv(r'modeled_data\Modeled_VivaReal_Data_Rent.csv')