from typing import Any

from sqlalchemy.orm import Session

from app import crud
from app.drive_script import create_folder_with_test, get_folder_file_id_by_name, \
    check_if_folder_already_exists, move_all_file, write_data_title, write_all_data, create_worksheet
from app.utils import check_table_info, check_columns_exist


def create_forlder_and_spreadsheet(db: Session) -> str:
    anne_univ = crud.anne_univ.get_actual_value(db)
    if anne_univ:
        anne_univ = anne_univ[0]
        print(anne_univ)
        schema = anne_univ.title
        foolder_name = f"annee {anne_univ.title}"
        is_exist = check_if_folder_already_exists(foolder_name)
        if not is_exist:
            parent_id = create_folder_with_test(foolder_name, "root")
            upload_file(schema, parent_id)
            upload_file("public", parent_id)
        return "Success"
    else:
        return "annee universitaire not found."


def upload_file(schema: str, parent_id: str):
    all_table = check_table_info(schema)
    spreadsheet_id = create_worksheet(schema, all_table)
    for table in all_table:
        write_title(spreadsheet_id, schema, table)
    move_all_file("root", parent_id, spreadsheet_id)


def write_title(spreadsheet_id: str, schema: str, table: str) -> Any:
    columns = check_columns_exist(schema, table)
    write_data_title(spreadsheet_id, table, columns)


def write_data_to_drive(db: Session) -> Any:
    anne_univ = crud.anne_univ.get_actual_value(db)
    if anne_univ:
        schema = anne_univ.title
        foolder_name = f"annee {anne_univ.title}"
        parent_id = get_folder_file_id_by_name(foolder_name)
        if parent_id:
            spreadsheet_id = get_folder_file_id_by_name("etudiants_et_matiers", parent_id)
            if spreadsheet_id:
                all_table = check_table_info(schema)
                for table in all_table:
                    write_data(spreadsheet_id, schema, table, "uuid")

                all_table = check_table_info("public")
                for table in all_table:
                    write_data(spreadsheet_id, "public", table, "uuid")
                return "Success"
            else:
                return "file not found."
        else:
            create_forlder_and_spreadsheet(db=db)

    else:
        return "annee universitaire not found."


def write_data(spreadsheet_id: str, schema: str, table: str, key: str) -> Any:
    all_data = crud.save.read_all_data(schema, table)
    write_all_data(spreadsheet_id=spreadsheet_id, sheet_name=table, all_data=all_data, key_unique=key)
