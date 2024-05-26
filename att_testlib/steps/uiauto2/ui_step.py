
import uiautomator2 as u2

from att_testlib.base.basic_step import Base


class UiStep(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uidevice = u2.connect(serial=self.serial)