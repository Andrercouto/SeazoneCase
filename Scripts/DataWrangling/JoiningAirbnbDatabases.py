'''This code's purpose is to join the already modeled Datasets with Mesh_Ids_Data_Itapema.csv
 and Hosts_ids_Itapema.csv .'''

# Libraries needed
import pandas as pd
import numpy as np

# Loading the modeled DataFrames
df_condensed_prices = pd.read_csv(r'modeled_data\Modeled_Prices_AV_Itapema.csv')
df_condensed_prices = df_condensed_prices.rename(columns={df_condensed_prices.columns[0]: 'ad_id'})
df_condensed_prices.ad_id = df_condensed_prices.ad_id.astype(str)
df_condensed_prices = df_condensed_prices.set_index('ad_id')


df_condensed_details = pd.read_csv(r'modeled_data\Modeled_Details_Data.csv')
df_condensed_details = df_condensed_details.drop([df_condensed_details.columns[0]],1)
df_condensed_details.ad_id = df_condensed_details.ad_id.astype(str)
df_condensed_details = df_condensed_details.set_index('ad_id')

'''The modeled DataFrames will be joined first to Mesh_Ids_Data_Itapema.csv'''

# Loading Mesh_Ids_Data_Itapema.csv dataset
df_mesh = pd.read_csv(r'raw_data\Mesh_Ids_Data_Itapema.csv')

# Checking the loaded Dataframe
df_mesh.info()

# Dropping duplicates
df_mesh = df_mesh.drop_duplicates()

'''The only relevant columns are latitude and longitude (besides id)'''

# Keeping relevant columns
df_mesh = df_mesh[['airbnb_listing_id', 'latitude', 'longitude']].rename(columns={'airbnb_listing_id':'ad_id'})

# Changing the id's type
df_mesh.ad_id = df_mesh.ad_id.astype(str)

# Reindexing the DataFrame
df_mesh = df_mesh.set_index('ad_id')

# Joining the Dataframes
df_airbnb_modeled = df_condensed_prices.merge(df_condensed_details, how='inner', left_index=True, right_index=True)
df_airbnb_modeled = df_airbnb_modeled.merge(df_mesh, how='inner', left_index=True, right_index=True)

'''Some owner's information would also be useful'''

# Loading Mesh_Ids_Data_Itapema.csv dataset
df_hosts = pd.read_csv(r'raw_data\Hosts_ids_Itapema.csv')

# Checking the loaded Dataframe
df_hosts.info()

'''The only relevant columns are host rating, number of reviews, and number of
 listings (besides id).'''
 
# Keeping relevant columns
df_hosts = df_hosts[['host_id', 'host_rating', 'n_reviews', 'n_listings']].rename(columns={'host_id':'owner_id'})

''' df_airbnb_modeled and df_hosts will be joined considering the owner/host id.'''

# Changing the owner id's types
df_hosts.owner_id = df_hosts.owner_id.astype(str)
df_airbnb_modeled.owner_id = df_airbnb_modeled.owner_id.astype(str)

# Reindexing the Dataframes
df_airbnb_modeled = df_airbnb_modeled.reset_index().set_index('owner_id')
df_hosts = df_hosts.set_index('owner_id')

# Joining the Dataframes
df_airbnb_modeled = df_airbnb_modeled.merge(df_hosts, how='left', left_index=True, right_index=True)

# Reindexing the modeled DataFrame
df_airbnb_modeled = df_airbnb_modeled.set_index('ad_id')

''' At this point all the Airbnb information is condensed on the DataFrame. The properties 
 bussiness values (price, revenue, availability), its features (number of rooms,
 amenities, rules, location type), its latitude and longitude and some information
 about its hosts'. Teorically the Data Wrangling could finish here, but there are some proccess
 that will be done in order to facilitate the Databases furter use. For example, there's two columns
 called "proibido fumar" and "permitido fumar", they are opposite one of them
 will be dropped. It occurs in more than one case.'''

 
# Dropping redundant columns
df_airbnb_modeled = df_airbnb_modeled.drop(['proibido fumar', 'animais de estimação são permitidos',
                                            'não é adequado para crianças ou bebês', 'cafeteira',
                                            'itens básicos de cozinha', 'itens básicos de praia',
                                            'kitchenette'], 1)


''' Some columns were represented both on the amenities and safety_features on the 
 original dataset Modeled_Details_Data.csv. There's no need for keeping both on the DataFrame.'''
 
# Dropping duplicated columns
to_delete_columns = []
for column in df_airbnb_modeled.columns:
    if column[len(column)-2:] == '_y':
        to_delete_columns.append(column)
    if column[len(column)-2:] == '_x':
        df_airbnb_modeled = df_airbnb_modeled.rename(columns={column:column[:len(column)-2]})
df_airbnb_modeled = df_airbnb_modeled.drop(to_delete_columns, 1)


# Saving the modeled file on 'modeled_data' folder
df_airbnb_modeled.to_csv(r'modeled_data\Modeled_Airbnb_Data.csv')