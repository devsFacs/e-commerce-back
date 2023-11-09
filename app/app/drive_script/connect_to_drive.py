import os
from typing import Optional

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

_drive: Optional[GoogleDrive] = None

client_json_path = "/app/credentials/client_secrets.json"
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_json_path


def get_drive() -> GoogleDrive:
    global _drive
    if not _drive:
        g_auth = GoogleAuth()
        g_auth.LoadCredentialsFile("/app/credentials/files/my_credentials.txt")
        _drive = GoogleDrive(g_auth)

        # Authenticate if they're not there
        g_auth.LocalWebserverAuth()

    _drive.GetAbout()
    _drive.auth.SaveCredentialsFile("/app/credentials/files/my_credentials.txt")
    return _drive
