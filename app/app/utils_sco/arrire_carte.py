from fpdf import FPDF
from typing import Any
import qrcode
import os


class PDF(FPDF):
    def footer(self) -> None:
        self.set_y(-6)

    def create_carte(
        pdf: FPDF, pos_init_y: int, long_init_y: int, deux_et: list, data: Any
    ):

        image_fac = f"images/arriere.jpg"
        # logo_univ = "images/logo_univ.jpg"
        # logo_fac = "images/logo_science.jpg"

        titre_1 = "Faculté des Sciences \n"
        titre_1 += "Visites médicale \n"
        titre_1 += "medecine préventive \n"

        titre_2 = (
            f"Null ne se présenter à l'examen s'il n'a pas subi la visite médicale organisé par le Service de "
            f"la medecine préventive, "
        )

        titre_3 = "Signature du Medecin"

        titre_4 = (
            f"NB:il n'est délivrer qu'une seule carte pendant l'année, l'interessé(e) doit faire une "
            f"déclaration auprès de la police en cas de perte. "
        )

        titre_5 = "Université \n "
        titre_5 += "de \n"
        titre_5 += "Fianarantsoa"
        i: int = 0
        pos_init_x: int = 0.2
        long_init_x: int = 3.9
        absci: int = 1.25
        ordon: int = 0.06
        i = 0
        while i < len(deux_et):
            pdf.set_font("Times", "", 8)
            pdf.image(
                image_fac, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y
            )
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.set_text_color(0, 0, 0)

            pdf.set_font("Times", "B", 10)
            if i == 0:
                pdf.set_xy(absci - 0.35, pos_init_y + ordon)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 0.35, pos_init_y + ordon)

            pdf.multi_cell(
                2.5, 0.15, titre_1.upper(), border=0, ln=0, fill=False, align="C"
            )
            pdf.ln(0.1)

            pdf.set_font("Times", "I", 8.0)
            if i == 0:
                pdf.set_xy(absci - 1, pos_init_y + ordon + 0.6)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 1, pos_init_y + ordon + 0.6)
            pdf.multi_cell(1.8, 0.15, titre_2, 0, fill=0, align="C")

            if i == 0:
                pdf.set_xy(absci - 1, pos_init_y + ordon + 1.3)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 1, pos_init_y + ordon + 1.3)
            pdf.cell(1.8, 0.15, txt=titre_3, border=0, ln=0, align="C")

            pdf.set_font("Times", "B", 7.0)
            if i == 0:
                pdf.set_xy(absci + 1.88, pos_init_y + ordon + 0.8)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 1.88, pos_init_y + ordon + 0.8)
            pdf.multi_cell(1, 0.13, titre_5.upper(), 0, fill=0, align="C")

            pdf.set_font("Times", "I", 7.0)

            if i == 0:
                pdf.set_xy(absci - 1.05, pos_init_y + ordon + 2.1)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 1.05, pos_init_y + ordon + 2.1)
            pdf.multi_cell(2.9, 0.15, titre_4, 0, fill=0, align="L")

            pos_init_x = long_init_x + 0.3
            i = i + 1

    def boucle_carte(pdf: FPDF, huit_etudiant: Any, data: Any):
        pdf.add_page()
        pos_init_y: int = 0.2
        long_init_y: int = 2.6
        if len(huit_etudiant) % 2 == 0:
            nbr = len(huit_etudiant) // 2
        else:
            nbr = (len(huit_etudiant) // 2) + 1
        n = 0
        p: int = 0
        k = 0
        while n < nbr:
            PDF.create_carte(
                pdf, pos_init_y, long_init_y, huit_etudiant[p : p + 2], data
            )
            p += 2
            pos_init_y = pos_init_y + long_init_y + 0.1
            n += 1

        pdf.line(4.15, 0.2, 4.15, pos_init_y - 0.05)

    def parcourir_et(etudiant: list, data: Any):

        pdf = PDF("P", "in", "a4")
        nbr: int = 0
        if len(etudiant) % 8 == 0:
            nbr = len(etudiant) // 8
        else:
            nbr = (len(etudiant) // 8) + 1
        k: int = 0
        l: int = 0

        while k < nbr:
            PDF.boucle_carte(pdf, etudiant[l : l + 8], data)
            k += 1
            l += 8
        pdf.output(f"files/carte_{data['mention']}_arriere.pdf", "F")

        return f"files/carte_{data['mention']}_arriere.pdf"
