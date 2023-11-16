from typing import Any
from app.pdf.PDFMark import PDFMark as FPDF

from app.liste import header
from app.utils import get_niveau_long, clear_name


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, title: str):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        header(pdf)
        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        mention = "MENTION:"
        mention_student = f"{data['mention']}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"

        pdf.set_font("alger", "", 22)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=mention_student, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

    def create_list_bourse(mention: str, all_data: Any, type_: str):
        pdf = PDF("P", "mm", "a4")
        pdf.watermark("Faculté des Sciences", font_style="BI")
        pdf.add_page()
        data = {"mention": all_data["mention"], "anne": all_data["year"]}

        titre = f"LISTE DES ÉTUDIANTS BOURSIER {type_.upper()}"
        PDF.add_title(pdf=pdf, data=data, title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"
        level = ["l1", "l2", "l3", "m1", "m2"]
        for i, journey in enumerate(all_data["journey"]):
            for niv in level:
                if len(journey[niv]) != 0:
                    pdf.add_page()
                    pdf.set_font("arial", "B", 12)
                    pdf.cell(0, 5, txt=f"Parcours: {journey['name']}", ln=1, align="L")
                    pdf.cell(1, 1, txt="", ln=1)
                    pdf.cell(
                        0, 5, txt=f"Niveau:{get_niveau_long(niv)}", ln=1, align="L"
                    )
                    pdf.cell(1, 4, txt="", ln=1)
                    pdf.set_font("arial", "BI", 10)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(12, 5, txt=num, border=1)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(18, 5, txt=num_c, border=1)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(160, 5, txt=nom_et_prenom, border=1, align="C")
                    num_ = 1
                    for j, student in enumerate(journey[niv]):
                        num_carte_ = student["num_carte"]
                        name = f"{clear_name(student['last_name'])} {student['first_name']}"
                        pdf.cell(1, 7, txt="", ln=1)
                        pdf.set_font("arial", "I", 10)
                        pdf.cell(1, 5, txt="")
                        pdf.cell(12, 5, txt=str(num_), border=1)
                        pdf.cell(1, 5, txt="")
                        pdf.cell(18, 5, txt=num_carte_, border=1)
                        pdf.cell(1, 5, txt="")
                        pdf.set_font("arial", "I", 10)
                        pdf.cell(160, 5, txt=name, border=1, align="L")
                        num_ += 1

        pdf.output(f"files/pdf/liste/list_bourse_{type_.lower()}_{mention}.pdf", "F")
        return f"files/pdf/liste/list_bourse_{type_.lower()}_{mention}.pdf"
