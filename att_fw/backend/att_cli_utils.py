import os
import sys
from typing import Dict, List

import typer
from rich import print

from att_testlib.base.basic_utils import CommsLib
from att_fw.backend.att_cli_configs import ATTCLIConfig


class LocalActions:
    def __init__(self):
        self.workdir = os.getcwd()
        self.bench_folder = self.__get_testsuites_bench_folder()
        self.campaign_folder = self.__get_testsuites_campaign_folder()
        self.case_folder = self.__get_testsuites_case_folder()

    def __get_testsuites_bench_folder(self):
        return os.path.join(self.workdir, 'att_test_suites', 'bench')

    def __get_testsuites_campaign_folder(self):
        return os.path.join(self.workdir, 'att_test_suites', 'campaign')

    def __get_testsuites_case_folder(self):
        return os.path.join(self.workdir, 'att_test_suites', 'case')


class CallBackFunctions:
    @staticmethod
    def campaign_name_callback(campaign_name: str):
        if not campaign_name:
            print(f"[red bold]{"*" * 60} [/red bold]")
            print("[red bold][ATT ERROR]            please input campaign name!!![/red bold]")
            print(f"[red bold]{"*" * 60} [/red bold]")
            raise typer.Exit(code=1)

        return campaign_name

    @staticmethod
    def bench_config_name_callback(bench_config_name: str):
        if bench_config_name != ATTCLIConfig.default_bench_config:
            if bench_files:= CommsLib.get_folder_files(LocalActions().bench_folder):
                for file in bench_files:
                    if bench_config_name in file:  
                        return bench_config_name
                    else:
                        print(f"[red bold]{"*" * 60} [/red bold]")
                        print("[red bold][ATT ERROR]recommand bench files: {}, not found bench_file:{}[/red bold]".
                              format(bench_files, f"{bench_config_name}.xml"))
                        print(f"[red bold]{"*" * 60} [/red bold]")
                        raise typer.Exit(code=1)
            else:
                raise typer.Exit(code=1)

        return bench_config_name

    @staticmethod
    def parse_extend_args_to_sql(args: List[str]) -> Dict[str, str]:
        otp_dict = {}
        if not args:
            return otp_dict
        for arg in args:
            key_value = arg.split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                otp_dict[key.strip()] = value.strip()
            else:
                typer.echo(f"Invalid OTP format: {arg}. Use --otp key=value.")
                raise typer.Exit(code=1)
        return otp_dict


class StartUpUtils:
    @staticmethod
    def set_python_path(path):
        if path not in sys.path:
            sys.path.append(path)


if __name__ == "__main__":
    CallBackFunctions.bench_config_name_callback('default_bench_config')
