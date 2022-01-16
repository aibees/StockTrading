import json
from datetime import datetime
import pymysql.err
import pythoncom
from module.core.StockAccount import StockAccount
from module.database.Transaction.AccountTransaction import AccountTransaction

class Job_Account:
    def __init__(self):
        self.__trans = AccountTransaction()
        self.id = 'Job_Account'
        self.cron = {
            'year': '*',
            'month': '*',
            'day': '*',
            'hour': '*',
            'minute': '*',
            'second': '0'
        }

    def getId(self):
        return self.id

    def getCronTime(self):
        return self.cron

    def getJob(self):
        return self.process

    def process(self):
        print("Daeshin Stock Batch started")
        print('#####################################')
        pythoncom.CoInitialize()
        account = StockAccount()
        result = account.getAccountInfo()
        pythoncom.CoUninitialize()

        for data in result:
            data['last_update'] = datetime.now()
            data['own_yn'] = 'Y' # 현 계좌에 있는 데이터 옮기니 소유값 하드코딩해도 무방
            # 기존데이터 조회
            prev_data = self.__trans.SelectByCode(data['stockId'])
            # master
            # insert or update
            print(prev_data)
            if len(prev_data) == 0:
                print("insert")
                data['seq'] = 1
                print(data)
                self.__trans.InsertMaster(data)
                # insert new detail
                self.__trans.InsertDetail(data)
            else:
                # already exist data.
                print("update")
                data['seq'] = prev_data[0]['seq']+1
                print(data)
                self.__trans.UpdateMaster(data)
                # insert new detail
                self.__trans.InsertDetail(data)
