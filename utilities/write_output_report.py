from fpdf import FPDF
import pandas as pd
from utilities.graph_data import graphPMTBoxplot, graphPMBoxplot, graphPMBarchart,graphFareAmountOverTripDistOverPgCountScatterplot, graphPgCountOverBoroughHeatmap
#from utilities.clean_data import getCleanedDataFrame
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

    #Page body
    def body(self, images:list, description:str):
        if len(images) == 1:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
            self.image(images[3], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
            self.image(images[4], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        
        self.cell(40, 10, "In this report we have included the average fare amount per mile and average fare amount per mile in time values ​​for the borough.\nAll of this was made visible by boxplots.")

    
def createPdfReport(df: pd.DataFrame, year:int, month:int, borough:str):

    # Instantiation of inherited class
    pdf = PDF()
    
    # Write the title
    pdf.set_title(f"Yellow Taxi Trip Report of {month}/{year} from {borough}")

    #Write the Author
    pdf.set_author('Vittorio Maria Calendra\n Eleonora Papa')

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
    description = 'In this report we have included the average fare amount per mile and average fare amount per mile in time values ​​for the borough.\nAll of this was made visible by boxplots.'
    print(description)
              

    # Save the report file
    pdf.output(f'./data/out/yt_report_of_{month}_{year}_from_{borough}.pdf', 'F')
