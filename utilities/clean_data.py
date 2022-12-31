import pandas as pd
import random as r

TAXI_ZONE_LOOKUP_DATASET_URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"


def removeMessyRows(df: pd.DataFrame, trip_inference:bool) -> pd.DataFrame:
    '''This func removes messy rows in dataframe. 
    - Drops duplicated rows.
    - Drops rows where passenger_count is eq. to 0 or is NaN.
    - Drops rows where fare_amount is less then 0.
    - Drops rows where congestion_surcharge is less then 0.
    - Drops rows where trip_distance == 0 and trip duration is less 5 minuts.
    - Substitute rows where trip_distance eq. 0 with avg trip dist. of same trip.
    - If trip_inference is set to True drop rows where doesnt exist alternative trip.

    Parameters:
    pandas.Dataframe : The dataframe which you want to conduct prize per mile analysis.
    bool : trip_inference choose if you want to try to inference Unkown trips.

    Returns:
    pandas.DataFrame : Return the dataframe cleaned.
    '''

    number_of_rows = len(df.index)

    print(f"Starting with {number_of_rows} rows.")
    
    #Remove duplicates
    df.drop_duplicates(inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed duplicated rows: {number_of_rows} ")
    number_of_rows = len(df.index) 

    #Now let's remove from from the table the rows with the passenger_count == 0 or NaN (null)
    df.drop(df[(df['passenger_count'] == 0)|(df["passenger_count"].isna())].index,inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where passenger_count eq. 0 or NaN: {number_of_rows} ")
    number_of_rows = len(df.index) 

    #Now let's remove from from the table the rows with the fare_amount == 0 or NaN (null)
    df.drop(df.loc[df.fare_amount<=0].index, inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where fare_amount eq. 0 or NaN: {number_of_rows} ")
    number_of_rows = len(df.index) 

    #Now let's remove from from the table the rows with the congestion_surcharge is less than 0.
    df.drop(df.loc[df.congestion_surcharge<0].index, inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where congestion_surcharge is less than 0: {number_of_rows} ")
    number_of_rows = len(df.index) 

    #null_trip are rows where trip_distance == 0 and trip duration is under 5minuts
    null_trip = df.loc[(df['tpep_dropoff_datetime']-df['tpep_pickup_datetime']<300) & (df['trip_distance'] == 0)]
    df.drop(null_trip.index,inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where trip_distance eq. to 0 and trip time under 5 minuts: {number_of_rows} ")
    number_of_rows = len(df.index) 

    #Let's see districts with unique PULocation values
    PULdistrics = df["PULocationZone"].unique()
    DOLdistrics = df["DOLocationZone"].unique()

    #Let's create a dictionary with the values ​​of PULocation, DOLocation and Average trip
    dict_avg_trip = {
        "PUL" : [],
        "DOL" : [],
        "AVG_TRIP": [],
        "AVG_DUR_S": []
    }

    #Create a table with the information of PULocationID, DOLocationID and Average trip
    for i in range(len(PULdistrics)):
        for j in range(len(DOLdistrics)):
            PUL=PULdistrics[i]
            DOL=DOLdistrics[j]
            avg_trip_query = df.query("PULocationZone == @PUL and DOLocationZone == @DOL")
            avg_trip = avg_trip_query["trip_distance"].mean()
            dict_avg_trip["PUL"].append(PUL)
            dict_avg_trip["DOL"].append(DOL)
            dict_avg_trip["AVG_TRIP"].append(avg_trip)

            duration=0
            for k in avg_trip_query.index:
                duration = duration + (avg_trip_query["tpep_dropoff_datetime"][k]-avg_trip_query["tpep_pickup_datetime"][k])

            #print(PUL+"->"+DOL+": "+str(avg_duration))    
            avg_duration = duration/avg_trip_query.__len__() if avg_trip_query.__len__() != 0 else 0
            dict_avg_trip["AVG_DUR_S"].append(avg_duration)

    #Merged the two dataframes on PULocationID and DOLocationID
    avg_trip_df = pd.DataFrame(dict_avg_trip)
    zone_lookup_df=pd.read_csv(TAXI_ZONE_LOOKUP_DATASET_URL)
    avg_trip_df = pd.merge(avg_trip_df,zone_lookup_df[["Borough","Zone"]],left_on="PUL",right_on="Zone")
    avg_trip_df.rename(columns={"Borough":"PULBorough"}, inplace=True)
    avg_trip_df = pd.merge(avg_trip_df,zone_lookup_df[["Borough","Zone"]],left_on="DOL",right_on="Zone")
    avg_trip_df.rename(columns={"Borough":"DOLBorough"}, inplace=True)
    avg_trip_df.drop_duplicates(inplace=True)

    #Lets find others occurency where trip_distance is equal to 0s
    null_trip = df.loc[(df['trip_distance'] == 0)]

    #Let's take the null_trips considered above and replace the values ​​that have trip_distance == 0 or NaN with the AVG_TRIP of the route
    for i in null_trip.index.to_list():
        PULL=null_trip["PULocationZone"][i]
        DOL=null_trip["DOLocationZone"][i]
        AVG=avg_trip_df.loc[(avg_trip_df["PUL"]==PULL)&(avg_trip_df["DOL"]==DOL)]["AVG_TRIP"]

        if (AVG.any()):
            df.at[i,"trip_distance"] = AVG
        else:
            df.drop(i,inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where  trip_distance == 0 and doesnt exist an alternative trip: {number_of_rows} ")

    if trip_inference:
        df = replaceUnkownTripRecord(df,avg_trip_df)

    return df

def replaceUnkownTripRecord(df: pd.DataFrame, avg_trip_df: pd.DataFrame) -> pd.DataFrame:
    '''This func tries to guess trip PUL / DOL based on trip duration and trip distance. 
    - Drops rows where PUL/DOL location is equ. to NV or NaN.

    Parameters:
    pandas.Dataframe : The dataframe which you want to analyse.
    pandas.Dataframe : The dataframe containing avg miles and durations of trips.

    Returns:
    pandas.DataFrame : Return the dataframe cleaned with trip inference.
    '''

    number_of_rows = len(df.index) 

    avg_trip_df.drop(avg_trip_df.loc[(avg_trip_df["PUL"]=="NV")|(avg_trip_df["DOL"]=="NV")].index, inplace=True)
    avg_trip_df.drop(avg_trip_df.loc[(avg_trip_df["PUL"].isna())|(avg_trip_df["DOL"].isna())].index, inplace=True)
    
    number_of_rows -= len(df.index)
    print(f"Removed rows where PUL or DOL location is eq. to NV or NaN: {number_of_rows} ")
    number_of_rows = len(df.index) 
    
    #Lets check unkown trips
    unknow_trip = df.loc[(df['DOLocation'] == 'Unknown')|(df['PULocation'] == 'Unknown')|(df['PULocationZone'] == 'NV')|(df['PULocationZone'].isna())|(df['DOLocationZone'] == 'NV')|(df['DOLocationZone'].isna())]

    for i in unknow_trip.index:
        PUL = unknow_trip["PULocationZone"][i]
        DOL = unknow_trip["DOLocationZone"][i]
        T_DUR = (unknow_trip["tpep_dropoff_datetime"][i] - unknow_trip["tpep_pickup_datetime"][i])
        T_DIST = unknow_trip["trip_distance"][i]

        T_DUR_UPPERB=T_DUR+900
        T_DUR_LOWERB=T_DUR-900
        
        T_DIST_UPPERB=T_DIST+3
        T_DIST_LOWERB=T_DIST-3

        similar_trips = avg_trip_df.query("(PUL == @PUL or DOL == @DOL) or ((AVG_TRIP>@T_DIST_LOWERB and AVG_TRIP<@T_DIST_UPPERB) and (AVG_DUR_S>@T_DUR_LOWERB and AVG_DUR_S<@T_DUR_UPPERB))")

        if len(similar_trips.index)>0:
            rand_row_index = r.choice(similar_trips.index)
            df.at[i,"PULocationZone"] = similar_trips.at[rand_row_index,"PUL"]
            df.at[i,"DOLocationZone"] = similar_trips.at[rand_row_index,"DOL"]
            df.at[i,"PULocation"] = similar_trips.at[rand_row_index,"PULBorough"]
            df.at[i,"DOLocation"] = similar_trips.at[rand_row_index,"DOLBorough"]
        else:
            df.drop(i,inplace=True)

    number_of_rows -= len(df.index)
    print(f"Removed rows where Borough is Unknows. Now df has: {number_of_rows} ")

    return df


def fromDateTimeToTimestamp(df: pd.DataFrame) -> pd.DataFrame:
    '''This func trasform date-time fields to timestamp

    Parameters:
    pandas.Dataframe : The dataframe which you want to analyse.

    Returns:
    pandas.DataFrame : Return the dataframe with trasformed date-time fields to timestamp.
    '''

    #Lets change tpep_pickup_datetime  from  datetime64[ns] to int64
    df["tpep_pickup_datetime"] = df["tpep_pickup_datetime"].apply(lambda x: pd.Timestamp(x)).astype('int64')
    # Lets do the same form tpep_dropoff_datetime
    df["tpep_dropoff_datetime"] = df["tpep_dropoff_datetime"].apply(lambda x: pd.Timestamp(x)).astype('int64') 

    return df

def removeUselessCols(df: pd.DataFrame) -> pd.DataFrame:
    '''This func  remove messy colums for the analysis.
    - ['VendorID', 'RatecodeID', 'store_and_fwd_flag', 'extra', 'mta_tax','tip_amount','tolls_amount', 'improvement_surcharge', 'airport_fee']

    Parameters:
    pandas.Dataframe : The dataframe which you want to analyse.

    Returns:
    pandas.DataFrame : Return the dataframe without useles cols.
    '''
    
    # Remove useles cols
    df.drop(['VendorID', 'RatecodeID', 'store_and_fwd_flag', 'extra', 'mta_tax','tip_amount','tolls_amount', 'improvement_surcharge', 'airport_fee'], axis=1, inplace=True)

    return df

def getCleanedDataFrame(df: pd.DataFrame, trip_inference: bool) -> pd.DataFrame:
    '''This func clean and trasform the dataframe for to analysis.

    Parameters:
    pandas.Dataframe : The dataframe which you want to analyse.

    Returns:
    pandas.DataFrame : Return the dataframe trasformed.
    '''

    df = removeUselessCols(df)
    df = fromDateTimeToTimestamp(df)
    df = removeMessyRows(df,trip_inference)
    
    return df