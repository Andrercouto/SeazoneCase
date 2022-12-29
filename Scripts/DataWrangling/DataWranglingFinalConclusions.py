'''Final conclusions of the Data Wrangling Process'''

# Libraries needed
import pandas as pd
import zipfile_deflate64 as zipfile
import sys

''' Loading the Airbnb Raw Data'''

# Loading Price_AV_Itapema.csv dataset
tag_hist_path = r"raw_data\Price_AV_Itapema.zip"
parentZip = zipfile.ZipFile(tag_hist_path, mode="r", compression=zipfile.ZIP_DEFLATED64)
df_prices =  pd.read_csv(parentZip.open('Price_AV_Itapema.csv', mode="r"))

# Loading Details_Data.csv dataset.
df_details = pd.read_csv(
    r'raw_data\Details_Data.csv',
    low_memory=False)

# Loading Hosts_ids_Itapema.csv dataset.
df_hosts = pd.read_csv(
    r'raw_data\Hosts_ids_Itapema.csv',
    low_memory=False)

# Loading Mesh_Ids_Data_Itapema.csv dataset.
df_mesh = pd.read_csv(
    r'raw_data\Mesh_Ids_Data_Itapema.csv',
    low_memory=False)

''' Loading the Airbnb Modeled Data'''

# Loading Modeled_Airbnb_Data.csv dataset.
df_airbnb_modeled= pd.read_csv( 
    r'modeled_data\Modeled_Airbnb_Data.csv',
    low_memory=False)

total_airbnb_raw_size = sys.getsizeof(df_prices) + sys.getsizeof(df_details) + sys.getsizeof(df_hosts) + sys.getsizeof(df_mesh)
total_airbnb_modeled_size = sys.getsizeof(df_airbnb_modeled)

print(f'Describing the Airbnb Datasets wrangling process:')

print(f'The modeled Airbnb Dataset has {round(((total_airbnb_modeled_size/total_airbnb_raw_size)*100),2)}% of the Airbnb raw data.')

print(f'The Data Wrangling proccess transformed 4 datasets with {df_prices.shape, df_details.shape, df_hosts.shape, df_mesh.shape} shapes into a {df_airbnb_modeled.shape} file.')

''' Loading the VivaReal Raw Data'''

# Loading VivaReal_Itapema.csv dataset.
df_vivareal = pd.read_csv(
    r'raw_data\VivaReal_Itapema.csv',
    low_memory=False)

# Loading Modeled_VivaReal_Data_Rent.csv dataset.
df_vivareal_rent_modeled = pd.read_csv(
    r'modeled_data\Modeled_VivaReal_Data_Rent.csv',
    low_memory=False)

# Loading Modeled_VivaReal_Data_Sale.csv dataset.
df_vivareal_sale_modeled = pd.read_csv( 
    r'modeled_data\Modeled_VivaReal_Data_Sale.csv',
    low_memory=False)

print(f'\nDescribing the VivaReal Datasets wrangling process:')

total_vivareal_raw_size = sys.getsizeof(df_vivareal)
total_vivareal_modeled_size = sys.getsizeof(df_vivareal_rent_modeled) + sys.getsizeof(df_vivareal_sale_modeled)

print(f'The two modeled VivaReal Datasets has {round(((total_vivareal_modeled_size/total_vivareal_raw_size)*100),2)}% of the VivaReal raw data.')

print(f'The Data Wrangling proccess transformed a dataset a {df_vivareal.shape} file into two datasets with {df_vivareal_rent_modeled.shape, df_vivareal_sale_modeled.shape} shapes.')
