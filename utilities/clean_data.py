import pandas as pd
import random as r

def removeMessyRows(df: pd.DataFrame) -> pd.DataFrame:
    
    #Remove duplicates
    df.drop_duplicates(inplace=True)

    #Now let's remove from from the table the rows with the passenger_count == 0 or NaN (null)
    df.drop(df[(df['passenger_count'] == 0)|(df["passenger_count"].isna())].index,inplace=True)

    #Now let's remove from from the table the rows with the fare_amount == 0 or NaN (null)
    df.drop(df.loc[df.fare_amount<=0].index, inplace=True)

    #Now let's remove from from the table the rows with the congestion_surcharge == 0 or NaN (null)
    df.drop(df.loc[df.congestion_surcharge<=0].index, inplace=True)

    #null_trip are rows where trip_distance == 0 and trip duration is under 10minuts
    null_trip = df.loc[(df['tpep_dropoff_datetime']-df['tpep_pickup_datetime']<600) & (df['trip_distance'] == 0)]
    #Now let's remove from from the table the rows with the passenger_count == 0 or NaN (null)
    df.drop(null_trip.index,inplace=True)

    #Let's see districts with unique PULocation values
    districs = df["PULocationZone"].unique()
    
    #Let's create a dictionary with the values ​​of PULocation, DOLocation and Average trip
    dict_avg_trip = {
        "PUL" : [],
        "DOL" : [],
        "AVG_TRIP": []
    }

    #Create a table with the information of PULocationID, DOLocationID and Average trip
    for i in range(len(districs)):
        for j in range(len(districs)):
            PUL=districs[i]
            DOL=districs[j]
            avg_trip = df.query("PULocationZone == @PUL and DOLocationZone == @DOL")["trip_distance"].mean()
            dict_avg_trip["PUL"].append(PUL)
            dict_avg_trip["DOL"].append(DOL)
            dict_avg_trip["AVG_TRIP"].append(avg_trip)

    avg_trip_df = pd.DataFrame(dict_avg_trip)

    #Lets find others accorency where trip_distance is equal to 0s
    null_trip = df.loc[(df['trip_distance'] == 0)]
    null_trip.reset_index()

    #Let's take the null_trips considered above and replace the values ​​that have trip_distance == 0 or NaN with the AVG_TRIP of the route
    for i in range(len(null_trip.index)):
        PULL=null_trip.iloc[i]["PULocationZone"]
        DOL=null_trip.iloc[i]["DOLocationZone"]
        INDEX=null_trip.index[i]
        AVG=avg_trip_df.loc[(avg_trip_df["PUL"]==PULL)&(avg_trip_df["DOL"]==DOL)]["AVG_TRIP"]
        df.at[INDEX,"trip_distance"] = AVG

    #Lets check unkown trips
    unknow_trip = df.loc[(df['DOLocation'] == 'Unknown')|(df['PULocation'] == 'Unknown')]
    avg_trip_df["AVG_DUR_S"] = 0

    # Lets compute avg trip duration for each PUL DOL combo
    for i in avg_trip_df.index:
        PUL=avg_trip_df["PUL"][i]
        DOL=avg_trip_df["DOL"][i]
        PUL_DOL_trips_df = df.query("PULocationZone == @PUL and DOLocationZone == @DOL")
        duration=0
        for j in PUL_DOL_trips_df.index:
            duration = duration + (PUL_DOL_trips_df["tpep_dropoff_datetime"][j]-PUL_DOL_trips_df["tpep_pickup_datetime"][j])

        #print(PUL+"->"+DOL+": "+str(avg_duration))    
        avg_duration = duration/PUL_DOL_trips_df.__len__() if PUL_DOL_trips_df.__len__() != 0 else 0
        avg_trip_df.at[i,"AVG_DUR_S"] = avg_duration

    avg_trip_df.drop(avg_trip_df.loc[(avg_trip_df["PUL"]=="NV")|(avg_trip_df["DOL"]=="NV")].index, inplace=True)
    avg_trip_df.drop(avg_trip_df.loc[(avg_trip_df["PUL"].isna())|(avg_trip_df["DOL"].isna())].index, inplace=True)


        
    dropped=0
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
            #print(PUL+"->"+DOL+": DIS "+str(T_DIST)+" U "+str(T_DIST_UPPERB)+" L "+str(T_DIST_LOWERB)+" D "+str(T_DUR)+" U "+str(T_DUR_UPPERB)+" L "+str(T_DUR_LOWERB))    
            rand_row_index = r.choice(similar_trips.index)
            df.at[i,"PULocationZone"] = similar_trips.at[rand_row_index,"PUL"]
            df.at[i,"DOLocationZone"] = similar_trips.at[rand_row_index,"DOL"]
        else:
            dropped=dropped+1
            df.drop(i,inplace=True)

    return df


def fromDateTimeToTimestamp(df: pd.DataFrame) -> pd.DataFrame:

    #Lets change tpep_pickup_datetime  from  datetime64[ns] to int64
    df["tpep_pickup_datetime"] = df["tpep_pickup_datetime"].apply(lambda x: pd.Timestamp(x)).astype('int64')
    # Lets do the same form tpep_dropoff_datetime
    df["tpep_dropoff_datetime"] = df["tpep_dropoff_datetime"].apply(lambda x: pd.Timestamp(x)).astype('int64') 

    return df

def removeUselessCols(df: pd.DataFrame) -> pd.DataFrame:
    
    # Remove useles cols
    df.drop(['VendorID', 'RatecodeID', 'store_and_fwd_flag', 'extra', 'mta_tax','tip_amount','tolls_amount', 'improvement_surcharge', 'airport_fee'], axis=1, inplace=True)

    return df

def getCleanedDataFrame(df: pd.DataFrame) -> pd.DataFrame:

    df = removeUselessCols(df)
    df = fromDateTimeToTimestamp(df)
    df = removeMessyRows(df)
    

    return df