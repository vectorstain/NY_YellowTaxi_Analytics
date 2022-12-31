import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

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