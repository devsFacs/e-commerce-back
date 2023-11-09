from typing import Any, List
from app.pdf.PDFMark import PDFMark as FPDF
from app.liste.header import header
from app.schemas import Journey


def set_orientation(nbr: int) -> str:
    if nbr >= 8:
        return "L"
    return "P"


def set_police(mot: str, nbr: int) -> int:
    if nbr >= 7:
        if len(mot) >= 25:
            return 8
        elif len(mot) >= 31:
            return 7
        elif len(mot) >= 36:
            return 6
    return 10


def set_police_name(mot: str, dim: int) -> int:
    if dim == 73:
        if len(mot) <= 35:
            return 10
        elif len(mot) <= 47:
            return 7
        elif len(mot) <= 54:
            return 6
    elif dim == 108:
        if len(mot) <= 50:
            return 10
        else:
            return 8
    return 10


def set_dimention(nbr: int) -> int:
    if nbr == 1:
        return 158
    elif nbr == 2:
        return 107
    elif nbr == 3:
        return 142
    else:
        return 90


def get_dime(nbr: int) -> int:
    if nbr == 6:
        return 320
    elif nbr == 5:
        return 396
    elif nbr == 7:
        return 286
    else:
        return 400


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, sems: str, title: str, nbr: int):
        header(pdf)
        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        journey = "PARCOURS:"
        journey_etudiant = f"{data['journey']}"
        semester = "SEMESTRE:"
        semester_etudiant = f"{sems.upper()}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"
        session = "SESSION:"
        sessionclass = f"{data['session']}"

        pdf.set_font("alger", "", 15)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=mention_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=journey, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=journey_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=semester, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=semester_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(23, 8, txt=session, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=sessionclass.upper(), ln=1)

    def add_corp(pdf: FPDF, data: Any, sems: str, matiers: List[str], admis: Any, type: str):
        pdf.add_page()
        pdf.set_margin(10)
        titre = f"RESULTAT DE L'UNITÉ D'ENSEIGNEMENTS {matiers[1].upper()}"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre, nbr=2)
        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(22, 5, txt="N° Carte", border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(160, 5, txt="Nom et prénom", border=1, align="C")
        nbr = 0
        for i, etudiant in enumerate(admis):
            nbr += 1
            num_carte_ = etudiant['N° Carte']
            name = f"{etudiant['nom']} {etudiant['prenom']}"
            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "I", 10)
            pdf.cell(1, 5, txt="")
            pdf.cell(22, 5, txt=num_carte_, border=1)
            pdf.cell(1, 5, txt="")
            pdf.set_font("arial", "I", 10)
            pdf.cell(160, 5, txt=name, border=1, align="L")

        text_1 = f"ARRÉTÉE LA PRÉSENTE LISTE AU NOMBRE DE {nbr} ÉTUDIANT(S) AYANT VALIDÉ(S) L'UNITE D'ENSEIGNEMENT "
        if type == "compense":
            text_2 = f"{matiers[1].upper()} PAR COMPENSATION"
        else:
            text_2 = f"{matiers[1].upper()} "

        text_3 = "Le PRÉSIDENT DU JURY"
        text_4 = "Fianarantsoa, le"
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 7, txt="", ln=1)
        pdf.cell(0, 5, txt=text_1, ln=1, align="L")
        pdf.cell(0, 5, txt=text_2, ln=1, align="L")
        pdf.cell(1, 2, txt="", ln=1)

        pdf.set_font("arial", "BI", 10)
        pdf.cell(100, 5, txt="", align="L")
        pdf.cell(0, 5, txt=text_4, ln=1, align="L")
        pdf.cell(1, 22, txt="", ln=1)
        pdf.cell(100, 5, txt="")
        pdf.cell(0, 5, txt=text_3, ln=1, align="L")

    def create_result_by_ue(sems: str, journey: Journey, data: Any, matiers: List[str], etudiants: Any, admis: Any,
                            admis_comp: Any):
        pdf = PDF(set_orientation(len(matiers)), "mm", "a4")

        pdf.watermark('Faculté des Sciences', font_style='BI')
        pdf.add_page()

        titre = f"RÉSULTAT PROVISOIR DE L'UNITÉ D'ENSEIGNEMENT {matiers[1].upper()}"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre, nbr=len(matiers))

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 5, txt="", ln=1, align="C")

        for i, ue in enumerate(matiers):
            dim = set_dimention(len(ue))
            pdf.set_left_margin(1)
            taille = set_police(ue, len(matiers))
            pdf.cell(1, 8, txt="")
            pdf.set_font("arial", "I", 10)
            titre = f"{ue}"
            dim = get_dime(len(matiers)) / len(matiers) - 4
            if titre == "Status":
                dim = 19
            elif titre == "Crédit":
                dim = 12
            elif titre == "N° Carte":
                dim = 21
            pdf.set_font("arial", "", taille)
            pdf.cell(dim, 5, txt=titre, border=1, align="C")

        for i, etudiant in enumerate(etudiants):

            pdf.cell(1, 5, txt="", ln=1)
            pdf.cell(1, 1, txt="", ln=1)
            for i, ue in enumerate(matiers):
                titre = f"{ue}"
                dim = get_dime(len(matiers)) / len(matiers) - 4
                if titre == "Status":
                    dim = 19
                    value = str(etudiant[ue])
                elif titre == "Crédit" :
                    dim = 12
                    value = str(etudiant[ue])
                elif titre == "N° Carte":
                    dim = 21
                    value = str(etudiant[ue])
                else:
                    if str(etudiant[ue]) == "None" or str(etudiant[ue]) == "":
                        value = "Absent"
                    else:
                        value = str(format(float(etudiant[ue]), '.3f'))
                pdf.set_font("arial", "I", 10)
                pdf.cell(1, 5, txt="")
                if value == "None" or value == "":
                    value = "Absent"
                pdf.cell(dim, 5, txt=value, border=1, align='C')
        PDF.add_corp(pdf=pdf, data=data, sems=sems, matiers=matiers, admis=admis, type="definitive")
        if len(admis_comp) != 0:
            PDF.add_corp(pdf=pdf, data=data, sems=sems, matiers=matiers, admis=admis_comp, type="compense")

        pdf.output(f"files/pdf/resultat/resultat_{sems}_{journey.abbreviation}_{matiers[1]}_{data['anne']}.pdf", "F")
        return f"files/pdf/resultat//resultat_{sems}_{journey.abbreviation}_{matiers[1]}_{data['anne']}.pdf"
