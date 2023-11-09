from typing import Any
from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import convert_date


def validation(ue: float, code: bool) -> str:
    if float(ue) < 10:
        if code:
            return "Compensé"
        else:
            return "À refaire"
    else:
        return "Validé"


def relever_note(num_carte: str, date: str, data: Any, note: Any) -> str:
    pdf = PDF()

    # set watermark prior to calling add_page()
    pdf.watermark('Faculté des Sciences', y=175, font_style='BI')
    pdf.add_page()
    pdf.l_margin = 0
    pdf.rect(3, 3, 204, 291)
    pdf.rect(2, 2, 206, 293)
    pdf.l_margin = 8

    titre1 = "REPOBLIKAN'I MADAGASIKARA"
    titre1_2 = "Universtité de Fianarantsoa"

    titre2 = "Fitiavana - Tanindrazana - Fandrosoana"
    titre2_1 = "Faculté des sciences"
    titre3 = "Ministère de l'Enseignement Supérieur"
    titre3_1 = "Service scolarité"
    titre4 = "et de la recherche scientifique"
    titre4_1 = f"Année universitaire {data['year']}"
    titre5 = "releve de note"
    titre6 = f"N° ___/{date}/UF/FAC.S/S.SCO"

    pdf.set_text_color(0, 0, 0)
    nom = "Nom et prénom:"
    nom_etudiant = f"{data['last_name']} {data['first_name'] if data['first_name'] != 'None' else ''} "
    naiss = "Né(e) le:"
    naiss_etudiant = f"{convert_date(data['date_birth'])} à {data['place_birth']}"
    numero = "N° carte:"
    semester = f"Semestre:"
    semester_etudiant = f"{data['semester']}"
    mention = "Mention:"
    mention_etudiant = f"{data['mention']}"
    journey = "Parcours:"
    journey_etudiant = f"{data['journey']}"
    session = f"Session:"
    sessionetudiant = f"{data['session']}"
    validation_et = f"{data['validation']}"

    titre_1 = "Les unité d'enseignements"
    titre_2 = "Notes(/20)"
    titre_3 = "Coéfficients"
    titre_4 = 'Crédits'
    titre_5 = "Status de l'UE"
    text_6 = "Décision du jury:"
    text_7 = "Fianarantsoa, le "
    moyenne = "moyenne générale"

    pdf.add_font("alger", "", "Algerian.ttf", uni=True)
    pdf.add_font("aparaj", "", "aparaj.ttf", uni=True)

    pdf.set_font("arial", "B", 10)
    pdf.cell(9, 5, txt="", ln=0, align="L")
    pdf.cell(120, 5, txt=titre1, ln=0, align="L")

    pdf.set_font("arial", "B", 10)
    pdf.cell(0, 5, txt=titre1_2.upper(), ln=1)

    pdf.set_font("arial", "", 8)
    pdf.cell(13, 5, txt="", ln=0, align="L")
    pdf.cell(125, 5, txt=titre2, ln=0, align="L")

    pdf.set_font("arial", "B", 10)
    pdf.cell(0, 5, txt=titre2_1.upper(), ln=1)

    pdf.set_font("arial", "B", 10)
    pdf.cell(142, 5, txt=titre3.upper(), ln=0, align="L")

    pdf.set_font("arial", "B", 10)
    pdf.cell(0, 5, txt=titre3_1.upper(), ln=1)

    pdf.set_font("arial", "B", 10)
    pdf.cell(6, 5, txt="", ln=0, align="L")
    pdf.cell(130, 5, txt=titre4.upper(), ln=0, align="L")

    pdf.set_font("arial", "", 10)
    pdf.cell(0, 5, txt=titre4_1, ln=1)

    pdf.set_font("arial", "B", 10)
    pdf.ln(1)
    pdf.cell(193, 5, txt=titre5.upper(), ln=1, align="C")
    pdf.cell(193, 5, txt=titre6.upper(), ln=1, align="C")

    pdf.l_margin = 0
    pdf.ln(3)
    pdf.rect(12, 42, 188, 23)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(32, 5, txt=nom, ln=0, align="L")

    pdf.set_font("aparaj", "", 11)
    pdf.cell(100, 5, txt=nom_etudiant, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=naiss, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=naiss_etudiant, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=numero, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=num_carte, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=journey, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=journey_etudiant, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=semester, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=semester_etudiant, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=mention, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=mention_etudiant, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=session, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=sessionetudiant, ln=1)

    # debut de creation du tableau
    pdf.cell(30, 2, txt="", ln=1)
    pdf.set_font("arial", "I", 10)
    pdf.cell(12, 2, txt="", ln=0)

    pdf.set_fill_color(210, 210, 210)
    pdf.cell(98, 5, txt=titre_1.upper(), border=1, ln=0, align="C", fill=True)

    pdf.cell(20, 5, txt=titre_2, border=1, ln=0, align="C", fill=True)

    pdf.cell(25, 5, txt=titre_3, border=1, ln=0, align="C", fill=True)

    pdf.cell(15, 5, txt=titre_4, border=1, ln=0, align="C", fill=True)

    pdf.cell(30, 5, txt=titre_5, border=1, ln=1, align="C", fill=True)

    for index_ue, value_ue in enumerate(note['ue']):
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(98, 5, txt=f"U.E-{index_ue + 1}: {value_ue['name']}", border=1, ln=0, align="C")
        pdf.set_font("arial", "I", 11)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(19, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        for index, value in enumerate(value_ue['ec']):
            pdf.set_top_margin(20)
            pdf.cell(30, 1, txt="", ln=1)
            pdf.cell(12, 2, txt="", ln=0)
            pdf.set_font("arial", "I", 9)
            pdf.cell(98, 5, txt=f"E.C-{index + 1}: {value['name']}", border=1, ln=0, align="L")
            pdf.set_font("arial", "I", 11)
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(19, 5, txt=str(value['note']), border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(24, 5, txt=str(value['weight']), border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(98, 5, txt=f"NOTE SOUS TOTAL U.E-{index_ue + 1}", border=1, ln=0, align="C")
        pdf.set_font("arial", "I", 9)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(19, 5, txt=str(format(value_ue['note'], '.3f')), border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt=str(value_ue['credit']), border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.set_font("alger", "", 9)
        pdf.cell(29, 5, txt=validation(value_ue['note'], data["code"]), border=1, ln=1, align="C")

    pdf.set_top_margin(20)
    pdf.cell(30, 1, txt="", ln=1)
    pdf.cell(12, 2, txt="", ln=0)
    pdf.set_font("arial", "BI", 9)
    pdf.cell(98, 6, txt=moyenne.upper(), border=1, ln=0, align="C")
    pdf.set_font("arial", "I", 10)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(19, 6, txt=str(format(note['mean'], '.3f')), border=1, ln=0, align="C")
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(24, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(14, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(29, 5, txt="", ln=1)

    pdf.set_font("Times", "Bui", 10)
    pdf.cell(40, 10, txt="", ln=0)
    pdf.cell(28, 10, txt=text_6, ln=0)
    pdf.set_font("Times", "i", 10)
    pdf.cell(0, 10, txt=validation_et, ln=1)
    pdf.set_font("arial", "I", 10)
    pdf.cell(130, 1, txt="", ln=1)
    pdf.cell(130, 8, txt="", ln=0)
    pdf.cell(0, 8, txt=text_7, ln=1)

    pdf.l_margin = 8

    pdf.output(f"files/pdf/relever/{num_carte}_relever.pdf", "F")

    return f"files/pdf/relever/{num_carte}_relever.pdf"


class PDF(FPDF):
    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("arial", "", 9)
        self.cell(1, 4, txt="N.B: Ce relevé de Notes ne doit être en aucun cas remis", ln=1)
        self.cell(12, 6, txt="", ln=0)
        self.cell(1, 6, txt="à l'intéressé sous peine d'annulation.", ln=0)
