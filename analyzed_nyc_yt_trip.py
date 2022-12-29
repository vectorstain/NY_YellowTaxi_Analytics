# Local Utilities
from utilities.read_data import readBoroughTripsByYearMonth, readUserInput
from utilities.clean_data import getCleanedDataFrame
#from utilities.analyze_data import computeAverageFareAmountPerMile, computeAverageFareAmountPerMileInTime
from utilities.write_output_report import createPdfReport
#from utilities.graph_data import graphPMTBoxplot, graphPMBoxplot, graphPMBarchart,graphFareAmountOverTripDistOverPgCountScatterplot, graphPgCountOverBoroughHeatmap


if __name__ == "__main__":

    # Get user input
    year,month,borough = readUserInput()

    # Read the dataset
    df = readBoroughTripsByYearMonth(year,month,borough)

    # Clean the dataset
    df = getCleanedDataFrame(df)

    # Print/Save report/analysis
    createPdfReport(df, year,month,borough)