import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

from .test_folder import get_folder_file_id_by_name
from .connect_to_drive import get_drive

parent = Path(__file__).resolve().parent.parent / ""
sys.path.append(str(parent))


class ListFolderAndFile:
    # Make parameter folder_id empty if you want to check list
    # of files in root folder
    def __init__(self):
        self.drive = get_drive()
        print(self.drive)

    def by_folder_id(self, folder_id: str = "root") -> List[Dict[str, Any]]:
        new_array = []
        file_list = self.drive.ListFile(
            {"q": f"'{folder_id}' in parents and trashed=false"}
        ).GetList()
        for file in file_list:
            new_array.append({"title": file["title"], "id": file["id"]})

        return new_array

    # Make parameter folder_name empty if you want to check list
    # of files in root folder
    def by_folder_name(self, folder_name: str = "root") -> List[Dict[str, Any]]:
        new_array = []
        if folder_name == "root":
            return self.by_folder_id()
        else:
            folder_id = get_folder_file_id_by_name(folder_name)
            if folder_id:
                file_list = self.drive.ListFile(
                    {"q": f"'{folder_id}' in parents and trashed=false"}
                ).GetList()
                for file in file_list:
                    new_array.append({"title": file["title"], "id": file["id"]})
            else:
                print("Folder not found")

            return new_array

    def delete_folders_file(self, folder_name: str = "root") -> None:
        lists: List[Dict[str, Any]] = self.by_folder_name(folder_name)
        if lists:
            for item in lists:
                self.drive.auth.service.files().update(
                    fileId=item["id"], addParents="root"
                ).execute()
            print(f"All files and folder at {folder_name} deleted")
        else:
            print("Folder empty")
