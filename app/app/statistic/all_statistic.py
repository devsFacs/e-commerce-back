from datetime import date
from typing import Any
from fpdf import FPDF
from app import crud
from sqlalchemy.orm import Session

from app.liste import header


def get_nbr_etudiant(db: Session, schemas: str, niveau: str, etat: str, sexe: str, uuid_journey: str) -> str:
    if etat == 'N':
        etat = "Passant"
    elif etat == "R":
        etat = "Redoublant"
    elif etat == "T+":
        etat = "Triplant ou plus"

    if niveau == "L1":
        niveau = "S2"
    elif niveau == "L2":
        niveau = "S4"
    elif niveau == "L3":
        niveau = "S6"
    elif niveau == "M1":
        niveau = "S8"
    else:
        niveau = "S10"

    all_student = []
    if etat != "M" and etat != "F" and etat != "Total":
        all_student = crud.ancien_student.get_for_stat(db=db, uuid_journey=uuid_journey, semester=niveau, sex=sexe,
                                                       type=etat.upper(), college_year=schemas)
    elif etat == "M":
        all_student = crud.ancien_student.get_by_sex_for_stat(db=db,
                                                               college_year=schemas,
                                                               uuid_journey=uuid_journey,
                                                               semester=niveau,
                                                               sex="MASCULIN")

    elif etat == "F":
        all_student = crud.ancien_student.get_by_sex_for_stat(db=db,
                                                                college_year=schemas,
                                                                uuid_journey=uuid_journey,
                                                                semester=niveau,
                                                                sex="FEMININ")

    elif etat == "Total":
        all_student = crud.ancien_student.get_by_journey_for_stat(db=db,
                                                                   college_year=schemas,
                                                                   uuid_journey=uuid_journey,
                                                                   semester=niveau)

    return len(all_student)


def get_by_params(all_niveau: Any, sexe: str, etat: str, age_: int) -> int:
    if etat == "R":
        etat = "Redoublant"
    elif etat == "T+":
        etat = "Triplant ou plus"
    elif etat == "N":
        etat = "Passant"
    now = date.today().year
    all_etudiant = []
    for etudiant in all_niveau:
        date_ = etudiant.date_naiss
        naiss = date_[0:4]
        age: int = int(now) - int(naiss)
        if sexe == "ENSEMBLE":
            if etat == "Total":
                if age_ == 15:
                    if age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    all_etudiant.append(etudiant)
                else:
                    if age == age_:
                        all_etudiant.append(etudiant)
            else:
                if age_ == 15:
                    if etudiant.etat == etat and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.etat == etat and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.etat == etat:
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.etat == etat and age == age_:
                        all_etudiant.append(etudiant)
        else:
            if etat == "S/Tot":
                if age_ == 15:
                    if etudiant.sexe == sexe and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.sexe == sexe and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.sexe == sexe:
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.sexe == sexe and age == age_:
                        all_etudiant.append(etudiant)
            else:
                if age_ == 15:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.sexe == sexe and etudiant.etat == etat:
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age == age_:
                        all_etudiant.append(etudiant)
    return len(all_etudiant)


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, type: str = "total"):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)
        header(pdf)

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        titre_1 = "Etudiants inscritent par filiere et option au titre de l'année"
        anne_univ = f"{data['anne']}"

        tabulation: int = 35
        ln: int = 1
        if type != "total":
            pdf.rect(195, 47.5, 5, 3)
            pdf.rect(195, 53.5, 5, 3)
            type_formation = "Type de Formation*:"
            cocher = "(Veuillez cochez)"
            type_1 = "Formation initial"
            type_2 = "Formation continue"
            anne_ = "Année d'etude :"
            anne_etude = f'{data["niveau"]} {data["journey"]}'
            ln = 0
            tabulation = 10


        pdf.cell(0, 18, txt="", ln=1, align="C")

        pdf.cell(tabulation, 6, txt="")
        pdf.set_font("arial", "BI", 12)
        pdf.cell(34, 6, txt=localisation, align="L")
        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 6, txt=localisation_, ln=1)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, txt="")
        pdf.cell(24, 6, txt=mention)

        pdf.set_font("arial", "I", 12)
        pdf.cell(70, 6, txt=mention_etudiant, ln=ln)

        if type != "total":
            pdf.cell(40, 6, txt=type_formation, ln=ln)
            pdf.cell(0, 6, txt=type_1, ln=1)

        if type != "total":
            pdf.cell(tabulation, 6, txt="")
            pdf.cell(30, 6, txt=anne_, ln=ln)
            pdf.cell(65, 6, txt=anne_etude, ln=ln)
            pdf.cell(38, 6, txt=cocher, ln=ln)
            pdf.cell(0, 6, txt=type_2, ln=1)

        else:
            pdf.cell(20, 6, txt="")
            pdf.cell(107, 6, txt=titre_1)
            pdf.cell(0, 6, txt=anne_univ, ln=ln)

        pdf.cell(15, 10, txt="", ln=1)

    def create_all_statistic(db: Session, data: Any, etudiant: Any, schemas: str):
        titre_stat = [{"name": '', "value": ["Niveau", "journey"]}, {"name": "masculin", "value": ["N", "R", "T+"]},
                      {"name": "feminin", "value": ["N", "R", "T+"]},
                      {"name": "ensemble", "value": ["M", "F", "Total"]}]

        niveau_ = ["L1", "L2", "L3", "M1", "M2", "H"]

        width: int = 39
        height: int = 7

        pdf = PDF("P", "mm", "a4")
        pdf.add_page()
        PDF.add_title(pdf=pdf, data=data, type="total")
        pdf.set_margin(20)
        for titre in titre_stat:
            if titre["name"] != '':
                pdf.set_font("arial", "BI", 10)
                pdf.cell(width, height, txt=titre["name"].upper(), border=1, align="C")
            else:
                pdf.cell(width, height, txt="")
        pdf.cell(0, height, txt="", ln=1)

        for titre in titre_stat:
            for value in titre["value"]:
                pdf.set_font("arial", "BI", 10)
                pdf.cell(width / (len(titre["value"])), height, txt=value, border=1, ln=0, align="C")
        pdf.cell(0, height, txt="", ln=1)

        pdf.cell(0, 1, txt="", ln=1)
        for index, journey in enumerate(etudiant):
            for index_1, titre in enumerate(titre_stat):
                for index_2, value in enumerate(titre["value"]):
                    if index_1 == 0:
                        if index_2 == 0:
                            if index == len(etudiant) - 1:

                                pdf.cell(width / (len(titre["value"])), height * len(journey[niveau_[index]]), txt="",
                                         border=1, align='C')
                            else:
                                pdf.cell(width / (len(titre["value"])), height * len(journey[niveau_[index]]),
                                         txt=niveau_[index], border=1, align='C')
                        elif index_2 == 1:
                            for index_3, parc in enumerate(journey[niveau_[index]]):
                                if index_3 == 0:
                                    pdf.cell(width / (len(titre["value"])), height, txt=parc["name"], border=1,
                                             align="C")
                                    for index_4, titre_1 in enumerate(titre_stat):
                                        if index_4 != 0:
                                            for value in titre_1["value"]:
                                                pdf.set_font("arial", "BI", 10)
                                                if index == len(etudiant) - 1:
                                                    pdf.cell(width / (len(titre_1["value"])), height, txt=str(0),
                                                             border=1, align='C')
                                                else:
                                                    value_stat = get_nbr_etudiant(db, schemas, niveau_[index], value,
                                                                                  titre_1["name"].upper(),
                                                                                  str(parc["uuid"]))
                                                    pdf.cell(width / (len(titre_1["value"])), height,
                                                             txt=str(value_stat),
                                                             border=1, align='C')
                                    pdf.cell(0, height, txt="", ln=1)
                                else:
                                    pdf.cell(width / (len(titre["value"])), height, txt='')
                                    pdf.cell(width / (len(titre["value"])), height, txt=parc["name"], border=1,
                                             align='C')
                                    for index_4, titre_1 in enumerate(titre_stat):
                                        if index_4 != 0:
                                            for value in titre_1["value"]:
                                                pdf.set_font("arial", "BI", 10)
                                                if index == len(etudiant) - 1:
                                                    pdf.cell(width / (len(titre_1["value"])), height, txt=str(0),
                                                             border=1, align="C")
                                                else:
                                                    value_stat = get_nbr_etudiant(db, schemas, niveau_[index], value,
                                                                                  titre_1["name"].upper(),
                                                                                  str(parc["uuid"]))
                                                    pdf.cell(width / (len(titre_1["value"])), height,
                                                             txt=str(value_stat),
                                                             border=1, align="C")
                                    pdf.cell(0, height, txt="", ln=1)
            pdf.cell(0, 1, txt="", ln=1)
        bas_1 = "N: Nouveau, R: Redoublant, T+: Triplant et plus"
        bas_2 = "Veuillez remplir séparement le canevas par filière, type de formation et année des études"

        pdf.cell(0, 5, txt=bas_1, ln=1, align="L")
        pdf.cell(0, 5, txt=bas_2, ln=1, align="L")

        pdf.output(f"files/statistic_total.pdf", "F")
        return f"files/statistic_total.pdf"

    def create_statistic_by_years(data: Any, all_niveau: Any, schemas: str):
        titre_stat = [{"name": '', "value": ["Age"]}, {"name": "masculin", "value": ["N", "R", "T+", "S/Tot"]},
                      {"name": "feminin", "value": ["N", "R", "T+", "S/Tot"]},
                      {"name": "ensemble", "value": ["N", "R", "T+", "Total"]}]

        width: int = 48
        height: int = 7

        pdf = PDF("P", "mm", "a4")

        niveau_ = ["L1", "L2", "L3", "M1", "M2", "H"]
        for index, niveau in enumerate(all_niveau):
            data["niveau"] = niveau_[index]
            for index_3, parc in enumerate(niveau[niveau_[index]]):
                if len(parc["etudiants"]) != 0:
                    data["journey"] = f'{parc["name"]}'
                    pdf.add_page()
                    PDF.add_title(pdf=pdf, data=data, type="age")
                    pdf.set_margin(9)
                    for titre in titre_stat:
                        if titre["name"] != '':
                            pdf.set_font("arial", "BI", 10)
                            pdf.cell(width, height, txt=titre["name"].upper(), border=1, align="C")
                        else:
                            pdf.cell(width, height, txt="")
                    pdf.cell(0, height, txt="", ln=1)

                    for titre in titre_stat:
                        for value in titre["value"]:
                            pdf.set_font("arial", "BI", 10)
                            pdf.cell(width / (len(titre["value"])), height, txt=value, border=1, align="C")
                    pdf.cell(0, height, txt="", ln=1)

                    for index in range(16):
                        for index_1, titre in enumerate(titre_stat):
                            for value in titre["value"]:
                                pdf.set_font("arial", "BI", 10)
                                response = get_by_params(parc["etudiants"], titre["name"].upper(), value, index + 15)
                                if index == 0:
                                    if index_1 == 0:
                                        pdf.cell(width / (len(titre["value"])), height, txt="Moins de 16 ans",
                                                 border=1, align="C")
                                    else:
                                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1,
                                                 align="C")
                                elif index == 14:
                                    if index_1 == 0:
                                        pdf.cell(width / (len(titre["value"])), height, txt="29+", border=1, align="C")
                                    else:
                                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1,
                                                 align="C")
                                elif index == 15:
                                    if index_1 == 0:
                                        pdf.cell(width / (len(titre["value"])), height, txt="Total", border=1,
                                                 align="C")
                                    else:
                                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1,
                                                 align="C")
                                else:
                                    if index_1 == 0:
                                        pdf.cell(width / (len(titre["value"])), height, txt=str(index + 15), border=1,
                                                 align="C")
                                    else:
                                        pdf.cell(width / (len(titre["value"])), height, txt=str(response), border=1,
                                                 align="C")

                        pdf.cell(0, height, txt="", ln=1)

                    bas_1 = "*la plupart des filières sont des types de formation; initiale pour les étudiants à plein temps"
                    bas_2 = "On attend par formation continue celle qui est donnée aux travailleurs à temps partiels"
                    bas_3 = "N.B: Veuillez remplir séparement le canevas par filière, type de formation et année d' études"

                    pdf.cell(0, height, txt="", ln=1)
                    pdf.cell(0, 5, txt=bas_1, ln=1, align="L")
                    pdf.cell(0, 5, txt=bas_2, ln=1, align="L")
                    pdf.cell(0, 5, txt=bas_3, ln=1, align="L")

        pdf.output(f"files/statistic_by_years.pdf", "F")
        return f"files/statistic_by_years.pdf"
