# Case Seazone - Data Scientist

The actual repository encompasses a testing Case for a data scientist job opportunity at Seazone. The Case was designed for testing both the coding skills, logical thinking and analytical capabilities, and it's based on a work done at Seazone, with real data and it's divided in two parts. Its first part consists on treating (wrangling, enriching, modeling) the raw data, while the second part is based on getting insights from the modeled data in order to make better strategic decisions.

## Configuring the Environment

### Basics Dependencies

 - The project was designed on Python 3.10.0 and some packages needed may be uncompatible to the later versions.

 - The necessary packages are on: [requirements.txt](https://github.com/Andrercouto/SeazoneCase/blob/main/requirements.txt).

 - The Datasets given on the Case's description were added on: [datasets](https://github.com/Andrercouto/SeazoneCase/tree/main/data). It's relevant to note that while the other files are on *.csv* format, the *Price_AV_Itapema*'s dataset is a compressed file and the reason is that it was too large (4GB) for Github's storage size.

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

Once the Repository has its Databases and the necessary dependencies configured, the first part of the Case can be started. It concerns Data Wrangling, which is process of transforming "Raw Data" into a more appropriate and valuable format, ensuring its quality and usefulness. In order to keep the modeled data a [new folder](https://github.com/Andrercouto/SeazoneCase/tree/main/modeled_data) was created.

On the case, for example, four of the five given Datasets were scrapped from *Airbnb*. The first questions would be: 

- *Are these differents datasets corcening the same set of places/appartments?*

- *If they are, would be usefull to merge them? In which way?*

The [DataWranglingAirbnb.py](https://github.com/Andrercouto/SeazoneCase/blob/main/Scripts/DataWrangling/DataWranglingAirbnb.py) (*the script has comments specifying what exactly was done on each line*) found out that **yes** this Datasets are related to the same set of places, so, it could be usefull to join them, and each one of them will need to be treated in a different way in order to *condense* and *merge* them without losing important information. 

