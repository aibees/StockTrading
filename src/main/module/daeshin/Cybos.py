import os
import time

import win32com.client
from pywinauto import application

from .account.Account import Account

class Cybos:
    def __init__(self):
        self.obj_CpUtil_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpUtil_CpStockCode = win32com.client.Dispatch('CpUtil.CpStockCode')
        self.obj_CpUtil_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_CpSysDib_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.obj_CpTrade_CpTdUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        self.obj_CpSysDib_MarketEye = win32com.client.Dispatch('CpSysDib.MarketEye')
        self.obj_CpUtil_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_CpTrade_CpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

    def connect(self, id_, pwd, pwdcert, trycnt=10):
        if not self.connected():
            self.disconnect()
            # self.kill_client()
            app = application.Application()
            print(str(app))
            app.start(
                'C:\\DAISHIN\\Starter\\ncStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart'.format(
                    id=id_, pwd=pwd, pwdcert=pwdcert
                )
            )

        cnt = 0
        while not self.connected():
            print("Connection 대기중..." + str(cnt))
            if cnt > trycnt:
                return False
            time.sleep(10)
            cnt += 1
        return True

    def connected(self):
        b_connected = self.obj_CpUtil_CpCybos.IsConnect
        print("connected? " + str(b_connected))
        if b_connected == 0:
            return False
        return True

    def disconnect(self):
        if self.connected():
            self.obj_CpUtil_CpCybos.PlusDisconnect()
            return True
        return False

    def kill_client(self):
        os.system('taskkill /IM ncStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%ncStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')


    def avoid_reqlimitwarning(self):
        remainTime = self.obj_CpUtil_CpCybos.LimitRequestRemainTime
        remainCount = self.obj_CpUtil_CpCybos.GetLimitRemainCount(1)  # 시세 제한
        if remainCount <= 3:
            time.sleep(remainTime / 1000)


    def get_codeToName(self, name):
        return self.obj_CpUtil_CpStockCode.NameToCode(name)

    def get_stockstatus(self, code):
        if not code.startswith('A'):
            code = 'A' + code
        return {
            'control': self.obj_CpUtil_CpCodeMgr.GetStockControlKind(code),
            'supervision': self.obj_CpUtil_CpCodeMgr.GetStockSupervisionKind(code),
            'status': self.obj_CpUtil_CpCodeMgr.GetStockStatusKind(code),
        }

    def get_chart(self, code, target='A', unit='D', n=None, date_from=None, date_to=None):
        _fields = [0, 2, 3, 4, 5, 6, 8, 37]
        _keys = ['date', 'open', 'high', 'low', 'close', 'diff', 'volume', 'diffsign']

        self.obj_CpSysDib_StockChart.SetInputValue(0, target + code)  # 주식코드: A, 업종코드: U
        if n is not None:
            self.obj_CpSysDib_StockChart.SetInputValue(1, ord('2'))  # 0: ?, 1: 기간, 2: 개수
            self.obj_CpSysDib_StockChart.SetInputValue(4, n)  # 요청 개수
        if date_from is not None or date_to is not None:
            if date_from is not None and date_to is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(1, ord('1'))  # 0: ?, 1: 기간, 2: 개수
            if date_from is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(3, date_from)  # 시작일
            if date_to is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(2, date_to)  # 종료일
        self.obj_CpSysDib_StockChart.SetInputValue(5, _fields)  # 필드
        self.obj_CpSysDib_StockChart.SetInputValue(6, ord(unit))
        self.obj_CpSysDib_StockChart.SetInputValue(9, ord('1'))  # 0: 무수정주가, 1: 수정주가

        def req(prev_result):
            self.obj_CpSysDib_StockChart.BlockRequest()

            status = self.obj_CpSysDib_StockChart.GetDibStatus()
            msg = self.obj_CpSysDib_StockChart.GetDibMsg1()
            print("status : " + str(status))
            print("msg : " + msg)
            if status != 0:
                return None

            cnt = self.obj_CpSysDib_StockChart.GetHeaderValue(3)
            list_item = []
            for i in range(cnt):
                dict_item = {k: self.obj_CpSysDib_StockChart.GetDataValue(j, cnt - 1 - i) for j, k in enumerate(_keys)}

                # type conversion
                dict_item['diffsign'] = chr(dict_item['diffsign'])
                for k in ['open', 'high', 'low', 'close', 'diff']:
                    dict_item[k] = float(dict_item[k])
                for k in ['volume']:
                    dict_item[k] = int(dict_item[k])

                # additional fields
                dict_item['diffratio'] = round((dict_item['diff'] / (dict_item['close'] - dict_item['diff']) * 100), 3)
                dict_item['code'] = code
                dict_item['name'] = self.obj_CpUtil_CpCodeMgr.CodeToName(code)
                list_item.append(dict_item)
            return list_item

        # 연속조회 처리
        result = req([])
        while self.obj_CpSysDib_StockChart.Continue:
            self.avoid_reqlimitwarning()
            _list_item = req(result)
            if len(_list_item) > 0:
                result = _list_item + result
                if n is not None and n <= len(result):
                    break
            else:
                break
        return result
    
    
    def getAccountList(self):
        Acc = Account()
        return Acc.getAccountList(self.obj_CpTrade_CpTdUtil, self.obj_CpTrade_CpTd6033, self.avoid_reqlimitwarning)