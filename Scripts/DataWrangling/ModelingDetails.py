'''This code's main purpose is model "Details_Data.csv"'''

# Libraries needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from sklearn.feature_extraction.text import CountVectorizer
import unidecode

# Loading Price_AV_Itapema.csv dataset.
df_details = pd.read_csv(
    r'raw_data\Details_Data.csv',
    low_memory=False)

print('aaaa')

# Inspetcing NaN Values
df_details.isna().sum()


'''Some columns are composed mostly by NaN values, other columns wouldn't be usefull'''

# Excluding columns
to_delete_columns = ['url', 'ad_name', 'ad_description', 'space',
                     'additional_house_rules', 'owner','check_in', 'check_out',
                     'cohosts', 'index', 'response_time_shown', 'response_rate_shown',
                     'guest_satisfaction_overall', 'picture_count', 'min_nights',
                     'latitude', 'longitude', 'can_instant_book', 'is_superhost',
                     'localized_star_rating', 'star_rating', 'ano', 'mes', 'dia']

df_details = df_details.drop(to_delete_columns, 1)

# Inspecting DataFrame
df_details.info()

''' The id column type is int64. Changing it to a str column is a good practice'''

# Changing 'ad_id' type
df_details['ad_id'] = df_details['ad_id'].astype(str)

# Checking 'ad_id' column
id_details_count = df_details['ad_id'].value_counts()
print(f"Details_Data.csv has: {id_details_count.sum()} registers and {len(id_details_count)} unique ids.")

'''Its important to check why theres so many registers, once theres only 2311 places'''

# Transforming 'aquisition_date_column' into a datetime 
df_details['aquisition_date'] = pd.to_datetime(df_details['aquisition_date'])

# Creating date column
df_details['date'] = df_details['aquisition_date'].dt.date

# Checking the number of places on different aquisition dates
ids_dates = df_details[['date', 'ad_id']].value_counts().to_frame().reset_index()

ids_dates.head(10)

'''Its possible to check that theres some registers from the same place in the same day.
Could be usefull to see the date variance on the Dataframe'''

date_variance = (df_details.groupby('ad_id')['aquisition_date'].max() - df_details.groupby('ad_id')['aquisition_date'].min()).max()

print(f'The date variance on the Data Frame is: {date_variance}')

''' Analysing the Dataframe context - which concerns places/appartments for rent -
 theres no need for having more than 1 register per place. Even if some
 small changes may have occurred in the locations, their main characteristics would
 be maintained over the time.
 
 A new Dataframe, keeping only the last registers from each location will be created'''

# Creating the new Dataframe
df_details = df_details.sort_values(by=['aquisition_date'])
last_ad_indexes = df_details.ad_id.drop_duplicates(keep='last').index
condensed_details = df_details.loc[last_ad_indexes]
condensed_details = condensed_details.reset_index(drop=True)

# Checking the new Dataframe
condensed_details.info()

# Checking 'house_rules', 'amenities' and 'safety_features' columns
condensed_details[['house_rules', 'amenities', 'safety_features']].head(5)

''' The right way to keep the information contained on these column at the
Dataframe is vectorizing them. For example: "proibido fumar" is a house rule,
present in some registers, a new column called "proibido fumar" will be created,
containing 1 on the registers wich has the rule'''

# Replacing unwanted characthers
df_to_vectorize = condensed_details[['house_rules', 'amenities', 'safety_features']].fillna('')
for char_to_remove in ['[', ']', '{', '}', '"']:
    df_to_vectorize = df_to_vectorize.applymap(lambda x: x.replace(char_to_remove, "").replace(', ', ','))
    
    
# Vectorizing and merging the results on the DataFrame
count_vectorizer =  CountVectorizer(tokenizer=lambda x: x.split(','))

for array_column in df_to_vectorize.columns:
    cv_matrix = count_vectorizer.fit_transform(df_to_vectorize[array_column])
    df_vectorized = pd.DataFrame(cv_matrix.toarray(), columns=count_vectorizer.get_feature_names_out()).drop('', 1)
    condensed_details = condensed_details.merge(df_vectorized,  how='left', left_index=True, right_index=True)
    
# Dropping the vectorized columns, 'date' and 'aquisition_date'
condensed_details = condensed_details.drop(['aquisition_date', 'amenities',
                                            'house_rules', 'safety_features', 'date'], 1)

# Each of the listing_type possibilities will be also turned into a binary column
for ltype in condensed_details['listing_type'].unique():
    condensed_details[ltype] = 0
    condensed_details[ltype].loc[condensed_details['listing_type']==ltype] =1

# Droppinf 'listing_type' column
condensed_details = condensed_details.drop('listing_type', 1)

# Saving the modeled file on 'modeled_data' folder
condensed_details.to_csv(r'modeled_data\Modeled_Details_Data.csv')