'''This code's main purpose is to get some first expressions about the Datasets given'''

# Libraries needed
import pandas as pd
import zipfile_deflate64 as zipfile
import sys

# Checking 'Price_AV_Itapema.csv'
tag_hist_path = r"raw_data\Price_AV_Itapema.zip"
parentZip = zipfile.ZipFile(tag_hist_path, mode="r", compression=zipfile.ZIP_DEFLATED64)
df_price_airbnb = pd.read_csv(parentZip.open('Price_AV_Itapema.csv', mode="r"))

# Checking the loaded DataFrame's size and columns.
print(f"The Price_AV_Itapema.csv size is {sys.getsizeof(df_price_airbnb)/10**9}GB.")

print(f"Price_AV_Itapema.csv columns: {df_price_airbnb.columns.values}.")

id_price_count = df_price_airbnb['airbnb_listing_id'].value_counts()
print(f"Price_AV_Itapema.csv has: {id_price_count.sum()} registers and {len(id_price_count)} unique ids.")

''' It's important to check if the "airbnb_listing_id" column matches with the
other Airbnb datasets'''

# Checking 'Details_Data.csv'
df_details_airbnb = pd.read_csv(r'raw_data\Details_Data.csv')

# Checking the loaded DataFrame's columns.
print(f"Details_Data.csv columns: {df_details_airbnb.columns.values}.")

id_details_count = df_details_airbnb['ad_id'].value_counts()
print(f"Details_Data.csv has: {id_details_count.sum()} registers and {len(id_details_count)} unique ids.")

# Checking if both Datasets are about the same places
if (set(df_details_airbnb['ad_id']) == set(df_price_airbnb['airbnb_listing_id'])) == True:
    print('Price_AV_Itapema.csv and Details_Data.csv has the exact same list of ids.')
else:
    print('The databases has a different set of ids.')

''' It's noticed that both Dataframes reffers to the same group of places/appartaments.
 So, in some cases they could be joined on a same Dataframe. The Details_Data.csv also
 has a "owner_id" column, that can be related to Hosts_ids_Itapema.csv'''

# Checking 'Details_Data.csv'
df_hosts_airbnb = pd.read_csv(r'raw_data\Hosts_ids_Itapema.csv')

# Checking the loaded DataFrame's columns.
print(f"Hosts_ids_Itapema.csv columns: {df_hosts_airbnb.columns.values}.")

# Checking if both Datasets are about the owners/hosts
if (set(df_details_airbnb['owner_id']) == set(df_hosts_airbnb['host_id'])) == True:
    print('Price_AV_Itapema.csv and Details_Data.csv has the exact same list of ids.')
else:
    print('The databases has a different set of ids.')
   
     
'''The set of host_ids is not exactly the same, but since the main analysis are related
to the places/appartments, and not about the hosts, if all of the owner_ids from
Details_Data are contained in Hosts_ids_Itapema a "left join" could be used, where
the hosts on Hosts_ids_Itapema which are not in Details_Data can be desconsidered'''

# Checking if all the owners from 'Details_Data.csv' are in 'Hosts_ids_Itapema.csv'
if ((set(df_hosts_airbnb['host_id']) - set(df_details_airbnb['owner_id'])) == set()) == True:
    print('All the ids from Details_Data.csv are in Hosts_ids_Itapema.csv.')
else:
    print('Some hosts from Details_Data.csv are not in Hosts_ids_Itapema.csv.')
    
    
# Checking 'Mesh_Ids_Data_Itapema.csv'
df_mesh_airbnb = pd.read_csv(r'raw_data\Mesh_Ids_Data_Itapema.csv')

# Checking the loaded DataFrame's columns.
print(f"Mesh_Ids_Data_Itapema.csv columns: {df_mesh_airbnb.columns.values}.")


'''Once the Mesh_Ids_Data_Itapema.csv is the most reliable information about latitude
and longitude, its set of ids will be compared with the Details_Data.csv ids'''

# Checking if both Datasets are about the same places
if (set(df_details_airbnb['ad_id']) == set(df_mesh_airbnb['airbnb_listing_id'])) == True:
    print('Price_AV_Itapema.csv and Details_Data.csv has the exact same list of ids.')
else:
    print('The databases has a different set of ids.')

print('fim')
