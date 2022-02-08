from datetime import datetime
import pymysql
from module.database.connect import Mysql
from ..sql.stock import *


class StockTransaction:
    def __init__(self):
        self.conn = Mysql()

    def InsertInterestCode(self, params):
        return self.conn.insert(InsertInterestCode, params)

    def SelectWholeInterestCode(self):
        return self.conn.select(SelectWholeInterestCode, None)

    def SelectWholeInterestCodeByCondition(self, params):
        return self.conn.select(SelectWholeInterestCodeByCondition, params)