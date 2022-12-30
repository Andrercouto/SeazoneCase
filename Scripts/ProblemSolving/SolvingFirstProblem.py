''' This code aims to answer the following question: "What is the best property
 profile to invest in the city"?
 
 A 'best investiment' will be defined by the average price of the property and the
 availability rate (cause a place being is always available could indicate that the
 clients have no interest on renting it).'''

# Libraries needed
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


''' The problem apparently is about RENTAL properties. For this, the Modeled_Airbnb_Data.csv will be used.'''

# Loading Modeled_Airbnb_Data.csv
df_airbnb = pd.read_csv(r'modeled_data\Modeled_Airbnb_Data.csv')

''' Once Seazone is focused on short-stay vacation homes, properties that usually
 have a minimum staying days above a week will be desconsidered.'''
 

df_airbnb = df_airbnb.loc[df_airbnb['minimum_stay_mode'].isin(['1','2','3','4','5','6','7'])]

''' Considering the Airbnb Modeled Dataset, the averages price for the different
 property types will be checked.'''

# Separating different property types
property_types = df_airbnb.columns[134:169]
print(f'Possible property types:{property_types}')

# Checking the number, percentage and accumulative percentage of properties with the different types
df_property_type = df_airbnb[property_types].sum().sort_values(ascending=False).to_frame()
df_property_type = df_property_type.rename(columns={0: 'number_of_properties'})
df_property_type['%'] = df_property_type['number_of_properties']/df_property_type['number_of_properties'].sum()
df_property_type['acc_%'] = df_property_type['%'].cumsum()

# Adding the average price of the different property types
df_property_type['avg_price'] = 0
for property_type in df_property_type.index:
    df_property_type['avg_price'].loc[property_type] = df_airbnb['avg_price'].loc[df_airbnb[property_type]==1].mean()


# Checking the most expensives property types
df_property_type[['avg_price', '%', 'number_of_properties']].sort_values(by=['avg_price'], ascending=False).head(5)
df_property_type[['avg_price', '%']].sort_values(by=['avg_price'], ascending=False)['%'].head(3).sum()

''' As it could be seen, the average price of 'Quarto inteiro em pousada', 'Espaço inteiro: bangalô'
 and 'Espaço inteiro: vila' types are highly bigger than the other types, but it represents less than
 0.5% of the total properties. Could be a good investiment, but maybe theres' some hidrances on these
 type of properties, otherwise would be more options for renting.'''

# Most commom properties types' prices
df_property_type['avg_price'].head(3)

# Plotting a bar graph
plt.title('Average price per property type')
plt.bar(df_property_type['avg_price'].head(3).index,
        df_property_type['avg_price'].head(3),
        color='lightblue', width=.6, linewidth=.8, edgecolor='black')
plt.xticks(rotation = 45, size=10)
plt.show()


''' It's noticed that are some difference among the properties type, but knowing 
 if the clients have interest on renting these properties is also needed. For this
 the mean availability_rate of these property types' will be found. Lower availability
 rates means that the places are constatly being used, and it indicates that the clients
 haver interest on it'''

# Adding the average price of the different property types
df_property_type['availability_rate'] = 0
for property_type in df_property_type.index:
    df_property_type['availability_rate'].loc[property_type] = df_airbnb['availability_rate'].loc[df_airbnb[property_type]==1].mean()

# Plotting a bar graph
plt.title('Availability rate per property type')
plt.bar(df_property_type['availability_rate'].head(3).index,
        df_property_type['availability_rate'].head(3),
        color='lightblue', width=.6, linewidth=.8, edgecolor='black')
plt.xticks(rotation = 45, size=10)
plt.show()


''' As it can be checked, the availability rate of the property types are almost
 the same, so the price it's principal indicator of what could be a good investment.
 It's also important to see which features are more important concerning the properties,
 for this a Machine Learning Regression Model will be applied on the different groups
 of properties based on it's type. The purpose of applying the model is to check if
 the properties price are predictable based on it's features and which features are
 more relevant'''

''' A function will be created in order to aply the Random Forest Regression model
 on the choosen data in order to predict its price. If the prediction score is above 80%
 it will be considered accurate, and the paramethers importances for the prediction will
 be added on a DataFrame.'''

# The number of reviews is not a property features
df_airbnb = df_airbnb.drop(['number_of_reviews'],1)

# Separating the predictor paramethers
features_columns = df_airbnb.columns[6:134]

# Creating a dataframe for the features importances
df_features = pd.DataFrame(index = features_columns)


# Creating the fuction
def automatizing_random_forest(df, column):
    
    # Keeping only the registers with the same property type
    df = df.loc[df[column]==1]

    # Defining the predictors and the target
    X = df[features_columns].fillna(0).values
    y = df['avg_price'].values

    # Scaling the variables
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Spliting the test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

    # Applying the Random Forest model
    regressor = RandomForestRegressor(n_estimators=40)
    regressor.fit(X_train, y_train)
    score = regressor.score(X_train, y_train)
    predictions = regressor.predict(X_test)
    
    print(f"\nThe algorithm's accuracy for registers with the '{column}' property type is: {score*100}%\n")
    if score > .80:
    
        df_features[column] = regressor.feature_importances_
    
    return

# Applying function 
automatizing_random_forest(df_airbnb, 'Espaço inteiro: apartamento')
automatizing_random_forest(df_airbnb, 'Espaço inteiro: casa')
automatizing_random_forest(df_airbnb, 'Espaço inteiro: condomínio')

# Features importances
df_features = df_features.loc[df_features.sum(1).sort_values(ascending=False).index]
print(f'The most important features are:{df_features.head(5).index}')

''' Number of bathrooms, bedrooms, guests and beds are always between the most
 relevant features for increasing the properties price'''

# Relevance of the 'number_of_bathrooms', 'number_of_bedrooms', 'number_of_guests' and 'number_of_beds'
print(f" The relevance of the number of bathrooms, bedrooms, guests and beds corresponds to {100*(df_features.loc[['number_of_bathrooms', 'number_of_bedrooms', 'number_of_guests','number_of_beds']].sum().mean())} of the model's weight.")


''' Conclusion:
    
        Some property types like "Vila", "Banglô" and "Pousada" have a very expensive average price.
    But they are uncommom. Considering the most commom property types as "Condomínio", "Casa" and "Apartamento"
    there's no considerably difference on the availabilty rate. But are some differences on the prices.
    
        The method's accuracy for predicting the properties rental prices score is
    almost 90% for all of the three groups of properties. It can be considered accurate
    and its features can be used for predicting the price.
 
        The most relevant features are 'number_of_bathrooms', 'number_of_bedrooms', 'number_of_guests'
    and 'number_of_beds. Their correlation is positive in, so a bigger number of rooms would imply, generaly,
    on a more expensive property.
    
    Investing on "Vila", "Banglô" and "Pousada" could be considered the best investment. But considering the most
    commom types of properties, the "Condomínios" are the best choice.
    
'''
