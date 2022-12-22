import pandas as pd

def computeAverageFareAmountPerMile(df: pd.DataFrame) -> float:
    '''This func download the specified yellow taxi data set from TLC website.

    Parameters:
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    pandas.core.frame.DataFrame :Return the pandas df of @year, @month, @borough selected.
    '''

    #Lets compute
    df["PM"]=pd.Series({}, dtype='float64')
    df["PM"]=df.apply(lambda x: x["fare_amount"]/x["trip_distance"], axis=1)

    AVG = df["PM"].mean()

    return AVG

def computeAverageFareAmountPerMileInTime(df: pd.DataFrame) -> float:
    '''This func download the specified yellow taxi data set from TLC website.

    Parameters:
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    pandas.core.frame.DataFrame :Return the pandas df of @year, @month, @borough selected.
    '''

    #Lets compute
    df["PMT"]=pd.Series({}, dtype='float64')
    df["PMT"]=df.apply(lambda x: (x["fare_amount"]/x["trip_distance"])/(x["tpep_dropoff_datetime"]-x["tpep_pickup_datetime"]), axis=1)

    AVG = df["PMT"].mean()

    return AVG