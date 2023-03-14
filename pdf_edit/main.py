from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from datetime import date, timedelta
from pathlib import Path

## Header
def fill_header(can):
    # Cognome e nome destinatario
    can.drawString(255, 414       , "Stefano Montesi")
    # Azienda ospitante
    can.drawString(255, 414 - 16, "TXT e-Tech")
    # Tutor aziendale
    can.drawString(255, 414 - 31, "Nicola Pietroleonardi")
    # Numero convenzione di riferimento
    #: can.drawString(255, 414 - 46, "???")

## Fill out weekdays
def fill_weekdays(can, month, year, times_st_pos, times_st, times_n):
    day = date(year, month, 1)
    # Go to `times_st`th weekday not counting weekends
    for i in range(times_st):
        day += timedelta(days=1)
        while day.weekday() > 4:
            day += timedelta(days=1)
    # Do fill
    for i in range(times_n):
        # Stop when month changes
        if day.month != month: return
        # Skip weekends
        while day.weekday() > 4: day += timedelta(days=1)
        # Date
        can.drawString(50, times_st_pos - 25*i, day.strftime("%d/%m"))
        # Mattina entrata, uscita
        can.drawString(125, times_st_pos - 25*i, "9:00")
        can.drawString(175, times_st_pos - 25*i, "13:00")
        # Pomeriggio entrata, uscita
        can.drawString(225, times_st_pos - 25*i, "N/A")
        can.drawString(285, times_st_pos - 25*i, "N/A")
        # Descrizione attività svolta
        can.drawString(350, times_st_pos - 25*i, "Sviluppo Skyflight")
        # Firma digitale (doesn't work...)
        #: can.drawInlineImage("./signature.jpg", 500, times_st_pos - 25*i - 13, 100, 30)
        #: can.drawImage("./signature.jpg", 575, times_st_pos - 25*i - 13, 100, 30)
        #: can.drawImage(fill_weekdays.signature, 575, times_st_pos - 25*i - 13, 100, 30)
        # Go to next day
        day += timedelta(days=1)
#: fill_weekdays.signature = ImageReader(io.BytesIO(Path('./signature.jpg').read_bytes()))

## Tail
def fill_tail(can, st_pos):
    can.drawString(60, st_pos, "14/03/23")

## Fill single page
def fill_page(page_n, times_st_pos, tail_st_pos, times_st, times_n, header=False):
    # Needed to write to pdf for some reason
    packet = io.BytesIO()

    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # Test
    #: can.drawInlineImage("./signature.jpg", 100, 100, 100-(.5*inch), (.316*inch))

    if header: fill_header(can)
    fill_weekdays(can, 2, 2023, times_st_pos, times_st, times_n)
    fill_tail(can, tail_st_pos)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[page_n]
    page.merge_page(new_pdf.pages[0])

    return page

# read your existing PDF
existing_pdf = PdfReader(open("input.pdf", "rb"))
output = PdfWriter()

output.add_page(existing_pdf.pages[0])
output.add_page(fill_page(1, times_st_pos=310, tail_st_pos=115, times_st=1, times_n= 8, header=True))
output.add_page(fill_page(2, times_st_pos=425, tail_st_pos=105, times_st=9, times_n=13, header=False))

# finally, write "output" to a real file
outputStream = open("output.pdf", "wb")
output.write(outputStream)
outputStream.close()
