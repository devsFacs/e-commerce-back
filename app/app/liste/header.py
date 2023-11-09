
from app.pdf.PDFMark import PDFMark as FPDF


def header(pdf: FPDF):
    image_univ = "images/logo_univ.jpg"
    image_fac = "images/logo_science.jpg"

    titre4 = "UNIVERSITE DE FIANARANTSOA"
    titre5 = "FACULTE DES SCIENCES"

    title6 = "compus Universitaire Andrainjato BP:1264-301-Fianarantsoa"
    title7 = "email: facscience@gmail.com-Téléphone: 034 27 931 75 ou 034 46 620 41"

    pdf.add_font("alger", "", "Algerian.ttf", uni=True)

    pdf.image(image_univ, x=15, y=6, w=30, h=30)
    pdf.image(image_fac, x=170, y=6, w=30, h=30)

    pdf.set_font("arial", "", 10)
    pdf.cell(0, 6, txt=titre4, ln=1, align="C")
    pdf.cell(0, 6, txt=titre5, ln=1, align="C")
    pdf.set_font("arial", "", 8)
    pdf.cell(0, 5, txt=title6, ln=1, align="C")
    pdf.cell(0, 5, txt=title7, ln=1, align="C")
