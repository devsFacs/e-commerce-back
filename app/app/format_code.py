import black
import os

import isort


def format_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    code_to_format = file.read()
                formatted_code = black.format_str(code_to_format, mode=black.FileMode())
                with open(file_path, "w") as file:
                    file.write(formatted_code)
    print(f"ALL file has been formatted using black.")


# Replace 'your_directory' with the path to the directory containing your .py files
format_files_in_directory("/app")
