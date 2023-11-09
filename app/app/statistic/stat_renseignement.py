from typing import Any
from fpdf import FPDF
from app import crud
from sqlalchemy.orm import Session


def get_by_params(all_etudiant: any, titre: str, niveau: str) -> int:
    etdiant = []
    if titre == "Nbr de demande reçue":
        return len(all_etudiant[niveau])
    else:
        for un_etudiant in all_etudiant[niveau]:
            if un_etudiant.select is True:
                etdiant.append(un_etudiant)
    return len(etdiant)


def create_stat_renseignement(data: Any, all_etudiant, db: Session, uuid_mention: str):
    titre_stat = [{"name": "Année d'etude", "value": ["Sexe"]},
                  {"name": "Admission en", "value": ["Nbr de demande reçue", "Nbr d'étudiants admis"]},
                  {"name": "Droit d'inscription (Ariary)", "value": ["Droit d'inscription (Ariary)"]}]

    width: int = 83
    height: int = 10

    niveau_ = ["L1", "M1", "M2"]
    pdf = PDF("P", "mm", "a4")
    for niv in niveau_:
        if len(all_etudiant[niv]) != 0:
            pdf.add_page()
            PDF.add_title(pdf=pdf, data=data, niveau=niv)
            pdf.set_font("arial", "BI", 9)
            for index, titre in enumerate(titre_stat):
                if index == 0 or index == 2:
                    pdf.cell(width - 30, height * 2, txt=titre["name"], border=1, ln=0, align="C")
                else:
                    pdf.cell(width, height, txt=f'{titre["name"]} {niv}', border=1, ln=0, align="C")
            pdf.cell(0, height, txt="", border=0, ln=1, align="L")

            for index, titre in enumerate(titre_stat):
                for value in titre["value"]:
                    if index == 0 or index == 2:
                        pdf.cell(width - 30, height, txt="", border=0, ln=0, align="C")
                    else:
                        pdf.cell(width / (len(titre["value"])), height, txt=value, border=1, ln=0, align="C")
            pdf.cell(0, height, txt="", border=0, ln=1, align="L")

            for index_1, titre in enumerate(titre_stat):
                for value in titre["value"]:
                    pdf.set_font("arial", "BI", 10)
                    response = get_by_params(all_etudiant, value, niv)
                    if index_1 == 0:
                        pdf.cell(width - 30, height, txt=niv, border=1, ln=0, align="C")
                    elif index_1 == 2:
                        droit = crud.droit.get_by_niveau_and_annee(db=db, niveau=niv, annee=data['annee'],
                                                                   uuid_mention=uuid_mention)
                        if droit:
                            pdf.cell(width - 30, height, txt=droit.droit, border=1, ln=0, align="C")
                        else:
                            pdf.cell(width - 30, height, txt="0", border=1, ln=0, align="C")
                    else:
                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1, ln=0, align="C")

            pdf.cell(0, height, txt="", border=0, ln=1, align="L")

    pdf.output(f"files/renseignement.pdf", "F")
    return f"files/renseignement.pdf"


class PDF(FPDF):

    def add_title(pdf: FPDF, data: Any, niveau: str):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        pdf.image(image_univ, x=30, y=26, w=30, h=30)
        pdf.image(image_fac, x=155, y=26, w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTÉ DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        anne_etude = f"Année d'etude : {niveau}"
        titre = f"Renseignement sur le filiere et option au titre de l'année {data['annee']}"
        tabulation: int = 35
        ln: int = 1

        pdf.set_font("arial", "B", 14)
        pdf.cell(15, 20, txt="", border=0, ln=1, align="L")
        pdf.cell(0, 6, txt=titre4, border=0, ln=1, align="C")

        pdf.set_font("arial", "B", 12)
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
        pdf.cell(70, 6, txt=mention_etudiant, border=0, ln=ln)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, txt="", border=0, ln=0, align="L")
        pdf.cell(70, 6, txt=anne_etude, border=0, ln=ln)

        pdf.set_font("arial", "I", 12)
        pdf.cell(tabulation, 6, txt="", border=0, ln=1, align="L")
        pdf.cell(tabulation - 15, 6, txt="", border=0, ln=0, align="L")
        pdf.cell(60, 6, txt=titre, border=0, ln=ln)

        pdf.cell(15, 10, txt="", border=0, ln=1, align="L")
