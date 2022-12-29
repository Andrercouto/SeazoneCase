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

Once the Repository has its Databases and the necessary dependencies configured, the first part of the Case can be started. It concerns Data Wrangling, which is process of transforming "Raw Data" into a more appropriate and valuable format (in this specific case, preferably a format that fits into a regression machine learning model), ensuring its quality and usefulness. In order to keep the modeled data a [new folder](https://github.com/Andrercouto/SeazoneCase/tree/main/modeled_data) was created.

Four of the five given Datasets were scrapped from *Airbnb*. The first questions would be: 

- *Do these differents datasets represent the same set of places/appartments?*

- *If they are, would be usefull - or even possible - to merge them into a condensed dataset, which would contain their most critical information? How could it be done?*

#### Check Airbnb Data

The [CheckAirbnbData.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/CheckAirbnbData.py) script (*which cointains comments specifying more clearly the steps taken on each line*) found out that **yes**, this Datasets are related to the same set of places, so, it could be usefull to join them.

Each one of the datasets will need to be treated in a different way in order to *condense* and *merge* them without losing important information. 

#### Wrangling *Details_Data.csv*

Once it's noticed that the Airbnb Databases contains information about the same location, the next steps will be treating them in a way that would be possible to consolidate their information in just **one** Dataset.

The [ModelingDetails.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/ModelingDetails.py) script's purpose was on modeling the [Details_Data.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/raw_data/Details_Data.csv) dataset (which contains the location's specificities, such as amenities, house rules, location type, rooms of the house), condensing it in order to keep just one register for each location. The qualitative technique was also treated (*vectorized*), and a modeled dataframe ([Modeled_Details_Data.csv](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_Details_Data.csv)) was added on the '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.

#### Wrangling *Price_AV_Itapema.zip*

Among the Datasets given, *Price_AV_Itapema.csv* was the biggest one (it even needed to be compressed for decreasing it's size) and the [ModelingPricess.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/ModelingPrices.py) script's purpose was summarizing a 40 milion registers Database in a modeled format that could be related with the others *Airbnb Datasets*. After excluding *NaN* values on critical columns, treating outliers, and creating usefull metrics a condensed *.csv* [file](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data/Modeled_Prices_Data.csv)) - where each register represents a location - was created and added to the '[modeled_data](https://github.com/Andrercouto/SeazoneCase/blob/main/modeled_data)' folder.

#### Joining Airbnb Data

At this moment, the most 