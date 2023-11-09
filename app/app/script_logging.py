import logging
from datetime import date, datetime
import os
from datetime import date

"""
class ScriptLogging:
    def __init__(self, filename: str, level=logging.INFO):
        self.filename = filename
        self.level = level
        self.logger = None
        try:
            path = f'/app/log/{date.today()}'
            # Check whether the specified path exists or not
            is_exist = os.path.exists(path)
            if not is_exist:
                # Create a new directory because it does not exist
                os.makedirs(path)
                print(path)
                print("The new directory is created!")

            path = open(os.path.join(path, f"{filename}.log"), "w")
            print(path)
            logging.getLogger("uvicorn").propagate = False
            self.logger = logging.getLogger(filename)
            formatter = logging.Formatter('%(asctime)s : %(message)s')
            fileHandler = logging.FileHandler(path.name, mode="w")
            fileHandler.setFormatter(formatter)
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)

            self.logger.setLevel(self.level)
            self.logger.addHandler(fileHandler)
            self.logger.addHandler(streamHandler)

        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    def script_logging(self, log_type: str, message: str) -> None:

        if log_type == "info":
            logging.info(message)
        elif log_type == "error":
            logging.error(message)
"""


class ScriptLogging:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            path = f'/app/log/{date.today().strftime("%d-%m-%Y")}'
            # Check whether the specified path exists or not
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)
                print("The new directory is created!")

            logging.getLogger("uvicorn").propagate = False
            logging.basicConfig(
                filename=f'{path}/logging.log',
                level=logging.INFO,
                filemode="a",
            )
        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    def script_logging(self,filename, log_type: str, message: str) -> None:
        message_ = f"""
                ####################################
                {datetime.now()}:{filename}    
                ####################################
                """
        if log_type == "info":
            logging.info(message_+f"\n {message}")
        elif log_type == "error":
            logging.error(message)
