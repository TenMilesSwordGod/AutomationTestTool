from pathlib import Path
# from enum import Enum


class ATTCLIConfig:
    ATT_ROOT_PATH = Path().resolve()
    ATT_CACHE_FOLDER = ".att-cache"


    # ATT DB
    DEFAULT_CACHE_CONFIG_DB = "att_config.db"
    CACHE_DB_PATH = Path(ATT_ROOT_PATH) / Path(ATT_CACHE_FOLDER) / Path(DEFAULT_CACHE_CONFIG_DB)

    DEFAULT_TESTLIB_CONFIG_TABLE = "optional_parameter"
    TESTLIB_TABLE_COLUMNS = "id INT PRIMARY KEY, " + "attribute TINYTEXT, " + "value TEXT"
    TESTLIB_TABLE_COLUMNS_ATTRIB = "attribute"
    TESTLIB_TABLE_COLUMNS_VALUE = "value"
    # NOT USE
    DEFAULT_EQUIPMENT_CONFIG_TABLE = "component_parameter"
    EQUIPMENT_TABLE_COLUMNS = "id INT PRIMARY KEY, " + "equipment TINYTEXT, " + "attribute TINYTEXT, " + "value TEXT"

    CAMPAIGN_TABLE = "campaign"
    CAMPAIGN_TABLE_COLUMNS = "campaign_id TINYTEXT PRIMARY KEY, " + "override_parameter TEXT, " +\
    "start_time TEXT NOT NULL, " + "stop_time TEXT, " + "total_cases INT, " + "actually_run INT, "+\
        "pass INT, " + "fail INT, " + "pass_rate FLOAT " 

    TESTCASE_TABLE = "testcase"
    TESTCASE_TABLE_COLUMNS = "testcase_id TINYTEXT PRIMARY KEY, " + "campaign_id TINYTEXT, " + "result TINYTEXT, " +\
        "test_log TEXT, " + "FOREIGN KEY (campaign_id) REFERENCES {}(campaign_id)".format(CAMPAIGN_TABLE)

    # bench
    DEFAULT_BENCH_CONFIG = "default_bench_config.xml"

    # ATT System
    # for system global parameters
    ATT_SYSTEM_TABLE = "att_system_table"
    ATT_SYSTEM_TABLE_COLUMNS = "attr_name TINYTEXT PRIMARY KEY, " + "attr_value TINYTEXT" 


if __name__ == "__main__":
    print(ATTCLIConfig.TESTCASE_TABLE_COLUMNS)