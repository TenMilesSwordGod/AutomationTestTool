from datetime import datetime

from att_fw import __att_version__
from att_fw.backend.att_cli_configs import ATTCLIConfig
from att_testlib.base.basic_utils import AttLogger, CommsLib
from att_test_scripts.local_tools.sqlite.sqlite_steps import SQLiteDB, sqlite3


class ATT_Prepare(AttLogger):
    def __init__(self, test_campaign, test_bench_config=ATTCLIConfig.DEFAULT_BENCH_CONFIG,
                 campaign_id=None, test_case=None,
                 component_parameter=None, optional_parameter=None,
                 user=None, email="example@example.com", rerun=False,
                 **kwargs):
        super().__init__()
        self.test_campaign = test_campaign
        self.test_bench_config = test_bench_config,
        self.user = user
        self.email = email
        self.campaign_id = campaign_id
        self.test_case = test_case
        self.rerun = rerun
        self.component_parameter: dict = component_parameter
        self.optional_parameter: dict = optional_parameter
        self.current_time = CommsLib.transform_date_to_att_standard(datetime.now())

    def generate_campaign_id(self):
        self.logger.debug("current time: {}".format(self.current_time))

        return CommsLib.calculate_md5(str(self.current_time))

    def search_test_campaign(self):
        pass

    def search_test_bench_config(self):
        pass

    def update_optional_parameter_to_db(self, db_instance: SQLiteDB):
        for idx, (attrib, value) in enumerate(self.optional_parameter.items()):
            db_instance.insert_record(table_name=ATTCLIConfig.DEFAULT_TESTLIB_CONFIG_TABLE,
                                      values=(idx, attrib, value))

    def cache_sql_setup(self):
        config_db_instance = SQLiteDB(db_name=ATTCLIConfig.CACHE_DB_PATH)
        self.logger.debug("start to set db.")
        try:
            # check db table
            # storage campaign info
            if not config_db_instance.table_exists(table_name=ATTCLIConfig.CAMPAIGN_TABLE):
                config_db_instance.create_table(table_name=ATTCLIConfig.CAMPAIGN_TABLE,
                                                columns=ATTCLIConfig.CAMPAIGN_TABLE_COLUMNS)

            # storage testcase details
            if not config_db_instance.table_exists(table_name=ATTCLIConfig.TESTCASE_TABLE):
                config_db_instance.create_table(table_name=ATTCLIConfig.TESTCASE_TABLE,
                                                columns=ATTCLIConfig.TESTCASE_TABLE_COLUMNS)

            # storage system details
            if not config_db_instance.table_exists(table_name=ATTCLIConfig.ATT_SYSTEM_TABLE):
                config_db_instance.create_table(table_name=ATTCLIConfig.ATT_SYSTEM_TABLE,
                                                columns=ATTCLIConfig.ATT_SYSTEM_TABLE_COLUMNS)

            # create a tmp table for current 
            config_db_instance.create_table(table_name=ATTCLIConfig.DEFAULT_TESTLIB_CONFIG_TABLE,
                                            columns=ATTCLIConfig.TESTLIB_TABLE_COLUMNS)

            # clear the db env
            # clear the testlib config table
            config_db_instance.truncate_table(table_name=ATTCLIConfig.DEFAULT_TESTLIB_CONFIG_TABLE)
            # clear the system global environment table
            config_db_instance.truncate_table(table_name=ATTCLIConfig.ATT_SYSTEM_TABLE)

            if self.optional_parameter:
                self.update_optional_parameter_to_db(config_db_instance)

            # create a new record for storage campaign
            if not self.rerun:
                config_db_instance.insert_record(table_name=ATTCLIConfig.CAMPAIGN_TABLE,
                                                 values=(self.campaign_id, str(self.optional_parameter),
                                                         self.current_time, None, None, None, None, None, None))
            else:
                if res:= config_db_instance.select_records(table_name=ATTCLIConfig.CAMPAIGN_TABLE,
                                                        condition="campaign_id='{}'".format(self.campaign_id)):
                    self.logger.info("found existed campaign id: {}".format(self.campaign_id))
                    self.logger.debug(res)
                else:
                    self.logger.info("campaign id: {} not found in db! start to create a new one".format(
                        self.campaign_id))
                    config_db_instance.insert_record(table_name=ATTCLIConfig.CAMPAIGN_TABLE,
                                                     values=(self.campaign_id, str(self.optional_parameter),
                                                             self.current_time, None, None, None, None, None, None))
            # load system global parameters
            # like [if configurate the adb serial, 
            #       serial should be a common argument for testlib and can be used by self,
            #       and these arguments also used by self.arguments.serial
            #       for example in testlib steps:
            #           when init one step class, self.arguments will found global parameters from db: att_system
        except sqlite3.IntegrityError as e:
            raise Exception(f"meet error:{str(e)}, because of campaign_id has been existed")
        finally:
            config_db_instance.close()

    def start_up(self):
        self.logger.info("=====================================================")
        self.logger.info("******** start to run Automation Test Tool *********")
        self.logger.info("********   ATT Version: {}              ********".format(__att_version__))
        self.logger.info("=====================================================")
        # self.logger.info(self.generate_campaign_id())
        if not self.campaign_id:
            self.logger.info("No exist campaign id, start to create new one")
            self.campaign_id = self.generate_campaign_id()
        self.logger.info("current campaign id: {}".format(self.campaign_id))
        self.cache_sql_setup()
 

if __name__ == "__main__":
    att = ATT_Prepare(test_campaign="LoginTests", optional_parameter={"audio_name": "test.mp3",
                                                                      "audio_path": "/data/media/10",
                                                                      "dut_ip": "192.168.0.2",},
                      campaign_id="5de29102023eca38b55b3e2cd7622269ce", rerun=True)
    att.start_up()
