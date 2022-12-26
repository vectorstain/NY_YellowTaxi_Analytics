import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def graphPMTBoxplot(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
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
    plt.figure()
    sns.barplot(data=df,x="DOLocation",y="PM")
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PM_barchart.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphPgCountOverBoroughHeatmap(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    pivot = pd.pivot_table(df, index='PULocationZone', columns='DOLocationZone', values='passenger_count', aggfunc=np.sum)
    plt.figure()
    sns.heatmap(pivot, annot=False, cmap="crest")
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PgCountOverBoroughHeatmap.png'
    plt.savefig(FILE_NAME,pad_inches=0.4, bbox_inches = 'tight')
    return FILE_NAME

def graphFareAmountOverTripDistOverPgCountScatterplot(df: pd.DataFrame, year:int, month: int, borough: str) -> str:
    plt.figure()
    g=sns.scatterplot(data=df, x="fare_amount", y="trip_distance", hue="passenger_count")
    plt.xlim(0, 500)
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_fare_amount_over_trip_distance_over_pg_count.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    
    return FILE_NAME