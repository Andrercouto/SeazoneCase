''' This code aims to answer the following question: "We would like to build a 
building of 50 apartments in the city, where should we build it and how should the 
apartments be designed in order to be a great investment? and "How much will be the
 return on investment of this building in the years 2024, 2025 and 2026?
"

 For solving this problem, the Modeled_Airbnb_Data.csv will be used'''
 
 
# Libraries needed
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import numpy as np


# Loading Modeled_Airbnb_Data.csv
df_airbnb = pd.read_csv(r'modeled_data\Modeled_Airbnb_Data.csv')

''' Only the registers with the property type = "Espaço inteiro: apartamento"
 will be considered, and all the columns related to property type will be excluded.'''
 
# Keeping the right registers 
df_airbnb = df_airbnb.loc[df_airbnb['Espaço inteiro: apartamento']==1]

# Deleting property type columns
df_airbnb = df_airbnb.drop(df_airbnb.columns[134:166],1)

''' Just the amenities that are present on 100% of the database will be considered
 on the analysis.'''
 
# Checking amenities occurrences
amenities_occurrences = df_airbnb[df_airbnb.columns[20:134]].sum()

# Listing amenities to drop
to_drop_amenities = amenities_occurrences.loc[amenities_occurrences<(len(df_airbnb)/10)].index

# Dropping columns
df_airbnb = df_airbnb.drop(to_drop_amenities, 1)

''' There's some other columns related to hosts, id, etc to drop. '''

# Listing column
to_drop_columns = ['ad_id', 'availability_rate', 'avg_price',  'number_of_reviews',
                   'host_rating', 'n_reviews', 'n_listings']

# Dropping columns
df_airbnb = df_airbnb.drop(to_drop_columns, 1)


''' Once Seazone is focused on short-stay vacation homes, properties that usually
 have a minimum staying days above a week will be desconsidered.'''
 
# Keeping the right registers 
df_airbnb = df_airbnb.loc[df_airbnb['minimum_stay_mode'].isin(['1','2','3','4','5','6','7'])].drop('minimum_stay_mode',1)

''' The metric to indicate a good investiment, on this case will be the total_revenue/n_of_diff_dates,
 once it encompasses will indicate generated revenue considering the number of possible days '''
 
# Creating the revenue column
df_airbnb['revenue'] = df_airbnb['total_revenue']/df_airbnb['n_of_diff_dates']

# Dropping columns
df_airbnb = df_airbnb.drop(['total_revenue', 'n_of_diff_dates'], 1).fillna(0)

''' The geolocation values (latitude and longitude) and the revenue will be aggregated with
 the K-means Clustering algorithm.'''
 
# Creating the DataFrame 
df_locations = df_airbnb[['latitude', 'longitude', 'revenue']]

# Transforming the data
scaler = StandardScaler()
x = scaler.fit_transform(df_locations.values)

''' The K-means doesn't specifies the ideal number of clusters (in the case, the
 ideal number of geozones, and for choosing the ideal number a wcss technique will be used.'''

# Applying WCSS technique
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters = i, random_state = 0)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss, marker='X', color='black')  
plt.xlabel('N de clusters')  
plt.ylabel('WCSS') 

''' By cheching the WCSS graph is noticed that 6 is the ideal number of clusters.'''

# Applying the K-means algorithm
kmeans = KMeans(n_clusters = 6, random_state = 0)
predictions = kmeans.fit_predict(x)

# Adding the cluster to the location's DataFrame
df_locations['cluster'] = predictions

# Checking the number of registers on each cluster
df_locations['cluster'].value_counts()

# Checking the mean revenue of the different clusters
df_locations.groupby('cluster')['revenue'].agg('mean')

''' It's possible to check that the properties from the cluster "3" 
 are the moste valuable, but theres just only 32 registers on it.
 The cluster "4" also has a revenue value considerably higher than the others
 so, it could also be a good choice for investing'''
 
# Checking the geolocation centers of clusters 3 and 4

print(f" The cluster '3' has a revenue value of {df_locations['revenue'].loc[df_locations['cluster']==3].mean()} and it's centered on {(df_locations['latitude'].loc[df_locations['cluster']==3].mean(), df_locations['longitude'].loc[df_locations['cluster']==3].mean())}'.")
print(f" The cluster '4' has a revenue value of {df_locations['revenue'].loc[df_locations['cluster']==4].mean()} and it's centered on {(df_locations['latitude'].loc[df_locations['cluster']==4].mean(), df_locations['longitude'].loc[df_locations['cluster']==4].mean())}'.")

# Removing geolocation columns
df_airbnb = df_airbnb.drop(['latitude', 'longitude'], 1)

# Separating the predictors
X = df_airbnb.drop(['revenue'],1).fillna(0).values

# Separating the total_revenue (target for the prediction)
y = df_airbnb['revenue'].fillna(0).values


''' Now that all the data is ready, a Machine Learning Regression Model will be applied. 
The purpose of applying the model is to check if the total revenue is predictable based on
 it's characteristics and which of them are more relevant.
 
 The test will be repeated 10 times in order to collect more results and if the score
 is greater than 80% it will be added to a DataFrame.'''
 
df_feature_importances = pd.DataFrame(index = df_airbnb.drop(['revenue'], 1).columns, columns = range(0,10))

for i in df_feature_importances.columns:
    # Spliting the test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    
    # Applying the Random Forest model
    regressor = RandomForestRegressor(n_estimators=40)
    regressor.fit(X_train, y_train)
    score = regressor.score(X_train, y_train)
    predictions = regressor.predict(X_test)
    print(f"\nThe algorithm's accuracy is: {score*100}%\n")
    if score > .80:
        df_feature_importances[i] = regressor.feature_importances_

df_feature_importances.mean(1).sort_values(ascending=False).head(10)

''' And the conclusion of this problem is similar to the other's, the number of rooms
 are the features that impacts more the properties revenue. Good locations for building 
 would be close to the coordinates  (-27.12172499266571, -48.603734205355465) or
 (-27.129436467728883, -48.60189474962269).
 
 For calculating the return over the year, it will be assumed that a building with the
 characteristics that increases its revenue will be built'''
 
 
# The building would be close to the most valuable clusters centers
df_building = df_airbnb.loc[df_locations.loc[df_locations['cluster'].isin([3, 4])].index]

# Minimum rooms, guests and beds based on the databases 3 quartile
for feature in ['number_of_bathrooms', 'number_of_guests', 'number_of_guests', 'number_of_bedrooms']:
    df_building = df_building.loc[df_building[feature]>=np.percentile(df_airbnb[feature], 50)]

print(df_building['revenue'].mean()*365*50)

''' The revenue over a year, considering that the properties would be available for use
 or in use would be almost R$13.000.000.'''
