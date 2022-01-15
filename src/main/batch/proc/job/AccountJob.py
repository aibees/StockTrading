import json

import pythoncom
from module.core.StockAccount import StockAccount


class Job_Account:
    def __init__(self):
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
            print(data)
            # insert or update


