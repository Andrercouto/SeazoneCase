# Case Seazone - Data Scientist

The actual repository encompasses a testing Case for a data scientist job opportunity at Seazone. The Case was designed for testing both the coding skills, logical thinking and analytical capabilities, and it's based on a work done at Seazone, with real data and it's divided in two parts.

The first part consists on treating (wrangling, enriching, modeling) the raw data, while the second part is based on getting insights (using data analytics techniques, regression machine learning models and business intelligence skills) from the modeled data in order to make better strategic decisions and try to find solutions for the proposed problems on the [case description](https://github.com/Andrercouto/SeazoneCase/blob/main/references/seazone_code_challenge.pdf).



## Configuring the Environment

### Basics Dependencies

 - The project was designed on Python 3.10.0 and some packages needed may be uncompatible with later versions.

 - The necessary packages are on: [requirements.txt](https://github.com/Andrercouto/SeazoneCase/blob/main/requirements.txt).

 - The Datasets given in the Case's description were added on: [datasets](https://github.com/Andrercouto/SeazoneCase/tree/main/data). It's relevant to note that while the other files are on *.csv* format, the *Price_AV_Itapema*'s dataset is a compressed file, and the reason is that it was too large (4GB) for Github's storage size.

### Installing

For running the aplication, the <code>virtualenv</code> library must be correctly installed. If it's not, just run:

<code>pip install virtualenv</code>

Clone the repository and install all the packages necessary:

```
py -3.10 -m venv my_env 
source my_env\scripts\activate 
cd my_env
git clone https://github.com/Andrercouto/SeazoneCase.git 
cd SeazoneCase
pip install -r requirements.txt
```

## Starting the Case

### Part 1 - Data Wrangling

Once the Repository has its Databases and the necessary dependencies configured, the first part of the Case can be started. It concerns Data Wrangling, which is process of transforming "Raw Data" into a more appropriate and valuable format (in this specific case, preferably a format that fits into a regression machine learning model), ensuring its quality and usefulness. 

The Case is based on data scrapped from *Airbnb* and *VivaReal* sites, and concerns places for rent and/or sale. These places can be apartments or houses that, in order to facilitate the understanding of the report (and the comments present in the codes), will be called **properties**.

Four of the five given Datasets were scrapped from *Airbnb*. The first questions would be: 

- *Do these different datasets represent the same set of properties?*

- *If they are, would be usefull - or even possible - to merge them into a condensed dataset, which would contain their most critical information? How could it be done?*

#### Check Airbnb Data

The [CheckAirbnbData.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/CheckAirbnbData.py) script (*which cointains comments specifying more clearly the steps taken on each line*) found out that **yes**, this Datasets are related to the same set of properties, so, it could be usefull to join them.

Each one of the datasets will need to be treated in a different way in order to *condense* and *merge* them without losing important information. In order to keep the modeled data a [new folder](https://github.com/Andrercouto/SeazoneCase/tree/main/modeled_data) was created.

#### Wrangling *Details_Data.csv*

Once it's noticed that the Airbnb Databases contains information about the same properties, the next steps will be treating them in a way that would be possible to consolidate their information in just **one** Dataset.

The [ModelingDetails.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/ModelingDetails.py) script's purpose was on modeling the [Details_Data.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/raw_data/Details_Data.csv) dataset (which contains the properties's specificities, such as amenities, house rules, location type, rooms of the house), condensing it in order to keep just one register for each property. The qualitative technique was also treated (*vectorized*), and a modeled dataframe ([Modeled_Details_Data.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_Details_Data.csv)) was added on the '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.

#### Wrangling *Price_AV_Itapema.zip*

Among the Datasets given, *Price_AV_Itapema.csv* was the biggest one (it even needed to be compressed for decreasing its size) and the [ModelingPrices.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/ModelingPrices.py) script's purpose was summarizing a 40 milion registers Database in a modeled format that could be related with the others *Airbnb Datasets*. After excluding *NaN* values on critical columns, treating outliers, and creating usefull metrics a condensed *.csv* [file](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_Prices_Data.csv) - where each register represents a properties - was created and added to the '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.

#### Wrangling *Mesh_Ids_Data_Itapema.csv*, *Hosts_ids_Itapema.csv* and joining all Airbnb Data

At this moment, the two most complex datasets (considering the *Airbnb* datasets) were already modeled and ready for being joined. [JoiningAirbnbDatabases.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/JoiningAirbnbDatabases.py) script's purpose was treating the other datasets and merging all of them.

 - *Mesh_Ids_Data_Itapema.csv* had latitude and longitude information and a 'id' (one id for each property) column which was used as a key for joining it.

- *Hosts_ids_Itapema.csv* contained some relevant information about the properties' hosts, and a 'owner_id' column that was used for merging it with modeled dataset *Modeled_Details_Data.csv*, which also has a 'owner_id' column. 

The final file ([Modeled_Airbnb_Data.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_Airbnb_Data.csv)) was added to '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.


#### Wrangling *VivaReal_Itapema.csv*

*VivaReal_Itapema.csv* is the only dataset that is not related with the others. The [ModelingVivaRealDatabase.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/ModelingVivaRealDatabase.py) script's purpose was wrangling the file, excluding *NaN* values, treating outliers, inspecting some inconsistent data, vectorizing its categorical columns. Its data concerns properties for rent and sale in the way that **two** modeled datasets were created from it ([Modeled_VivaReal_Data_Sale.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_VivaReal_Data_Sale.csv) and [Modeled_VivaReal_Data_Rent.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_VivaReal_Data_Rent.csv)) and added to the '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.


#### Data Wrangling Final Conclusions

*Now that the Data is properly modeled, what's the conclusion? Did the Data Wrangling processes worth it?*

The [DataWranglingFinalConclusions](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/DataWranglingFinalConclusions.py) describes the files' sizes and shapes. 

Concerning the Airbnb Datasets, the size decreased sensibily (the modeled data has 0,02% of the raw data's size). Instead of 4 datasets - with varioues numbers of registers - now there's just one condensed dataset. Its number of column increased (the original dataset with the largest number of columns has 37 while the modeled has 174) but it's necessary in order to use categorical values on a machine learning model.

The VivaReals Dataset was turned into two separate files, but the modeled's data size represents 26% of the original and its number of columns also increased.

The biggest lose of information is related to the date values on the *Price_AV_Itapema.zip*. The original file has registers from different properties on different dates and for this specific kind of analysis (behaviour of the prices over the time) the modeled data would not be very useful.


### Part 2 - Data Analysis and Business Inteligence

Once the Data is modeled, the focus is on solving the problems presented on the [case description](https://github.com/Andrercouto/SeazoneCase/blob/main/references/seazone_code_challenge.pdf).

#### Problem 1

*What is the best property profile to invest in the city?"*

The resolution, using Modeled_Airbnb_Data.csv is on [code].

The first part of the problem is defining the concepts of '*best*' and '*profile*'.  A the 'best investiments' will be defined by the average price of the property and the availability rate (cause a place being is always available could indicate that the clients have no interest on renting it). The 'profile' was defined as the property type itself (House/Appartment/Loft/ etc).

Considering that Seazone is focused on short-stay vacation homes, properties that usually have more than a week for minimum staying days were be desconsidered.

Some properties considered 'Quarto inteiro em pousada', 'Espaço inteiro: bangalô' and 'Espaço inteiro: vila' are considerably more expensive for renting, and it could be a good investment.

Considering the most commom property types ('Espaço inteiro: apartamento', 'Espaço inteiro: casa', 'Espaço inteiro: condomínio') the availability rate is almost the same (about 65% available) and the average prices of these type of properties are:

 - 'Espaço inteiro: apartamento': R$676/day;

 - 'Espaço inteiro: casa': R$621/day;

 - 'Espaço inteiro: condomínio': R$730/day;

The house caracteristics that increases more the rental price is the number of rooms (bedrooms, bathrooms) and number of guests.