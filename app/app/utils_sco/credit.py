from typing import Any

from app.liste import header
from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import convert_date


def get_niveau_credit(niveau: str):
    niveau_ = {}
    if niveau == "L1":
        niveau_["level"] = "PREMIERE ANNÉE DU LICENCE"
        niveau_["credit"] = "60"
    elif niveau == "L2":
        niveau_["level"] = "DEUXIEME ANNÉE DU LICENCE"
        niveau_["credit"] = "120"
    elif niveau == "L3":
        niveau_["level"] = "TROISIÈME ANNÉE DU LICENCE"
        niveau_["credit"] = "180"
    elif niveau == "M1":
        niveau_["level"] = "PREMIERE ANNÉE DU MASTER"
        niveau_["credit"] = "60"
    else:
        niveau_["level"] = "DEUXIEME ANNÉE DU MASTER"
        niveau_["credit"] = "120"
    return niveau_


def attestation_validation_credit(num_carte: str, date: str, data: Any) -> str:
    pdf = FPDF("P", "mm", "a4")
    pdf.add_page()
    pdf.l_margin = 20

    titre1 = "REPOBLIKAN'I MADAGASIKARA"
    titre2 = "Fitiavana - Tanindrazana - Fandrosoana"
    titre3 = "Ministère de l'Enseignement Supérieur et de la Recherche Scientifique"

    titre4 = "UNIVERSITE DE FIANARANTSOA"
    titre5 = "FACULTE DES SCIENCES"
    titre6 = f"N° ___/{date}/UF/FAC.S/S.SCO"
    nom_certificat = f"ATTESTATION DE VALIDATION DE CREDITS"

    text_1 = "Le DOYEN de la FACULTE des SCIENCES de L'Université de Fianarantsoa"
    text_2 = "Soussigné, atteste que:"

    nom = "Nom:"
    nom_etudiant = f"{data['last_name']}"
    prenom = "Prénom:"
    prenom_etudiant = f"{data['first_name']}"
    naiss = "Né(e) le:"
    naiss_etudiant = f"{convert_date(data['date_birth'])} à {data['place_birth']}"
    mention = "MENTION:"
    mention_etudiant = f"{data['mention']}"
    journey = "Parcours:"
    journey_etudiant = f"{data['journey']}"
    registre = f"N° sur le registre:"
    registre_etudiant = f"{num_carte} RI-{data['register']}"

    text_3 = f"A validé les {get_niveau_credit(data['level'])['credit']} " \
             f"crédits de la {get_niveau_credit(data['level'])['level']}"
    text_3_1 = f"en {data['journey']}"
    text_4 = "En foi de quoi, la présence d'attestation lui est delivré pour servir et valoir ce que le droit"

    text_5 = "Fianarantsoa, le "

    pdf.add_font("alger", "", "Algerian.ttf", uni=True)
    pdf.add_font("aparaj", "", "aparaj.ttf", uni=True)

    header(pdf)

    pdf.set_font("arial", "B", 14)
    pdf.cell(0, 15, txt="", ln=1, align="C")

    pdf.set_font("arial", "B", 14)
    pdf.cell(0, 2, txt=titre1, ln=1, align="C")

    pdf.set_font("aparaj", "", 11)
    pdf.cell(0, 10, txt=titre2, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 0, txt=titre3, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 10, txt="", ln=1, align="C")
    #
    # pdf.set_font("arial", "B", 14)
    # pdf.cell(0, 6, txt=titre4, ln=1, align="C")
    #
    # pdf.set_font("arial", "B", 12)
    # pdf.cell(0, 6, txt=titre5, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 6, txt=titre6, ln=1, align="C")

    pdf.cell(0, 6, txt="", ln=1, align="C")
    pdf.set_font("alger", "", 18)
    pdf.cell(150, 20, txt=nom_certificat, border=1, ln=1, align="C", center=True)

    pdf.cell(0, 5, txt="", ln=1)
    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_1, ln=1, align="L")

    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_2, ln=1, align="L")

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(12, 8, txt=nom, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=nom_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(18, 8, txt=prenom, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=prenom_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(18, 8, txt=naiss, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=naiss_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(22, 8, txt=mention, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=mention_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(22, 8, txt=journey, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=journey_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(37, 8, txt=registre, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=registre_etudiant, ln=1)

    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_3, ln=1)
    pdf.cell(0, 8, txt=text_3_1, ln=1)

    pdf.cell(0, 8, txt="", ln=1)
    pdf.cell(0, 8, txt=text_4, ln=1)
    pdf.cell(94, 12, txt="", ln=0)
    pdf.cell(0, 12, txt=text_5, ln=1)

    pdf.cell(0, 40, txt="", ln=1)

    pdf.output(f"files/{num_carte}_validation.pdf", "F")
    return f"files/{num_carte}_validation.pdf"


if __name__ == "__main__":
    # string = "éôfèçdn&n sdgfgz"
    # strd = string.replace(" ","_")
    # print(unidecode.unidecode(strd))
    data = {"nom": "RALAITSIMANOLAKAVANA", "prenom": "Henri Franck",
            "date_naiss": "07 octobre 1995 ", "lieu_naiss": " Fianarantsoa",
            "niveau": "M2", "mention": "Mathématiques et Applications",
            "journey": "Mathématiques et Informatiques pous la Sciences Social",
            "registre": "20"}

    attestation_validation_credit("4465", "2020", "2020-2021", data)
