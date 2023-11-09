from app.drive_script.connect_to_drive import get_drive


def get_folder_file_id_by_name(folder_name: str, folder_id: str = "root") -> str:
    drive = get_drive()
    file_list = drive.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()

    for file in file_list:
        if file["title"] == folder_name:
            folder_id = file["id"]
            return folder_id

