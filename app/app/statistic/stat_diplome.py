from datetime import date
from typing import Any, List
from fpdf import FPDF
from app import crud


def get_by_params(sexe: str, all_etudiant: any, diplome: str) -> int:
    stat_etudiant = []
    for etudiant in all_etudiant:
        if sexe == "Total":
            if etudiant["diplome"] == diplome:
                stat_etudiant.append(etudiant)

        if sexe == "Total" and diplome == "Total":
            stat_etudiant.append(etudiant)
        if diplome == "Total":
            if etudiant["info"].sexe == sexe:
                stat_etudiant.append(etudiant)
        else:
            if etudiant["info"].sexe == sexe and etudiant["diplome"] == diplome:
                stat_etudiant.append(etudiant)
    return len(stat_etudiant)


class PDF(FPDF):

    def add_title(pdf: FPDF, data: Any):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        txt=pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        pdf.image(image_univ, x=30, y=26, w=30, h=30)
        pdf.image(image_fac, x=155, y=26, w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTE DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"

        tabulation: int = 35
        ln: int = 1

        pdf.set_font("arial", "B", 12)
        pdf.cell(15, 20, txt="", border=0, ln=1, align="L")
        pdf.cell(0, 6, txt=titre4, border=0, ln=1, align="C")

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 6, txt=titre5, border=0, ln=1, align="C")

        pdf.cell(0, 18, txt="", border=0, ln=1, align="C")

        pdf.cell(tabulation, 6, txt="", border=0, ln=0, align="L")
        pdf.set_font("arial", "BI", 12)
        pdf.cell(34, 6, txt=localisation, border=0, ln=0, align="L")
        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 6, txt=localisation_, border=0, ln=1)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, txt="", border=0, ln=0, align="L")
        pdf.cell(24, 6, txt=mention, border=0, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(70, 6, txt=mention_etudiant, ln=ln)

        pdf.cell(15, 10, txt="", border=0, ln=1, align="L")

    def create_statistic_by_diplome(data: Any, all_etudiant, schemas: str):
        titre_stat = [{"name": 'Sexe', "value": ["Sexe"]}, {"name": "Diplome", "value": ["Licence", "Master"]},
                      {"name": "Total", "value": ["Total"]}]

        width: int = 50
        height: int = 10

        pdf = PDF("P", "mm", "a4")

        sexe_ = ["MASCULIN", "FEMININ", "Total"]
        pdf.add_page()
        PDF.add_title(pdf=pdf, data=data)
        pdf.set_margin(30)
        pdf.set_font("arial", "BI", 10)
        for titre in titre_stat:
            if titre["name"] == "Sexe" or titre["name"] == "Total":
                pdf.cell(width, height * 2, txt=titre["name"], border=1, ln=0, align="C")
            else:
                pdf.cell(width, height, txt=titre["name"], border=1, ln=0, align="C")
        pdf.cell(0, height, txt="", border=0, ln=1, align="L")

        for titre in titre_stat:
            for value in titre["value"]:
                if titre["name"] == "Sexe" or titre["name"] == "Total":
                    pdf.cell(width / (len(titre["value"])), height, txt="", border=0, ln=0, align="C")
                else:
                    pdf.cell(width / (len(titre["value"])), height, txt=value, border=1, ln=0, align="C")
        pdf.cell(0, height, txt="", border=0, ln=1, align="L")

        for sexe in sexe_:
            for index_1, titre in enumerate(titre_stat):
                for value in titre["value"]:
                    pdf.set_font("arial", "BI", 10)
                    response = get_by_params(sexe, all_etudiant, value)
                    if index_1 == 0:
                        pdf.cell(width / (len(titre["value"])), height, txt=sexe, border=1, ln=0, align="C")
                    else:
                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1, ln=0, align="C")

            pdf.cell(0, height, txt="", border=0, ln=1, align="L")

        pdf.output(f"files/statistic_by_diplome.pdf", "F")
        return f"files/statistic_by_diplome.pdf"
