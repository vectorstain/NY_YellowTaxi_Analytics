import pandas as pd
import numpy as np

def computeAverageFareAmountPerMile(df: pd.DataFrame) -> list:
    '''This func compute the prize per mile for each row of the passed dataframe.

    Parameters:
    pandas.Dataframe : The dataframe which you want to conduct prize per mile analysis.

    Returns:
    float : Return the avg prize per mile
    pandas.DataFrame : Return the data frame with PM compute for each row
    '''

    #Lets compute
    df["PM"]=pd.Series({}, dtype='float64')
    df["PM"]=df.apply(lambda x: x["fare_amount"]/x["trip_distance"], axis=1)

    AVG = df["PM"].mean()

    return [float(AVG), df]

def computeAverageFareAmountPerMileInTime(df: pd.DataFrame) -> list:
    '''This func compute the prize per mile per time unit for each row of the passed dataframe.

    Parameters:
    pandas.Dataframe : The dataframe which you want to conduct prize per mile per time unit analysis.

    Returns:
    float : Return the avg prize per mile per time
    pandas.DataFrame : Return the data frame with PMT compute for each row
    '''

    #Lets compute
    df["PMT"]=pd.Series({}, dtype='float64')
    df["PMT"]=df.apply(lambda x: ((x["fare_amount"]/x["trip_distance"])/(x["tpep_dropoff_datetime"]-x["tpep_pickup_datetime"]))*1000000 if (x["tpep_dropoff_datetime"]-x["tpep_pickup_datetime"])>0 else np.NaN , axis=1)

    AVG = df["PMT"].mean()

    return [float(AVG), df]