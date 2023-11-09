import os
from typing import Any
from googleapiclient.discovery import build
from google.oauth2 import service_account

from .test_folder import get_folder_file_id_by_name
from .list_folder_and_file import ListFolderAndFile
from .connect_to_drive import get_drive


def get_sertvice():
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "/app/credentials/credential.json", scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
    return service


def insert_data(
        spreadsheetId: str,
        last_row: int,
        begin_title: str,
        end_title: str,
        value: list,
        sheet: str,
):
    """
    for insert data from api to the google sheet
    :param spreadsheetId: id of the google spreadsheet
    :param last_row: the row number to insert data
    :param begin_title: the column
    :param end_title:
    :param value:
    :param sheet:
    :return:
    """

    range_ = f"{sheet}!{begin_title}{last_row}:{end_title}"
    values = [
        value,
    ]
    body = {"range": range_, "values": values, "majorDimension": "ROWS"}
    request = (
        get_sertvice().spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=range_,
            valueInputOption="USER_ENTERED",
            body=body,
        )
    )
    request.execute()


def get_data(spreadsheet_id: str, sheet: str, begin: str, end: str, row: int):
    """
    Use this to retrieve data from the Google spreadsheet
    :param spreadsheet_id: id of the spreadsheet
    :param sheet: name of the sheet
    :param begin: the start column to retrieve data
    :param end: the end column to retrieve data
    :param row: the row number
    :return: default return a list of all data row by row
    """
    range_ = f"{sheet}!{begin}{row}:{end}"
    result = (
        get_sertvice().spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    )
    rows = result.get("values", {})
    return rows


def insert_row(spreadsheet_id: str, sheet_id: str, last_row: int):
    sheet = get_sertvice().spreadsheets()
    spreadsheet_id = spreadsheet_id
    body_add = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': last_row,
                        'endIndex': last_row + 100,
                    },
                    "inheritFromBefore": True
                }
            }
        ]
    }

    sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body_add).execute()


def delete_row(spreadsheet_id: str, sheet_id: str, last_row: int):
    sheet = get_sertvice().spreadsheets()
    spreadsheet_id = spreadsheet_id
    body_delete = {
        'requests': [
            {
                'deleteDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': last_row,
                    },
                }
            }
        ]
    }

    sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body_delete).execute()


def get_sheet_id_by_name(spreadsheet_id: str, sheet_name: str):
    # sheet = service.spreadsheets()
    spreadsheet = get_sertvice().spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_id = None
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == sheet_name:
            sheet_id = _sheet['properties']['sheetId']
    return sheet_id


def create_spreadsheet(name: str) -> str:
    spreadsheet = {
        'properties': {
            'title': name
        }
    }
    spreadsheet = get_sertvice().spreadsheets().create(body=spreadsheet, field='spreadsheetId').execute()
    sheet_id = spreadsheet.get('spreadsheetId')
    return sheet_id


def create_sheets(speadsheet_id: str, title: str):
    request = {
        'requests': [
            {
                'addSheets': {
                    'properties': {
                        'title': title
                    }
                }
            }
        ]
    }
    get_sertvice().spreadsheets().batchUpdate(spreadsheetId=speadsheet_id, body=request).execute()


def check_if_folder_already_exists(folder_name: str, parent_id: str = "root") -> bool:
    list_folder_and_file = ListFolderAndFile()
    folder_lists = list_folder_and_file.by_folder_id(parent_id)
    for folder_list in folder_lists:
        if folder_list["title"] == folder_name:
            return True
    return False


def create_folder_with_test(folder_name: str, root_folder_id: str) -> str:
    exist_folder: bool = check_if_folder_already_exists(folder_name, root_folder_id)
    if not exist_folder:
        drive = get_drive()
        folder = drive.CreateFile(
            {
                "parents": [{"id": f"{root_folder_id}"}],
                "title": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
            }
        )
        folder.Upload()
        return folder["id"]
    else:
        return get_folder_file_id_by_name(folder_name, root_folder_id)


def upload_file_to_drive(filename: str, folder_id: str = "root") -> str:
    drive = get_drive()
    template = drive.CreateFile({"parents": [{"id": f"{folder_id}"}]})
    template.SetContentFile(filename)
    template.Upload()

    return filename
