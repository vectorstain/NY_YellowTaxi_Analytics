from fpdf import FPDF
import pandas as pd
from utilities.graph_data import graphPMTBoxplot, graphPMBoxplot, graphPMBarchart,graphFareAmountOverTripDistOverPgCountScatterplot, graphPgCountOverBoroughHeatmap, graphPgOverBorough

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
    def first_pg_body(self, images:list, description:str):

        if len(images) == 5:
            self.add_page()
            self.image(images[0], x=10, y=20, w=40, type='PNG')
            self.image(images[1], x=50, y=20, w=40, type='PNG')
            self.set_font('Arial', '', 7)

            self.set_xy(90,30)
            txt='The boxplot on the left graph shows how changes trip prize per mile in time unit from a common start borough.\n'
            txt+='On the right boxplot instead we graph the general prize per mile from a common start borough.\n'
            txt+=description
            self.multi_cell( w = 110, h = 5, txt = txt, border = 1, align = 'J', fill = False)

            self.image(images[2], x=95, y=56, w=100, type='PNG')
            self.image(images[3], x=95, y=126, w=100, type='PNG')
            self.image(images[4], x=95, y=200, w=100, type='PNG')

    #Page body
    def second_pg_body(self, images:list, description:str):

        if len(images) > 0 :
            self.add_page()
            self.image(images[0], x=10, y=20, w=40, type='PNG')
            self.image(images[1], x=50, y=20, w=40, type='PNG')
            self.set_font('Arial', '', 7)

            self.set_xy(90,30)
            txt='This graph plot n of passeger moving from choosen borough to the others.\n'

            txt+=description

            self.multi_cell( w = 110, h = 5, txt = txt, border = 1, align = 'J', fill = False)

    
def createPdfReport(df: pd.DataFrame, year:int, month:int, borough:str, PM:float, PMT:float):
    '''This func graph passenger count over boroughs in the nyc borough map.

    Parameters:
    pd (pandas.core.frame.DataFrame) : The pandas df of @year, @month, @borough selected.
    year (int): The year you would analyzed, e.g. 2020 2021 2022.
    month (int): The n. th. month you would analyzed, e.g. 1 for Jen, 2 for Feb, 3 for May.
    borough (str): The borough you would analyzed, e.g. Manhattan, Bronx.
    PM (float): The avg PM computed.
    PMT (float): The avg PMT computed.
    '''

    # Instantiation of inherited class
    pdf = PDF()
    
    # Write the title
    pdf.set_title(f"Yellow Taxi Trip Report of {month}/{year} from {borough}")

    #Write the Author
    pdf.set_author('Vincenzo Maria Calandra\n Eleonora Papa')

    #Write the footer
    pdf.alias_nb_pages()

    # Generate graph
    PMT_boxplot_png_path = graphPMTBoxplot(df, year, month, borough)
    PM_boxplot_png_path = graphPMBoxplot(df, year, month, borough)
    PM_barchart_png_path = graphPMBarchart(df, year, month, borough)
    fare_amount_over_tripdist_over_pgcount_scatterplot_png_path = graphFareAmountOverTripDistOverPgCountScatterplot(df, year, month, borough)
    pg_count_over_borough_zone_heatmap_png_path = graphPgCountOverBoroughHeatmap(df, year, month, borough)
    pg_count_over_borough_map_png_path = graphPgOverBorough(df, year, month, borough)

    # Insert descriptions
    description = f'The average prize per mile from {borough}\'s borough is: {PM};\nThe average prize per mile in time unit from {borough}\'s borough is: {PMT}\n'

    pdf.first_pg_body([PMT_boxplot_png_path,PM_boxplot_png_path,PM_barchart_png_path,fare_amount_over_tripdist_over_pgcount_scatterplot_png_path,pg_count_over_borough_zone_heatmap_png_path],description)
    pdf.second_pg_body([pg_count_over_borough_map_png_path],"")

    # Save the report file
    pdf.output(f'./data/out/yt_report_of_{month}_{year}_from_{borough}.pdf', 'F')
