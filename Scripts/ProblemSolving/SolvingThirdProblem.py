''' This code aims to answer the following question: "What are the characteristics
 and reasons for the best revenues in the city?"?
 
 Almost all the possible paramethers of the the Modeled_Airbnb_Data.csv will be considered
 as a potential characteristic to increasing the revenue generated.''' 
 


# Libraries needed
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans

# Loading Modeled_Airbnb_Data.csv
df_airbnb = pd.read_csv(r'C:\Users\andrr\Desktop\Case\SeazoneCase\modeled_data\Modeled_Airbnb_Data.csv')

''' As it was already seen, the properties with the type 'Quarto inteiro em pousada' are outliers,
 they'll be excluded.'''
 
# Excluding outliers
df_airbnb = df_airbnb.drop(df_airbnb.loc[df_airbnb['Quarto inteiro em pousada']==1].index)

'''The exceptions will be "availability_rate" and "average_price" cause these paramethers are
direclty related to the total revenue, number of reviews and some of the hosts information
will also be desconsiderated.'''

# Separating the predictors
predictor_paramethers = list(set(df_airbnb.columns[3:]) - set(['number_of_reviews', 'n_of_diff_dates',
        'ad_id', 'host_rating', 'n_reviews', 'n_listings', 'latitude', 'longitude', 'minimum_stay_mode']))

''' The latitude and longitude values will be treated using the K-means Machine 
 Learning algorithm in order to group properties with similar geolocations into geozones.'''

# Creating a DataFrame
df_geolocation = df_airbnb[['latitude', 'longitude']]

# Transforming the data
scaler = StandardScaler()
x = scaler.fit_transform(df_geolocation.values)

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

''' 5 is the ideal number of clusters.'''

# Applying the K-means algorithm
kmeans = KMeans(n_clusters = 5, random_state = 0)
predictions = kmeans.fit_predict(x)

# Keeping just the predictor columns on the Dataset
df_airbnb = df_airbnb[predictor_paramethers]
df_airbnb['geolocation_zones'] = predictions

''' The geolocation_zones are a categorical column, which needs to be vectorized.'''

# Treating geolocation_zones
df_airbnb['geolocation_zones'] = df_airbnb['geolocation_zones'].astype(str).apply(lambda x: f'geolocation zone: {x}')

# Each of the geolocation_zones possibilities will be also turned into a binary column
for geozone in df_airbnb['geolocation_zones'].unique():
    df_airbnb[geozone] = 0
    df_airbnb[geozone].loc[df_airbnb['geolocation_zones']==geozone] = 1
    
# Dropping the categorical column
df_airbnb = df_airbnb.drop(['geolocation_zones'], 1).fillna(0)

# Separating the predictors
X = df_airbnb.drop(['total_revenue'], 1).values

# Separating the total_revenue (target for the prediction)
y = df_airbnb['total_revenue'].fillna(0).values

# Scalling the values
scaler = StandardScaler()
X = scaler.fit_transform(X)

''' Now that all the data is ready, a Machine Learning Regression Model will be applied. 
The purpose of applying the model is to check if the total revenue is predictable based on
 it's characteristics and which of them are more relevant.
 
 The test will be repeated 10 times in order to collect more results and if the score
 is greater than 80% it will be added to a DataFrame.'''
 
df_feature_importances = pd.DataFrame(index = df_airbnb.drop(['total_revenue'], 1).columns, columns = range(0,100))

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


''' As it was already seen on the previously analysis, the most critical characteristics
 for the revenue are related to the number of guests and rooms (bigger number = bigger revenue).
 The 4 paramethers based on it are, by far, the most critical.
 
 The number of dates that the property were on the listings Dataset is also a good predictor,
 so, besides the'''