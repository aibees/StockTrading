from datetime import datetime
import pymysql
from module.database.connect import Mysql
from ..sql.account import *


class AccountTransaction:
    def __init__(self):
        self.conn = Mysql()

    def test(self):
        return self.conn.test()

    def SelectByCode(self, code):
        return self.conn.select(SelectMasterByCode, {'stockId': code})

    def InsertMaster(self, params):
        return self.conn.insert(InsertAccountMaster, params)

    def UpdateMaster(self, params):
        return self.conn.update(UpdateAccountMaster, params)

    def InsertDetail(self, params):
        return self.conn.update(InsertAccountDetail, params)