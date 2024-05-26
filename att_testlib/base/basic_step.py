from abc import abstractmethod
from typing import Any, NoReturn

from loguru import logger as lg

from att_testlib.base.basic_errors import AttTestError
from att_testlib.base.basic_utils import AttLogger


class StepResponse:
    def __init__(self):
        self._ok = False
        self._data = None

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, status: bool):
        self._ok = status

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Any):
        self._data = data


class Base(AttLogger):
    CRITICAL = True

    def __init__(self, critical: bool = CRITICAL, logger=None):
        self.critical = critical
        self.logger = logger
        self.response = StepResponse()
        # test phone
        self.serial = None

    @abstractmethod
    def do(self) -> NoReturn:
        # 为测试的步骤api
        pass

    @abstractmethod
    def check(self) -> bool:
        # 为验证最终结果
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        try:
            self.do()
        except Exception as e:
            if self.critical:
                raise AttTestError(f"{str(e)}")
            else:
                self.response.ok = False
        else:
            self.response.ok = self.check()
        return self.response


if __name__ == "__main__":
    resp = StepResponse()
    resp.ok = True
    print(resp.ok)
    resp.ok = False
    print(resp.ok)

    class StepDemo(Base):
        def __init__(self, name: str, value: int, **kwargs):
            super().__init__(**kwargs)
            self.name = name
            self.value = value

        def do(self):
            self.logger.info("use name: {}".format(self.name))
            self.logger.info("use value: {}".format(self.value))
            self.response.data = 1 / self.value

        def check(self):
            if self.value == 10:
                self.response.ok = True
            else:
                self.response.ok = False
            self.logger.info("test self.respose.ok: {}".format(self.response.ok))
            return self.response.ok
    test_list = [{"name": "zhangfei", "value": 0},
                 {"name": "guanyu", "value": 0, "critical": False},
                 {"name": "liubei", "value": 10},
                 {"name": "caocao", "value": 11}]
    for testdata in test_list:
        try:
            StepDemo(logger=lg, **testdata)()
        except Exception as e:
            lg.debug("===================================")
            print(str(e))
            lg.debug("===================================")
