# Local Utilities
from utilities.read_data import readBoroughTripsByYearMonth, readUserInput
from utilities.clean_data import getCleanedDataFrame
from utilities.analyze_data import computeAverageFareAmountPerMile, computeAverageFareAmountPerMileInTime
from utilities.write_output_report import createPdfReport


if __name__ == "__main__":

    # Get user input
    year,month,borough = readUserInput()

    # Read the dataset
    df = readBoroughTripsByYearMonth(year,month,borough)

    # Clean the dataset
    df = getCleanedDataFrame(df)

    # Analyzed the dataset
    PM_AVG,df = computeAverageFareAmountPerMile(df)
    print(f"The average PM is:{PM_AVG}")
    
    PMT_AVG,df=computeAverageFareAmountPerMileInTime(df)
    print(f"The average PMT is:{PMT_AVG}")

    # Print/Save report/analysis
    createPdfReport(df, year,month,borough, PM_AVG, PMT_AVG)