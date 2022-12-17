# Local Utilities
from utilities.read_data import readBoroughTripsByYearMonth
from utilities.clean_data import getCleanedDataFrame

if __name__ == "__main__":

    # read user input
    year=2020
    month=1
    borough="Bronx"

    # Read the dataset
    df = readBoroughTripsByYearMonth(year,month,borough)

    # Clean the dataset
    df = getCleanedDataFrame(df)
    
    # Analyzed the dataset

    # Print/Save report/analysis