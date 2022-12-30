''' This code aims to answer the following question: "Which is the best location
in the city in terms of revenue"?
 
 The 'location' will be defined as the property's neighborhood '''

# Libraries needed
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

''' For this, the Modeled_Airbnb_Data.csv will be used.'''

# Loading Modeled_Airbnb_Data.csv
df_vivareal_rent = pd.read_csv(r'modeled_data\Modeled_VivaReal_Data_Rent.csv')

# Listing the possible neighborhoods
neighborhoods = df_vivareal_rent.columns[8:26]

'''A Dataframe will be creating for containing the average rental price and the
 number of properties on each neighborhood'''

# Creating DataFrame
df_neighborhoods = pd.DataFrame(index = neighborhoods, columns = ['avg_rental_price', 'n_of_places'])

# Filling the DataFrame
for neighborhood in neighborhoods:
    if len(df_vivareal_rent.loc[df_vivareal_rent[neighborhood]==1]) > 1:
        df_neighborhoods['avg_rental_price'].loc[neighborhood] = df_vivareal_rent['rental_price'].loc[df_vivareal_rent[neighborhood]==1].mean()
        df_neighborhoods['n_of_places'].loc[neighborhood] = len(df_vivareal_rent['rental_price'].loc[df_vivareal_rent[neighborhood]==1])
df_neighborhoods = df_neighborhoods.dropna()

# Plotting a bar graph
plt.title('Average price per property type')
plt.bar(df_neighborhoods['avg_rental_price'].sort_values(ascending=False).index,
        df_neighborhoods['avg_rental_price'].sort_values(ascending=False),
        color='lightblue', width=.6, linewidth=.8, edgecolor='black')
plt.xticks(rotation = 45, size=10)
plt.show()

''' Considering the revenue, the best location in terms of revenue is on
the "meia praia" neighborhood, "andorinha" also has a high value. Otherwise
"ilhota" and  "morretes" properties has the smallest average prices'''

