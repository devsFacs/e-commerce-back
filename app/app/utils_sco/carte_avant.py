from app.pdf.PDFMark import PDFMark as FPDF
from typing import Any
import qrcode
import os

from app.utils import convert_date, clear_name


class PDF(FPDF):
    def create_carte(pdf: FPDF, pos_init_y: int, long_init_y: int, deux_et: list, data: Any):
        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        logo_univ = "images/logo_univ.jpg"
        logo_fac = "images/logo_science.jpg"

        titre_1 = "Université de Fanarantsoa \n"
        titre_1 += "Faculté des Sciences \n"

        titre_2 = "Le Chef de service de scolarité:"
        titre_3 = f"{data['supperadmin']}"

        # titre_4 = "Faculté des Sciences"
        i: int = 0
        pos_init_x: int = 0.2
        long_init_x: int = 3.9
        absci: int = 1.25
        ordon: int = 0.06

        i = 0
        while i < len(deux_et):
            num_carte = f"{deux_et[i]['num_carte']}"
            niveau = f"{deux_et[i]['level']}"
            image_fac = f"images/{niveau.lower()}_avant.jpg"
            profile = f"files/photo/{deux_et[i]['photo']}"
            image = profile if os.path.exists(profile) else f"images/profil.png"
            mask = "images/mask.png"

            info = f"Nom: {clear_name(deux_et[i]['last_name'].upper(), 25)}\n"
            info += f"Prénom: {deux_et[i]['first_name']}\n"
            info += f"Né(e) le: {convert_date(deux_et[i]['date_birth'])} à {deux_et[i]['place_birth']}\n"
            if deux_et[i]['num_cin'] and deux_et[i]['num_cin'] != "None":
                info += f"CIN: {deux_et[i]['num_cin']} \n"
                info += f"du {convert_date(deux_et[i]['date_cin'])} à {deux_et[i]['place_cin']} \n "
            info_ = f"CE: {num_carte}\n"
            info_ += f"Parcours: {deux_et[i]['journey'].upper()}\n"
            info_ += f"Mention: {data['mention']}\n"

            data_et = [deux_et[i]['num_carte'], data['key']]
            #
            # if {deux_et[i]['num_cin']}:
            #     info_ += f"CIN {deux_et[i]['num_cin']} "
            #     info_ += f"du {deux_et[i]['date_cin']} \n "
            #     info_ += f"à {deux_et[i]['lieu_cin']} \n "

            qr = qrcode.make(f"{data_et}")

            pdf.set_font('Times', '', 8.0)

            # pdf.image(f"images/mask.png", is_mask=True)
            pdf.image(image_fac, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            # pdf.image(mask,x=pos_init_x+0.05, y=pos_init_y+0.05,w=1, is_mask=True)

            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(image, x=pos_init_x + 0.05, y=pos_init_y + 0.7, w=1, h=1.18)
            pdf.set_text_color(0, 0, 0)

            pdf.set_font('Times', 'B', 8.0)
            with pdf.local_context(fill_opacity=0.35):
                pdf.set_fill_color(255, 255, 255)
                if i == 0:
                    pdf.set_xy(absci - 1, pos_init_y + ordon - 0.02)
                else:
                    pdf.set_xy(absci + pos_init_x - 0.2 - 1, pos_init_y + ordon - 0.02)
                pdf.cell(3.8, 0.63, txt="", border=0, fill=True, align="L")

            if i == 0:
                pdf.set_xy(absci - 0.7, pos_init_y + ordon + 0.05)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 0.7, pos_init_y + ordon + 0.05)
            pdf.image(logo_univ, w=0.5, h=0.5)

            if i == 0:
                pdf.set_xy(absci + 2, pos_init_y + ordon + 0.05)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2, pos_init_y + ordon + 0.05)
            pdf.image(logo_fac, w=0.5, h=0.5)

            pdf.set_font('Times', 'B', 9)
            if i == 0:
                pdf.set_xy(absci - 0.35, pos_init_y + ordon + 0.08)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 - 0.35, pos_init_y + ordon + 0.08)

            pdf.multi_cell(2.5, 0.15, titre_1.upper(), border=0, ln=0, fill=False, align='C')
            pdf.ln(0.1)

            pdf.set_font('Times', 'B', 7.0)
            if i == 0:
                pdf.set_xy(absci + 0.02, pos_init_y + ordon + 0.7)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 0.02, pos_init_y + ordon + 0.7)

            pdf.multi_cell(2.16, 0.15, info, 0, fill=0, align='L')
            pdf.ln(0.1)

            pdf.set_font('Times', '', 8.0)
            if i == 0:
                pdf.set_xy(absci, pos_init_y + ordon + 1.7)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2, pos_init_y + ordon + 1.7)
            pdf.cell(2.5, 0.15, txt=titre_2, ln=1, align="L")

            if i == 0:
                pdf.set_xy(absci + 0.1, pos_init_y + ordon + 1.9)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 0.1, pos_init_y + ordon + 1.9)
            pdf.cell(2.5, 0.15, txt=titre_3, ln=0, align="L")

            pdf.set_font('Times', '', 10)
            pdf.set_fill_color(255, 255, 255)
            if i == 0:
                pdf.set_xy(absci + 2.1, pos_init_y + ordon + 1)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2.1, pos_init_y + ordon + 1)
            pdf.cell(0.7, 0.4, txt="", border=1, fill=True, align="L")

            if i == 0:
                pdf.set_xy(absci + 2.1, pos_init_y + ordon + 0.8)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2.1, pos_init_y + ordon + 0.8)
            pdf.cell(0.9, 0.15, txt="Signature", align="L")

            # if i == 0:
            #     pdf.set_xy(absci + 1.6, pos_init_y + ordon + 1.3)
            # else:
            #     pdf.set_xy(absci + pos_init_x - 0.2 + 1.6, pos_init_y + ordon + 1.3)
            # pdf.cell(0, 0.15, txt=titre_4, ln=0, align="L")

            if i == 0:
                pdf.set_xy(0.3, pos_init_y + ordon + 2)
            else:
                pdf.set_xy(0.9 + pos_init_x - 0.2 - 0.6, pos_init_y + ordon + 2)

            pdf.set_font('Times', '', 9.0)
            pdf.multi_cell(2.2, 0.15, info_, 0, fill=0, align='J')

            pdf.set_font('Times', 'B', 14.0)
            if i == 0:
                pdf.set_xy(absci + 2.2, pos_init_y + ordon + 1.9)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2.2, pos_init_y + ordon + 1.9)
            # pdf.cell(1, 0.15, txt=num_carte, ln=1, align="C")
            pdf.image(qr.get_image(), w=0.6, h=0.6)

            pdf.set_font('Times', 'BI', 9)
            if i == 0:
                pdf.set_xy(absci + 1.9, pos_init_y + ordon + 0.36)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 1.9, pos_init_y + ordon + 0.36)
            # pdf.cell(1, 0.15, txt=niveau, ln=1, align="C")
            pdf.ln(0.1)

            pos_init_x = long_init_x + 0.3
            i = i + 1

    def boucle_carte(pdf: FPDF, huit_etudiant: list, data: Any):
        pdf.add_page()
        pos_init_y: int = 0.2
        long_init_y: int = 2.6
        nbr: int = 0
        if len(huit_etudiant) % 2 == 0:
            nbr = len(huit_etudiant) // 2
        else:
            nbr = (len(huit_etudiant) // 2) + 1
        n = 0
        p: int = 0
        k = 0
        while n < nbr:
            PDF.create_carte(pdf, pos_init_y, long_init_y, huit_etudiant[p:p + 2], data)
            p += 2
            pos_init_y = pos_init_y + long_init_y + 0.1
            n += 1

        pdf.line(4.15, 0.2, 4.15, pos_init_y - 0.05)

    def parcourir_et(etudiant: list, data: Any):

        pdf = PDF("P", "in", "a4")

        nbr: int = 0

        if len(etudiant) % 8 == 0:
            nbr = len(etudiant) // 8
        else:
            nbr = (len(etudiant) // 8) + 1
        k: int = 0
        l: int = 0

        while k < nbr:
            PDF.boucle_carte(pdf, etudiant[l:l + 8], data)
            k += 1
            l += 8
        pdf.output(f"files/pdf/carte/carte_{data['mention']}.pdf", "F")

        return f"files/pdf/carte/carte_{data['mention']}.pdf"
