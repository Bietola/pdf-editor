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
def fill_weekdays(can, days, times_st_pos):
    # TODO: Param
    holidays = []

    # Do fill
    for i, day in enumerate(days):
        # Date
        can.drawString(50, times_st_pos - 25*i, day.strftime("%d/%m"))
        # Mattina entrata, uscita
        can.drawString(125, times_st_pos - 25*i, "9:00")
        can.drawString(175, times_st_pos - 25*i, "13:00")
        # Pomeriggio entrata, uscita
        can.drawString(225, times_st_pos - 25*i, "N/A")
        can.drawString(285, times_st_pos - 25*i, "N/A")
        # Descrizione attivit├á svolta
        can.drawString(350, times_st_pos - 25*i, "Sviluppo Skyflight")
        # Firma digitale (doesn't work...)
        #: can.drawInlineImage("./signature.jpg", 500, times_st_pos - 25*i - 13, 100, 30)
        #: can.drawImage("./signature.jpg", 575, times_st_pos - 25*i - 13, 100, 30)
        #: can.drawImage(fill_weekdays.signature, 575, times_st_pos - 25*i - 13, 100, 30)
        # Go to next day
        #: day += timedelta(days=1)
#: fill_weekdays.signature = ImageReader(io.BytesIO(Path('./signature.jpg').read_bytes()))

## Tail
def fill_tail(can, st_pos):
    can.drawString(60, st_pos, "14/03/23")

## Fill single page
def fill_page(page_n, days, times_st_pos, tail_st_pos, header=False):
    # Needed to write to pdf for some reason
    packet = io.BytesIO()

    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    if header: fill_header(can)
    fill_weekdays(can, days, times_st_pos)
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

    def weekdays(rng):
        return list(filter(
            lambda d: d.weekday() < 5 and d.day not in [],
            [date(2022, 11, i) for i in rng]
        ))

    # Fill pages
    output.add_page(page1_pdf.pages[0])
    output.add_page(fill_page(1, days=weekdays(range(14, 24)), times_st_pos=310, tail_st_pos=115, header=True))
    output.add_page(fill_page(2, days=weekdays(range(24, 31)), times_st_pos=425, tail_st_pos=105, header=False))
    # output.add_page(fill_page(3, days=weekdays(range(31, 32)), times_st_pos=425, tail_st_pos=145, header=False))

    # finally, write "output" to a real file
    outputStream = open(f"output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

main()
