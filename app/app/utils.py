import json
import logging
import os
import secrets
import smtplib
import ssl
import string
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional
from uuid import UUID

import requests
from jose import jwt
from pydantic import EmailStr
from sqlalchemy import MetaData, Table
from unidecode import unidecode

from app import schemas
from app.core.config import settings
from app.db.session import engine
import pytz


def _get_date():
    return datetime.now()


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    file_path: str = "",
    file_name: str = "",
    environment=None,
) -> None:
    if environment is None:
        environment = {}
    message = MIMEMultipart()
    message["From"] = (
        settings.EMAILS_FROM_NAME + " <" + settings.EMAILS_FROM_EMAIL + ">"
    )
    message["To"] = email_to
    message["Subject"] = subject_template
    if os.path.exists(file_path):
        with open(file_path, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_attachment.add_header(
                "content-disposition", "attachment", filename=file_name
            )
            message.attach(pdf_attachment)

    message.attach(MIMEText(html_template, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()  # Use TLS for secure connection
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        # Send the email
        response = server.sendmail(settings.SMTP_USER, email_to, message.as_string())
        logging.info(f"send email result: {response}")


def send_student_transcript(email_to, name, semester, num_carte):
    subject = f"{settings.UNIVERSITY_NAME} - Relevé de notes"
    file_path = f"files/pdf/relever/{num_carte}_relever.pdf"
    file_name = f"{num_carte}_relever.pdf"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email.html") as f:
        template_str = f.read()

        template_str = template_str.replace("{{name}}", name)
        template_str = template_str.replace("{{semester}}", semester)

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        file_path=file_path,
        file_name=file_name,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def create_secret():
    res = "".join(
        secrets.choice(string.ascii_letters + string.digits) for x in range(10)
    )
    return res


def create_year(year: str):
    ann = "year_" + year[0:4] + "_" + year[5:9]
    return ann


def get_last_year(year: str, bacc_year: str) -> bool:
    if year[0:4] != bacc_year:
        return False
    return True


def create_num_carte(plugged: str, num: str):
    key: str = plugged[0:1]
    nbr_zero: int = 6 - len(num)
    response: str = "".join("0" for x in range(nbr_zero))
    return f"{key.upper()}{response}{num}"


def decode_schemas(schema: str):
    ann = f"{schema[5:9]}-{schema[10:15]}"
    return ann


def creaate_registre(schema: str):
    reg = schema[2:4]
    return reg


def decode_text(text: str) -> str:
    str_ = text.replace(" ", "_")
    str_ = str_.replace("'", "_")
    return unidecode(str_.replace("-", "_"))


def decode_(text: str) -> str:
    str_ = text.replace("'", "\\'")
    return str_


def get_max(sems_a: str, sems_b: str) -> str:
    if not sems_a:
        sems_a = ""
    if not sems_b:
        sems_b = ""
    if len(sems_a) == 0:
        value_1 = 0
    else:
        value_1 = sems_a.upper().partition("S")[2]

    if len(sems_b) == 0:
        value_2 = 0
    else:
        value_2 = sems_b.upper().partition("S")[2]

    if int(value_1) > int(value_2):
        return sems_a
    return sems_b


def get_min(sems_a: str, sems_b: str) -> str:
    if not sems_a:
        sems_a = ""
    if not sems_b:
        sems_b = ""
    if len(sems_a) == 0:
        value_1 = 0
    else:
        value_1 = sems_a.upper().partition("S")[2]

    if len(sems_b) == 0:
        value_2 = 0
    else:
        value_2 = sems_b.upper().partition("S")[2]
    if int(value_1) > int(value_2):
        return sems_b
    return sems_a


def get_sems_min(niveau: str) -> str:
    if niveau.upper() == "L1":
        return "S1"
    elif niveau.upper() == "M1":
        return "S7"
    elif niveau.upper() == "M2":
        return "S9"


def get_sems_max(niveau: str) -> str:
    if niveau.upper() == "L1":
        return "S2"
    elif niveau.upper() == "M1":
        return "S8"
    elif niveau.upper() == "M2":
        return "S10"


def get_credit(value: float, credit: int) -> int:
    if value >= 10:
        return credit
    return 0


def max_value(value_1: str, value_2: str) -> float:
    if value_1 == "" or value_1 is None:
        value_1 = 0
    if value_2 == "" or value_2 is None:
        value_2 = 0

    if float(value_1) >= float(value_2):
        return value_1
    return value_2


def get_niveau(sems_a: str, sems_b: str) -> str:
    if len(get_max(sems_a, sems_b)) == 0:
        return "Invalid semester"
    else:
        value_1 = get_max(sems_a, sems_b).upper().partition("S")[2]
    if int(value_1) <= 2:
        return "L1"
    elif int(value_1) <= 4:
        return "L2"
    elif int(value_1) <= 6:
        return "L3"
    elif int(value_1) <= 8:
        return "M1"
    elif int(value_1) <= 10:
        return "M2"


def get_niveau_(sems_a: str, sems_b: str) -> str:
    if len(get_max(sems_a, sems_b)) == 0:
        return "Invalid semester"
    else:
        value_1 = get_max(sems_a, sems_b).upper().partition("S")[2]
    if int(value_1) <= 2:
        return "PREMIERE ANNÉE"
    elif int(value_1) <= 4:
        return "DEUXIEME ANNÉE"
    elif int(value_1) <= 6:
        return "TROISIÈME ANNÉE"
    elif int(value_1) <= 8:
        return "QUATRIÈME ANNÉE"
    elif int(value_1) <= 10:
        return "CINQUIÈME ANNÉE"


def get_niveau_long(niv: str) -> str:
    if niv == "l1":
        return "PREMIÈRE ANNÉE"
    if niv == "l2":
        return "DEUXIÈME ANNÉE"
    if niv == "l3":
        return "TROISIÈME ANNÉE"
    if niv == "m1":
        return "QUATRIÈME ANNÉE"
    if niv == "m2":
        return "CINQUIÈME ANNÉE"


def validation_semester(sems_i: str, credit: int, total_cred: int, year: str):
    response = {"year": year}
    if sems_i:
        if credit == total_cred:
            response[
                "status"
            ] = f"Étudiant(e) ayant validé(e) les {total_cred} crédit définitive."
            response["code"] = True
        else:
            response[
                "status"
            ] = f"Étudiant(e) ayant validé(e) les {total_cred} crédit par compensation."
            response["code"] = True
    else:
        response["status"] = "Étudiant(e) redoublé(e)"
        response["code"] = False
    return response


def check_table_info(schemas: str) -> list:
    all_table = []
    metadata = MetaData(schema=schemas)
    metadata.reflect(bind=engine)
    for table in metadata.tables:
        table_name = table.replace(f"{schemas}.", "")
        if table_name[0:4] != "note":
            all_table.append(table_name)
    return all_table


def check_table_note(schemas: str = "scolary") -> list:
    all_table = []
    metadata = MetaData(schema=schemas)
    metadata.reflect(bind=engine)
    for table in metadata.tables:
        table_name = table.replace(f"{schemas}.", "")
        if table_name[0:4] == "note":
            all_table.append(table_name)
    return all_table


def check_columns_exist(schemas: str, table_name: str) -> Optional[List[str]]:
    metadata = MetaData(schema=schemas, bind=engine)
    columns = []
    table_ = Table(table_name, metadata, autoload=True)
    for index, table in enumerate(table_.columns):
        columns.append(str(table).partition(".")[2])
    return columns


def compare_list(list_2: list, list_1: list):
    for key_1 in list_1:
        if key_1 in list_2:
            list_2.remove(key_1)
    return list_2


def send_new_account(email_to: str, password: str) -> any:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.EMAILS_FROM_EMAIL
    sender_password = settings.PASSWORD_FROM_EMAIL

    message = f"""\
        FROM: Faculté des Sciences
        To: {email_to}
        Subject: Nouveau compte FacScience
        Nouveau compte:\n
        Username: {email_to}
        Password: {password}
        """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email_to, message)


def check_email_valide(email: EmailStr) -> str:
    response = requests.get(
        "https://isitarealemail.com/api/email/validate", params={"email": email}
    )
    status = response.json()["status"]
    return status


def transpose(data: list) -> list:
    new_data = []
    for i in range(len(data[0])):
        new_row = []
        for j in range(len(data)):
            new_row.append(data[j][i])
        new_data.append(new_row)
    return new_data


def find_in_list(list_: list, key_: str) -> int:
    try:
        index = list_.index(key_.lower())
        return index
    except Exception as e:
        return -1


def find_by_key(list_: list, key_: str, value: str) -> int:
    result = -1
    for item in list_:
        if item[key_] == value:
            return 1
    return result


def convert_date(date: str) -> str:
    month = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Aout",
        "Séptembre",
        "Octobre",
        "Novembre",
        "Décembre",
        "",
    ]
    # 1995-10-20
    if not date:
        return ""
    try:
        days = date[8:10]
        year = date[0:4]
        month_ = int(date[5:7])
        return f"{days} {month[month_ - 1]} {year}"
    except Exception as e:
        print(e, date)
        return ""


def clear_name(name: str, nbr: int = 50) -> str:
    if len(name) <= nbr:
        return name
    else:
        return name[0:nbr] + " ..."


def format_date(date_: datetime = ""):
    tz = pytz.timezone("Africa/Nairobi")
    if date_ == "":
        date_ = datetime.now(tz)
    return format(date_.strftime("%Y-%m-%d %H:%M"))


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)
