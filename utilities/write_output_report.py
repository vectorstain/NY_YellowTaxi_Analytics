from fpdf import FPDF

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

def createPdfReport(year:int,month:int,borough:str):
    # Instantiation of inherited class
    pdf = PDF()
    
    # Write the title
    pdf.set_title(f"Yellow Taxi Trip Report of {month}/{year} from {borough}")

    #Write the footer
    pdf.alias_nb_pages()

    # Insert Images

    # Insert descriptions

    # Save the report file
    pdf.output(f'./data/out/yt_report_of_{month}_{year}_from_{borough}.pdf', 'F')
