from datetime import datetime
import hashlib
import os
import yaml
from xml.etree import ElementTree as ET

import loguru


class AttLogger:
    def __init__(self):
        self.logger = loguru.logger
        # self.logger.remove()
        # self.logger.add(sink=,format="{time} {level} {message}", colorize=True)


class CommsLib:
    @staticmethod
    def calculate_md5(input_string):
        hash_object = hashlib.md5(str(input_string).encode())
        md5_hash = hash_object.hexdigest()

        return md5_hash

    @staticmethod
    def transform_date_to_att_standard(date):
        format = "%Y-%m-%d %H:%M:%S"  
        if isinstance(date, datetime):
            date = datetime.strftime(date, format)
        elif isinstance(date, str):
            date = datetime.strptime(date, format)
        else:
            raise Exception("date time error")

        return date

    @staticmethod
    def read_xml_from_file(path):
        tree = ET.parse(path)

        return tree.getroot()

    @staticmethod
    def read_yaml_from_file(path):
        with open(path, 'r', encoding="utf-8") as fstream:
            datas = yaml.load(stream=fstream)

        return datas

    @staticmethod
    def get_folder_files(folder):
        all_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files


if __name__ == "__main__":
    # s = CommsLib.get_folder_files("att_test_suites/campaign")
    # print(s)
    CommsLib.transform_date_to_att_standard()