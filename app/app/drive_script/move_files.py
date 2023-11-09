from typing import List, Dict, Any
from .connect_to_drive import get_drive


def all_file_by_folder_id(folder_id: str = "root", file_id: str = "") -> List[Dict[str, Any]]:
    new_array = []
    file_list = (
        get_drive()
        .ListFile({"q": f"'{folder_id}' in parents and trashed=false"})
        .GetList()
    )
    if file_id == "":
        for file in file_list:
            new_array.append({"title": file["title"], "id": file["id"]})
    else:
        for file in file_list:
            if file["id"] == file_id:
                new_array.append({"title": file["title"], "id": file["id"]})
    return new_array


def move_all_file(old_folder_id: str, new_folder_id: str, file_id: str = "") -> bool:
    list_file = all_file_by_folder_id(old_folder_id, file_id)
    error: bool = False
    for file in list_file:
        new_file = {"title": file["title"], "parents": [{"id": new_folder_id}]}
        if (
            get_drive()
            .auth.service.files()
            .copy(fileId=file["id"], body=new_file)
            .execute()
        ):
            get_drive().CreateFile({"id": file["id"]}).Delete()
        else:
            error = True
    return error
