import pandas as pd

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"

def readByYearMonthBorough(year: int,month: int,borough: str):
    '''This func download the specified yellow taxi data set from TLC website.

    Parameters:
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    pandas.core.frame.DataFrame :Return the pandas df of @year, @month, @borough selected.
    '''

    #Check if month is tidy
    #Check if year is tidy
    #Check if borough is tidy

    #Format the url
    DATA_URL = URL  + str(year) + "-" + str(month).zfill(2) + ".parquet"

    #Download data of @month @year specified
    df = pd.read_parquet(DATA_URL)

    #Trasform the download
    df.drop(df[(df['PULocationID'] != borough)].index,inplace=True)
    
    return df