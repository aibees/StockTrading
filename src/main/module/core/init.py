import win32event
import win32com.client
import pythoncom


class Init:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):  # Foo 클래스 객체에 _instance 속성이 없다면
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):  # Foo 클래스 객체에 _init 속성이 없다면
            print("__init__ is called\n")
            cls._init = True
            self.initModule()

    def initModule(self):
        self.agnt_Acc = win32com.client.Dispatch("CpTrade.CpTdUtil")

        print("initTrade")
        self.agnt_Trade = win32com.client.Dispatch("CpTrade.CpTd6033")

        print("initStock")
        self.agnt_Stock = win32com.client.Dispatch("DsCbo1.StockMst")

        print("initManager")
        self.agnt_Mng = win32com.client.Dispatch('CpUtil.CpCodeMgr')

        print("initTd6033")
        self.agnt_Td6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

        print("initChart")
        self.agnt_Chart = win32com.client.Dispatch("CpSysDib.StockChart")

    def getAccAgnt(self):
        return self.agnt_Acc

    def getTradeAgnt(self):
        return self.agnt_Trade

    def getStockAgnt(self):
        return self.agnt_Stock

    def getMngAgnt(self):
        return self.agnt_Mng

    def getTd6033(self):
        return self.agnt_Td6033

    def getChart(self):
        return self.agnt_Chart
