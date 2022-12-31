import pandas as pd
import geopandas as gp
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# import background package
import contextily as ctx

def graphPMTBoxplot(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph the PMT value boxplot.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''
    plt.figure()
    g = sns.catplot(
    data=df,
    x="PMT", y="PULocation", row="DOLocation",
    kind="box", orient="h",
    sharex=False, margin_titles=True
    )
    g.set(autoscalex_on=True)
    
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PMT_boxplot.png'
    g.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphPMBoxplot(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph the PM value boxplot.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''

    plt.figure()
    g = sns.catplot(
    data=df,
    x="PM", y="PULocation", row="DOLocation",
    kind="box", orient="h",
    sharex=False, margin_titles=True
    )
    g.set(autoscalex_on=True)
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PM_boxplot.png'
    g.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphPMBarchart(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph the PM value barchart.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''

    plt.figure()
    sns.barplot(data=df,x="DOLocation",y="PM")
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PM_barchart.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphPgCountOverBoroughHeatmap(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph the passengers value of trips between nyc districs via heatmap.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''

    pivot = pd.pivot_table(df, index='PULocationZone', columns='DOLocationZone', values='passenger_count', aggfunc=np.sum)
    plt.figure()
    sns.heatmap(pivot, annot=False, cmap="crest")
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PgCountOverBoroughHeatmap.png'
    plt.savefig(FILE_NAME,pad_inches=0.4, bbox_inches = 'tight')
    return FILE_NAME

def graphFareAmountOverTripDistOverPgCountScatterplot(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph the fare_amount value over trip distance and n. of passengers via scatterplot.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''

    plt.figure()
    g=sns.scatterplot(data=df, x="fare_amount", y="trip_distance", hue="passenger_count")
    plt.xlim(0, 500)
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_fare_amount_over_trip_distance_over_pg_count.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    
    return FILE_NAME

def graphPgOverBorough(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    '''This func graph passenger count over boroughs.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

    Returns:
    (str): The generated graph file path.
    '''

    nyc_pul_pa_df=pd.DataFrame()
    # Set boroughs names
    nyc_pul_pa_df['BoroName']=['Brooklyn','Bronx','Manhattan','Queens','Staten Island']

    # Set boroughs labels position
    nyc_pul_pa_df['longitude']=[985000,1000000,970000 ,1040000,925000]
    nyc_pul_pa_df['latitude']=[180000,250000,220000,200000,150000]

    # Compute n of passengers took yt in each boroughs
    boroughs = nyc_pul_pa_df["BoroName"].unique()
    index = 0
    for borought in boroughs:
        nyc_pul_pa_df.at[index, "pa_count"] = df.loc[df["DOLocation"]==borought]["passenger_count"].sum()
        index=index+1
    
    # load the data from geopandas.datasets
    nyc_shp = gp.read_file(gp.datasets.get_path('nybb'))

    # merge con_fa_nyc and nyc_shp
    nyc_shp=nyc_shp.merge(nyc_pul_pa_df,on='BoroName')

    plt.figure()
    
    # plot new york city 
    ax = nyc_shp.plot(column='pa_count',figsize=(10, 10), alpha=0.5, edgecolor='k', cmap='Reds',legend=True,scheme="quantiles")

    # add boroughs' names with numbers of passangers 
    for i in range(len(nyc_shp)):
        plt.text(nyc_shp.longitude[i],nyc_shp.latitude[i],"{}\nN. of people that took yellow taxi: {}".format(nyc_shp.BoroName[i],nyc_shp.pa_count[i],size=13))

    # Add title
    plt.title('NCY Yellow taxi passengers count',fontsize=25)

    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1.35,1))
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_pg_count.png'
    plt.savefig(FILE_NAME)
    
    return FILE_NAME

# def graphPgOverBorough(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
#     '''This func graph passenger count over boroughs.

#     Parameters:
#     pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
#     year (int): The year you would analyzed, e.g. 2020 2021 2022.
#     month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
#     borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.

#     Returns:
#     (str): The generated graph file path.
#     '''

#     ny_zone_df = gp.read_file("data/raw/nyu_2451_34566.shp")
#     ny_df = pd.read_csv("data/raw/nyc_zone_lookup.csv")
#     ny_df = pd.merge(ny_df, ny_zone_df, left_on="LocationID",right_on="BoroCD")
#     df = pd.merge(df, ny_df, left_on="DOLocationZone",right_on="Zone")

#     nyc_pul_pa_df = pd.DataFrame()
#     print(ny_df["Zone"].unique().tolist())
#     nyc_pul_pa_df['BoroName']=(ny_df["Zone"].unique().tolist())


#     # Compute n of passengers took yt in each boroughs
#     boroughs = ny_df["Zone"].unique()
#     index = 0
#     for borought in boroughs:
#         nyc_pul_pa_df.at[index, "pa_count"] = df.loc[df["DOLocationZone"]==borought]["passenger_count"].sum()
#         index=index+1

#     # merge con_fa_nyc and nyc_shp
#     nyc_shp=nyc_shp.merge(nyc_pul_pa_df,on='BoroName')

#     plt.figure()
    
#     #Convert the data to Web Mercator
#     nyc_shp = nyc_shp.to_crs(epsg=3857)
#     ax = nyc_shp.plot(column='pa_count',figsize=(10, 10), alpha=0.5, edgecolor='k', cmap='Reds',legend=True,scheme="quantiles")

#     #Add background tiles to plot
#     ctx.add_basemap(ax)
#     FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_pg_count.png'
#     plt.savefig(FILE_NAME)
    
#     return FILE_NAME