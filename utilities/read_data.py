import pandas as pd

YT_TRIP_DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"
TAXI_ZONE_LOOKUP_DATASET_URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

def readBoroughTripsByYearMonth(year: int,month: int,borough: str) -> pd.DataFrame:
    '''This func download the specified yellow taxi data set from TLC website.

    Parameters:
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    pandas.core.frame.DataFrame :Return the pandas df of @year, @month, @borough selected.
    '''

    zone_lookup_df=pd.read_csv(TAXI_ZONE_LOOKUP_DATASET_URL)

    #Check if month is tidy
    if (month<1 or month >13):
        raise ValueError("Month provided can't be less than 1 or greater than 12")
    #Check if year is tidy
    if (year<2009 or year>2022):
        raise ValueError("Year provided can't be less than 2009 or greater than 2022")
    #Check if borough is tidy
    if (borough not in zone_lookup_df["Borough"].unique()):
        raise ValueError("Borough provided {} is not valid, should be one of these: {}".format(borough,zone_lookup_df["Borough"].unique()))

    #Format the url
    DATA_URL = YT_TRIP_DATASET_URL  + str(year) + "-" + str(month).zfill(2) + ".parquet"

    #Download data of @month @year specified
    df = pd.read_parquet(DATA_URL)
    
    #Merged the two dataframes on PULocationID and DOLocationID
    df = pd.merge(df,zone_lookup_df[["LocationID","Borough","Zone"]],left_on="PULocationID",right_on="LocationID")
    df.rename(columns={"Borough":"PULocation"}, inplace=True)
    df.rename(columns={"Zone":"PULocationZone"}, inplace=True)
    df.drop('PULocationID', axis=1, inplace=True)
    df.drop('LocationID', axis=1, inplace=True)

    df = pd.merge(df,zone_lookup_df[["LocationID","Borough","Zone"]],left_on="DOLocationID",right_on="LocationID")
    df.rename(columns={"Borough":"DOLocation"}, inplace=True)
    df.rename(columns={"Zone":"DOLocationZone"}, inplace=True)
    df.drop('DOLocationID', axis=1, inplace=True)
    df.drop('LocationID', axis=1, inplace=True)

    #Drop records where PULocation is different than specified @borough
    df.drop(df[(df['PULocation'] != borough)].index,inplace=True)

    #Reindex the returned dataframe
    df = df.reset_index(drop=True)
    return df

def readUserInput() -> list:
    '''This func read the user input.

    Parameters:
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    list :Return a list of @year, @month, @borough .
    '''
    contition = False
    while  contition == False :
        default_year="2020"
        year = (input("Type the year number: ")  )

        print(year)
        print(type(year))
        
        if year and year.isdigit():
            if int(year) >=2010 and int(year) <=2022:
                condition = True
    
    default_month=1
    contition = False
    while not contition:
        default_month="1"
        month = (input("Type the month number): ") != "" or default_month )
        
        if month and month.isdigit():
            if int(month) >=1 and int(month) <=12:
                condition = True

    default_borough="Bronx"
    contition = False
    borough_list = ['EWR', 'Queens', 'Bronx', 'Manhattan', 'Staten Island', 'Brooklyn']
    while not contition:
        default_borough="Bronx"
        borough = (input("Type borough): ") != "" or default_borough )

        if borough in borough_list:
            condition = True
    
    return [year,month,borough]
            

