from typing import Any, List
from app.pdf.PDFMark import PDFMark as FPDF
from app.liste.header import header


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


def get_title_session(session: str) -> str:
    if session.lower() == "rattrapage":
        return "session de rattrapage"
    return f"session {session}"


def get_type_response(session: str, type: str) -> str:
    if type != "compense":
        if session.lower() == "rattrapage":
            return "en session de rattrapage"
        return f"en session {session}"
    return "par compensation"


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, sems: str, title: str):
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
        pdf.cell(28, 8, txt=journey, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=journey_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(28, 8, txt=semester, align="L")

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

    def create_result_by_session(sems: str, parcour: str, data: Any, admis: Any):
        pdf = PDF("P", "mm", "a4")
        session = str(data["session"])
        titre = f"RÉSULTAT {get_title_session(session).upper()}"
        text_3 = "LE PRÉSIDENT DU JURY"
        text_4 = "Fianarantsoa, le"

        type_result = ["definitive", "compense"]
        for type_ in type_result:
            pdf.watermark("Faculté des Sciences", font_style="BI")
            pdf.add_page()
            PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre)
            pdf.set_margin(10)
            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "BI", 10)
            pdf.cell(12, 5, txt="Rang", border=1, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(18, 5, txt="N° Carte", border=1, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(117, 5, txt="Nom et prénom", border=1, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(24, 5, txt="Moyenne", border=1, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(20, 5, txt="Crédit", border=1, align="C")
            for i, etudiant in enumerate(admis[type_]):
                num_carte_ = etudiant["N° Carte"]
                mean = etudiant["mean"]
                credit = etudiant["credit"]
                name = f"{etudiant['last_name']} {etudiant['first_name']}"
                pdf.cell(1, 7, txt="", ln=1)
                pdf.set_font("arial", "I", 10)
                pdf.cell(12, 5, txt=str(i + 1), border=1, align="C")
                pdf.cell(1, 5, txt="")
                pdf.cell(18, 5, txt=num_carte_, border=1)
                pdf.cell(1, 5, txt="")
                pdf.set_font("arial", "I", 10)
                pdf.cell(117, 5, txt=name, border=1, align="L")
                pdf.cell(1, 5, txt="")
                pdf.cell(24, 5, txt=str(mean), border=1, align="C")
                pdf.cell(1, 5, txt="")
                pdf.cell(20, 5, txt=str(credit), border=1, align="C")

            text_1 = f"ARRÉTÉE LA PRÉSENTE LISTE AU NOMBRE DE {len(admis[type_])} ÉTUDIANT(S) AYANT VALIDÉ "
            text_2 = f"LES TRENTE CREDITS (30 Crédits) {get_type_response(session, type_).upper()}"

            pdf.set_font("arial", "BI", 10)
            pdf.cell(1, 10, txt="", ln=1)
            pdf.cell(0, 5, txt=text_1, ln=1, align="L")
            pdf.cell(0, 5, txt=text_2, ln=1, align="L")
            pdf.cell(1, 2, txt="", ln=1)

            pdf.set_font("arial", "BI", 10)
            pdf.cell(100, 5, txt="", align="L")
            pdf.cell(0, 5, txt=text_4, ln=1, align="L")
            pdf.cell(1, 22, txt="", ln=1)
            pdf.cell(100, 5, txt="", align="L")
            pdf.cell(0, 5, txt=text_3, ln=1, align="L")

        pdf.output(f"files/pdf/resultat/resultat_{sems}_{parcour}_{session}.pdf", "F")
        return f"files/pdf/resultat/resultat_{sems}_{parcour}_{session}.pdf"
