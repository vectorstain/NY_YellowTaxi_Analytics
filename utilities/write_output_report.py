from fpdf import FPDF
import pandas as pd
from .graph_data import graphPMTBoxplot, graphPMBoxplot, graphPMBarchart,graphFareAmountOverTripDistOverPgCountScatterplot, graphPgCountOverBoroughHeatmap
from utilities.clean_data import getCleanedDataFrame
from utilities.analyze_data import computeAverageFareAmountPerMile, computeAverageFareAmountPerMileInTime

class PDF(FPDF):
    def header(self):

        # Arial bold 15
        self.set_font('Arial', 'B', 15)

        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)

        # Calculate width of title and position
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)

        # Write Title
        self.cell(w, 9, self.title, 1, 1, 'C', 1)

        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def createPdfReport(df: pd.DataFrame, year:int, month:int, borough:str):
    # Instantiation of inherited class
    pdf = PDF()
    
    # Write the title
    pdf.set_title(f"Yellow Taxi Trip Report of {month}/{year} from {borough}")

    #Write the footer
    pdf.alias_nb_pages()

    # Insert Images
    PMT_boxplot_png_path = graphPMTBoxplot(df, year, month, borough)
    print(PMT_boxplot_png_path)

    PM_boxplot_png_path = graphPMBoxplot(df, year, month, borough)
    print(PM_boxplot_png_path)

    PM_barchart_png_path = graphPMBarchart(df, year, month, borough)
    print(PM_barchart_png_path)

    fare_amount_over_tripdist_over_pgcount_scatterplot_png_path = graphFareAmountOverTripDistOverPgCountScatterplot(df, year, month, borough)
    print(fare_amount_over_tripdist_over_pgcount_scatterplot_png_path)

    pg_count_over_borough_zone_heatmap_png_path = graphPgCountOverBoroughHeatmap(df, year, month, borough)
    print(pg_count_over_borough_zone_heatmap_png_path)

    # Report the analyzed of dataset
    PM_AVG,df = computeAverageFareAmountPerMile(df)
    print(f"The average PM is:{PM_AVG}")
    
    PMT_AVG,df=computeAverageFareAmountPerMileInTime(df)
    print(f"The average PMT is:{PMT_AVG}")

    # Insert descriptions

    # Save the report file
    pdf.output(f'./data/out/yt_report_of_{month}_{year}_from_{borough}.pdf', 'F')
