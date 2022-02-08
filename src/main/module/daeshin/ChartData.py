import datetime

import win32com.client as winClient

from module.core.Request import process


class CharData:
    def __init__(self, name, obj):
        self.obj = winClient.Dispatch(obj)
        self.name = name

    def RequestToday(self, code):
        date = datetime.datetime.now().strftime('%Y%m%d')
        order = [0, 1, 2, 3, 5, 6, 9]
        param = [code, ord('1'), date, date, [0, 2, 3, 4, 5, 8], ord('D'), ord('1')]
        process(order, param, self.obj, self)
        # self.obj.SetInputValue(0, code)
        # self.obj.SetInputValue(1, ord('1')) # ord(1') : 기간으로 받기 / ord('2') : 갯수로 받기
        # self.obj.SetInputValue(2, date)
        # self.obj.SetInputValue(3, date)
        # self.obj.SetInputValue(5, [0, 2, 3, 4, 5, 8])
        # self.obj.SetInputValue(6, ord('D'))
        # self.obj.SetInputValue(9, ord('1'))

    def updates(self):
        data = {
            "date": self.obj.GetDataValue(0, 0), # 일자
            "open": self.obj.GetDataValue(1, 0), # 시가
            "high": self.obj.GetDataValue(2, 0), # 고가
            "lows": self.obj.GetDataValue(3, 0), # 저가
            "clos": self.obj.GetDataValue(4, 0), # 종가
            "vols": self.obj.GetDataValue(5, 0)  # 거래량
        }

        print(data)
