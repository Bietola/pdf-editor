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
    can.drawString(255, 414 - 46, "254/22")

## Fill out weekdays
def fill_weekdays(can, year, month, times_st_pos, times_st, times_n):
    # TODO: Param
    holidays = []

    day = date(year, month, 1)
    # Go to `times_st`th weekday not counting weekends
    while day.weekday() > 4:
        day += timedelta(days=1)
    for i in range(1, times_st):
        # TODO: Param
        if i in holidays: day += timedelta(days=1)
        day += timedelta(days=1)
        while day.weekday() > 4:
            day += timedelta(days=1)
    # Do fill
    i = 0
    while i < times_n:
        # Stop when month changes
        if day.month != month: break
        # Skip weekends
        while day.weekday() > 4: day += timedelta(days=1)
        # AC: Skip these days
        ## Epifania
        if day.day in holidays:
            day += timedelta(days=1)
            # NB. no `i` increment
            continue
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
        i += 1
#: fill_weekdays.signature = ImageReader(io.BytesIO(Path('./signature.jpg').read_bytes()))

## Tail
def fill_tail(can, st_pos):
    can.drawString(60, st_pos, "14/03/23")

## Fill single page
def fill_page(page_n, times_st_pos, tail_st_pos, times_st, times_n, year, month, header=False):
    # Needed to write to pdf for some reason
    packet = io.BytesIO()

    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    if header: fill_header(can)
    fill_weekdays(can, year, month, times_st_pos, times_st, times_n)
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
page1_pdf = PdfReader(open("page1.pdf", "rb"))
existing_pdf = PdfReader(open("input.pdf", "rb"))

def _fill_first_page(output):
    # Fill first page
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 24)
    can.drawString(400, 200, "Hello world")
    can.save()
    packet.seek(0)
    tmp_pdf = PdfReader(packet)
    page = page1_pdf.pages[0]
    page.merge_page(tmp_pdf.pages[0])
    output.add_page(page)

def main():
    output = PdfWriter()

    # Fill pages
    output.add_page(page1_pdf.pages[0])
    output.add_page(fill_page(1, times_st_pos=310, tail_st_pos=115, times_st= 14, times_n= 8, year=2022, month=11, header=True))
    output.add_page(fill_page(2, times_st_pos=425, tail_st_pos=105, times_st=  9, times_n=1, year=2022, month=11, header=False))
    # output.add_page(fill_page(3, times_st_pos=425, tail_st_pos=145, times_st=22, times_n=13, year=2023, month=2, header=False))

    # finally, write "output" to a real file
    outputStream = open(f"output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

main()
