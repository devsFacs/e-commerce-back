from typing import Any
from app.pdf.PDFMark import PDFMark as FPDF
from .header import header
from ..utils import clear_name


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, sems: str, title: str):
        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        header(pdf)
        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        journey = "PARCOURS:"
        journey_etudiant = f"{data['journey']}"
        semester = "SEMESTRE:"
        semester_etudiant = f"{sems.upper()}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"

        pdf.set_font("alger", "", 22)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, mention_etudiant, 0, 1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(28, 8, txt=journey, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=journey_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(28, 8, txt=semester, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=semester_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

    def create_list_inscrit(sems: str, parcour: str, data: Any, etudiants: Any):
        pdf = PDF("P", "mm", "a4")
        pdf.watermark('Faculté des Sciences',  font_style='BI')
        pdf.add_page()
        titre = "LISTE DES ÉTUDIANTS INSCRITS"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre)

        num = "N°"
        nom_et_prenom = "Nom et prénom"

        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(25, 5, txt=num, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(163, 5, txt=nom_et_prenom, border=1, ln=0, align="C")
        num_ = 1
        for i, etudiant in enumerate(etudiants):
            num_select_ = etudiant["num_carte"]
            name = f"{clear_name(etudiant['last_name'])} {etudiant['first_name']}"
            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "I", 10)
            pdf.cell(1, 5, txt="")
            pdf.cell(25, 5, txt=num_select_, border=1, ln=0)
            pdf.cell(1, 5, txt="")
            pdf.set_font("arial", "I", 10)
            pdf.cell(163, 5, txt=name, border=1, ln=0, align="L")
            num_ += 1
        pdf.output(f"files/pdf/liste/list_inscit_{sems}_{parcour}_{data['anne']}.pdf", "F")
        return f"files/pdf/liste/list_inscit_{sems}_{parcour}_{data['anne']}.pdf"
