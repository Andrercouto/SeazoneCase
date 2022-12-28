# Case Seazone - Data Scientist

The actual repository encompasses a testing Case for a data scientist job opportunity at Seazone. The Case was designed for testing both the coding skills, logical thinking and analytical capabilities, and it's based on a work done at Seazone, with real data and it's divided in two parts. Its first part consists on treating (wrangling, enriching, modeling) the raw data, while the second part is based on getting insights from the modeled data in order to make better strategic decisions.

## Running the Aplication

### Basics Dependencies

 - The project was designed on Python 3.10.0 and some packages needed may be uncompatible to the later versions.

 - The necessary packages are on: [requirements.txt](https://github.com/Andrercouto/SeazoneCase/blob/main/requirements.txt).

 - The Datasets given on the Case's description were added on: [datasets](https://github.com/Andrercouto/SeazoneCase/tree/main/data). It's relevant to note that while the other files are on *.csv* format, the *Price_AV_Itapema*'s dataset is a compressed file and the reason is that it was too large (4GB) for Github's storage size.

### Installing

For running the aplication, the <code>virtualenv</code> library must be correctly installed. If it's not, just run:

<code>pip install virtualenv</code>

Clone the repository and install all the packages necessary:

<code>
```
git clone https://github.com/Andrercouto/SeazoneCase.git 
py -3.10 -m venv my_env 
source my_env\scripts\activate 
pip install -r requirements.txt
```
 </code>