# NY_YellowTaxi_Analytics
From data collected by NYC about taxi trips, we'll extract some useful analytics about the average cost of trips through several districts in the city of NY.

This project is developed by:
- Vincenzo Maria Calandra
- Eleonora Papa

under the supervision of Professor Guarrasi Valerio.

## What process generates this data?
The data used in the attached datasets were collected and provided to the NYC Taxi and Limousine Commission (TLC) by technology providers authorized under the Taxicab & Livery Passenger Enhancement Programs (TPEP/LPEP).

You can find the data set at this [link](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) 

## When was it created?
On a first analysis we are going to examinate data collects on January 2022, you can find the data set [here](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2020-01.parquet)


## Schema description
| Field Name            | Description                                                                                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| VendorID              | A code indicating the TPEP provider that provided the record.  1= Creative Mobile Technologies, LLC;  2= VeriFone Inc                                                                                                                                |
| tpep_pickup_datetime  | The date and time when the meter was engaged.                                                                                                                                                                                                        |
| tpep_dropoff_datetime | The date and time when the meter was disengaged.                                                                                                                                                                                                     |
| Passenger_count       | The number of passengers in the vehicle.                                                                                                                                                                                                             |
| Trip_distance         | The elapsed trip distance in miles reported by the taximeter.                                                                                                                                                                                        |
| PULocationID          | TLC Taxi Zone in which the taximeter was engaged                                                                                                                                                                                                     |
| DOLocationID          | TLC Taxi Zone in which the taximeter was disengaged                                                                                                                                                                                                  |
| RateCodeID            | The final rate code in effect at the end of the trip.  1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride                                                                                                        |
| Store_and_fwd_flag    | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server. Y= store and forward trip N= not a store and forward trip |
| Payment_type          | A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip                                                                                                              |
| Fare_amount           | The time-and-distance fare calculated by the meter.                                                                                                                                                                                                  |
| Extra                 | Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.                                                                                                                                 |
| MTA_tax               | $0.50 MTA tax that is automatically triggered based on the metered rate in use.                                                                                                                                                                      |
| Improvement_surcharge | $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.                                                                                                                                   |
| Tip_amount            | Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.                                                                                                                                                 |
| Tolls_amount          | Total amount of all tolls paid in trip.                                                                                                                                                                                                              |
| Total_amount          | The total amount charged to passengers. Does not include cash tips.                                                                                                                                                                                  |
| Congestion_Surcharge  | Total amount collected in trip for NYS congestion surcharge.                                                                                                                                                                                         |
| Airport_fee           | $1.25 for pick up only at LaGuardia and John F. Kennedy Airports                                                                                                                                                                                     |





## Project Genesis
These are some things to do at the genesis of your data analysis project
* Create a folder in your file system to hold all your files for the analysis
* Create a documents/spreadsheets to store the names, titles, contact information and notes of all the people connected to your project
* Find and introduce yourself to all the people connected to your project
* Connections to others is key to making your projects work. The more you are visible to others the more information will freely pass your way
* Be aware of all the people that are directly and indirectly connected to your project. Meet all of them
 * Stakeholders
 * Domain Experts
 * Other data scientists
 * Database admins - data engineers
 * Solutions architects
 * Project managers
 * Web developers
 
## Before Looking at Data
Once you have been given access to data, in a text document or Jupyter notebook answer the following questions:

* Is it generated from industrial equipment, a website, internal software?


* What systems use the data?
* Have their been previous data scientists working with this dataset?
* How has data changed over time? Which columns have been added/subtracted? 
* Is data for some columns not being collected?

## Subject Matter Research
* Read articles, watch videos, talk to local subject matter experts
* Read articles/papers by academics who have already studied the field using statistical analysis
* Could be beneficial to do some analysis first as to not bias your results

## First Look at Data
* Find data dictionary
* Even if one exists, create a column to keep track of notes for each variable
* Make sure your data dictionary has the column name, data type, range of values and notes on each column
* If the data comes from a relational database, ask to see the schema
* Number of rows and columns
* Find number of missing values per column

## Is the Data Tidy?
* Data must be tidy before analysis starts.
* Most data from relational databases will be tidy
* Data from spreadsheets or scraped from the web/pdfs might not be
* Find data type of each column - continuous, categorical (ordinal or nominal), or date
* Rearrange column order in a sensible manner - categorical first, continuous last. Group common variables together.

# Univariate vs Bivariate and Graphical vs Non-Graphical

| Univariate             | Graphical                               | Non-Graphical                     | 
|-------------|-----------------------------------------|-----------------------------------|
| Categorical | Bar char of frequencies (count/percent) | Contingency table (count/percent) |
| Continuous  | Histogram/rugplot/KDE, box/violin/swarm, qqplot, fat tails  | central tendency -mean/median/mode, spread - variance, std, skew, kurt, IQR  |

| Bivariate/multivariate            | Graphical                               | Non-Graphical                     | 
|-------------|-----------------------------------------|-----------------------------------|
| Categorical vs Categorical | heat map, mosaic plot | Two-way Contingency table (count/percent) |
| Continuous vs Continuous  | all pairwise scatterplots, kde, heatmaps |  all pairwise correlation/regression   |
| Categorical vs Continuous  | [bar, violin, swarm, point, strip seaborn plots](http://seaborn.pydata.org/tutorial/categorical.html)  | Summary statistics for each level |

## Univariate Analysis
* Look at one variable at a time.
### Categorical variables
* There is less available options with categorical variables
* Count the frequency of each variable
* Low frequency strings might be outliers
* You might want to relabel low frequency strings 'other'
* Find the number of unique labels for each column
* In pandas, change the data type to categorical (better when there aren't too many unique values)
* Bar plots of counts
* String columns allow for feature engineering by splitting the string, counting certain letters, finding the length of, etc... Feature engineering can be done later when modeling
### Continuous variables
* There are a lot more options for continuous variables
* Use the five number summary - with **`.describe`**
* Boxplots are great ways to find outliers
* Use histograms and kernel density estimators to visualize the distribution.
* Know the shape of the distribution
* Think about making categorical variables out of continuous variables by cutting them into bins.

### Use bootstrapping to get more 'samples'
* Bootstrapping is done by resampling your data with replacement and gives you a 'new' random dataset
* This helps you get multiple looks at the data
* You can get estimates for the mean and variance of continuous columns this way.

### Outliers in one dimension
* Use your natural human ability to look at boxplots to find thresholds for what an outlier might be
* Generate a new column of data that is 0/1 for outlier or not. This will quickly help you find them later.

### Duplicated data
* Lots of data gets accidentally duplicated. Check for duplicates or near duplicates of rows and columns
* If any columns are calculated entirely by that of another column or columns (like with depth from the diamonds data), ensure the calculation holds. 

### Making new binary columns to label some finding
* Just like it was described above to make a 0/1 column for outliers, you can do the same for any other finding
* You can drop the duplicated rows or you can make a binary column labeling them. 
* Same for rows that do not have a correct calculation.

## Bivariate and Multivariate EDA
### Categorical vs Categorical
* Create two way contingency table of frequency counts
* Create a heat map
* Find expected counts and possibly do a chi-squared test
### Categorical vs Continuous
* Use the seaborn categorical plots
### Continuous vs Continuous
* Plot all combinations of scatterplots
* Use a hierarchical clustering plot
