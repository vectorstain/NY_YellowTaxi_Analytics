import pandas
import seaborn as sns
import matplotlib.pyplot as plt

def graphPMTBoxplot(df: pandas.DataFrame, year:int, month: int, borough: str) -> str:
    
    g = sns.catplot(
    data=df,
    x="PMT", y="PULocation", row="DOLocation",
    kind="box", orient="h",
    sharex=True, margin_titles=True
    )
    
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PMT_boxplot.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphPMBoxplot(df: pandas.DataFrame, year:int, month: int, borough: str) -> str:
    
    g = sns.catplot(
    data=df,
    x="PM", y="PULocation", row="DOLocation",
    kind="box", orient="h",
    sharex=False, margin_titles=True
    )
    
    FILE_NAME=f'./data/out/yt_of_{month}_{year}_from_{borough}_PM_boxplot.png'
    plt.savefig(FILE_NAME,pad_inches=0.4,
    bbox_inches = 'tight')
    return FILE_NAME

def graphBarchart(df: pandas.DataFrame) -> None:
    sns.barplot(data=df, x="passenger_count", y="fare_amount")
    plt.savefig('./data/out/'+'yt_districts_2020_01'+
    '_pgcount_fa_barchart.png',pad_inches=0.4,
    bbox_inches = 'tight')
    pass

def graphHeatmap(df: pandas.DataFrame) -> None:
    pass

def graphScatterplot(df: pandas.DataFrame) -> None:
    pass