from typing import Any
from app.pdf.PDFMark import PDFMark as FPDF
from .header import header
from ..utils import clear_name


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, title: str):
        header(pdf)
        pdf.add_font("alger", "", "Algerian.ttf", uni=True)
        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"

        pdf.set_font("alger", "", 14)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=mention_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

    def create_list_select(mention: str, data: Any, etudiants: Any):
        niveau = ["L1", "M1", "M2"]
        pdf = PDF("P", "mm", "a4")

        for niv in niveau:
            if len(etudiants[niv]) != 0:
                titre = f"LISTE DES ÉTUDIANTS ADMIS PAR SÉLÉCTION DE DOSSIER EN {niv}"
                pdf.add_page()
                pdf.watermark('Faculté des Sciences',  font_style='BI')
                PDF.add_title(pdf=pdf, data=data, title=titre)

                num = "N°"
                nom_et_prenom = "Nom et prénom"

                pdf.cell(1, 7, txt="", ln=1)
                pdf.set_font("arial", "BI", 10)
                pdf.cell(1, 5, txt="")
                pdf.cell(25, 5, txt=num, border=1)
                pdf.cell(1, 5, txt="")
                pdf.cell(163, 5, txt=nom_et_prenom, border=1, ln=0, align="C")
                num_ = 1
                for i, etudiant in enumerate(etudiants[niv]):
                    num_select_ = etudiant["num_select"]
                    name = f"{clear_name(etudiant['last_name'])} {etudiant['first_name']}"
                    pdf.cell(1, 7, txt="", ln=1)
                    pdf.set_font("arial", "I", 10)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(25, 5, txt=num_select_, border=1, ln=0)
                    pdf.cell(1, 5, txt="")
                    pdf.set_font("arial", "I", 10)
                    pdf.cell(163, 5, txt=name, border=1, ln=0, align="L")
                    num_ += 1

        pdf.output(f"files/pdf/liste/list_select_{mention}.pdf", "F")
        return f"files/pdf/liste/list_select_{mention}.pdf"
