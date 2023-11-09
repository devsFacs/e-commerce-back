from typing import List, Dict, Any

from .insert_data import create_spreadsheet, create_sheets, insert_data, get_data

possible_col = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM",
                "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]


def trasnform_list(data: list) -> List[Dict[Any, Any]]:
    """
    This methode transforme a list of list to a dick, and the first row is a key and the other is a value
    :param data: list of list
    :return: dict of the element in the list
    """
    all_data = []
    for index, item in enumerate(data):
        if index != 0:
            all_data.append(dict(zip(data[0], item)))
    return all_data


def diff_order_by_key(list_data: List[Dict[Any, Any]], filter_key: str, key: str) -> bool:
    for x in list_data:
        if str(x[f"{key}"]) == str(filter_key):
            return True
    return False


def create_worksheet(name: str, sheet_name: list):
    spreadsheet_id = create_spreadsheet(name=name)
    for sheet in sheet_name:
        create_sheets(speadsheet_id=spreadsheet_id, title=sheet)


def write_data_title(spreadsheet_id: str, sheet_name: str, all_columns: list):
    try:
        insert_data(spreadsheetId=spreadsheet_id,
                    last_row=1,
                    begin_title="A",
                    end_title=str(possible_col[len(all_columns) - 1]),
                    value=all_columns,
                    sheet=sheet_name)
    except Exception as e:
        print(e)


def write_all_data(spreadsheet_id: str, sheet_name: str, all_data: list, key_unique):
    end = str(possible_col[len(all_data[0])])
    data_script_ = get_data(spreadsheet_id=spreadsheet_id, sheet=sheet_name, begin="A", end=end, row=1)
    last_row: int = 2
    if len(data_script_) != 0:
        data_script = trasnform_list(data_script_)
        for row_index, row in enumerate(all_data):
            if diff_order_by_key(data_script, row[key_unique], key_unique):
                continue
            else:
                all_row = []
                for row_cols, col in enumerate(row):
                    key = data_script_[0][row_cols]
                    all_row.append(row[key])
                insert_data(spreadsheetId=spreadsheet_id, last_row=last_row, begin_title="A",
                            end_title=end, value=all_row, sheet=sheet_name)
                last_row += 1
