from datetime import date
from typing import Any, List
from fpdf import FPDF
from app import crud
from sqlalchemy.orm import Session


def get_by_params(all_etudiant: any, titre: str) -> int:
    etdiant = []
    if titre == "Ensemble":
        return len(all_etudiant["L1"])
    else:
        print(all_etudiant["L1"])
        for un_etudiant in all_etudiant["L1"]:
            print(un_etudiant.bacc_serie)
            if un_etudiant.bacc_serie == titre:
                etdiant.append(un_etudiant)
    return len(etdiant)


class PDF(FPDF):

    def add_title(pdf: FPDF, data: Any, niveau: str):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        pdf.image(image_univ, x=60, y=26, w=30, h=30)
        pdf.image(image_fac, x=210, y=26, w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTÉ DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        anne_etude = f"Année d'etude : {niveau}"
        titre = f"Renseignement sur le filiere et option au titre de l'année {data['annee']}"
        tabulation: int = 80
        ln: int = 1

        pdf.set_font("arial", "B", 18)
        pdf.cell(15, 20, txt="", ln=1)
        pdf.cell(0, 10, txt=titre4, ln=1, align="C")

        pdf.set_font("arial", "B", 16)
        pdf.cell(0, 10, txt=titre5, ln=1, align="C")

        pdf.cell(0, 18, txt="", ln=1, align="C")

        pdf.cell(tabulation, 6, txt="")
        pdf.set_font("arial", "BI", 12)
        pdf.cell(34, 6, txt=localisation, align="L")
        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 6, txt=localisation_, ln=1)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, txt="")
        pdf.cell(24, 6, txt=mention, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(70, 6, txt=mention_etudiant, ln=ln)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, txt="", align="L")
        pdf.cell(70, 6, txt=anne_etude, ln=ln)

        pdf.set_font("arial", "I", 12)
        pdf.cell(tabulation, 6, txt="", ln=1, align="L")
        pdf.cell(tabulation - 15, 6, txt="", align="L")
        pdf.cell(60, 6, txt=titre, ln=ln)

        pdf.cell(15, 10, txt="", ln=1, align="L")

    def create_stat_bachelier(data: Any, all_etudiant,bacc_serie):
        titre_stat = [{"name": "Nouveau Bachelier en : ",
                       "value": ["Serie A1", "Serie A2", "Serie C", "Serie D", "Technique \n Génie civile",
                                 "Technique Industrielle", "Technique Tertiaire",
                                 "Technique Agricole", "Technologique", "Autre", "Ensemble"]}]

        width: int = 285
        height: int = 10

        pdf = PDF("L", "mm", "a4")
        pdf.add_page()
        PDF.add_title(pdf=pdf, data=data, niveau="L1")
        pdf.set_font("arial", "BI", 8)
        pdf.set_left_margin(5)
        for index, titre in enumerate(titre_stat):
            pdf.cell(width, height, txt=f'{titre["name"]}{data["annee"]}', border=1, align="C")
        pdf.cell(0, height, txt="", ln=1)

        for titre in titre_stat:
            for index, value in enumerate(titre["value"]):
                if index < 4 or index > 8:
                    pdf.cell((width / len(titre["value"])) - 10, height, txt=value, border=1, align="C")
                elif index == 10:
                    pdf.cell((width / len(titre["value"])), height, txt=value, border=1, align="C")
                else:
                    pdf.cell((width / len(titre["value"])) + 12, height, txt=value, border=1, align="C")
            pdf.cell(0, height, txt="", ln=1, align="L")

        for titre in titre_stat:
            for index, value in enumerate(titre["value"]):
                response = get_by_params(all_etudiant, value)
                if index < 4 or index > 8:
                    pdf.cell((width / len(titre["value"])) - 10, height, txt=str(response), border=1, align="C")
                elif index == 10:
                    pdf.cell((width / len(titre["value"])), height, txt=str(response), border=1, align="C")
                else:
                    pdf.cell((width / len(titre["value"])) + 12, height, txt=str(response), border=1, align="C")
            pdf.cell(0, height, txt="", ln=1)

        bas_1 = "N.B: Veuillez remplir séparement le canevas par filière, type de formation et année d' études "

        pdf.set_font("arial", "BI", 12)
        pdf.cell(0, height, txt="", ln=1)
        pdf.cell(0, 5, txt=bas_1, ln=1, align="L")

        pdf.output(f"files/bachelier.pdf", "F")
        return f"files/bachelier.pdf"
