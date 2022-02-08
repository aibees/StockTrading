from datetime import datetime
import pymysql
from module.database.connect import Mysql
from ..sql.code import *


class CodeTransaction:
    def __init__(self):
        self.conn = Mysql()

    def SelectSectorCode(self, code, clcd):
        return self.conn.select(selectSectorCode, {'sysdiv': code, 'clcd': clcd})

    def selectCategoryCode(self, code, clcd, other):
        return self.conn.select(selectCategoryCode, {'sysdiv': code, 'clcd': clcd, 'other': other})
