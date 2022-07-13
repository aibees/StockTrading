import datetime as dt

class Account: 
    def __init__(self) :
        pass
        
    def getAccountList(self, obj_util, obj_6033, avoid, param=None):
        trade_init = obj_util.TradeInit(0)
        if trade_init != 0:
            return None
        
        acc = obj_util.AccountNumber[0]
        accFlag = obj_util.GoodsList(acc, 1)
        
        obj_6033.SetInputValue(0, acc)
        obj_6033.SetInputValue(1, accFlag[0])
        obj_6033.SetInputValue(2, 50)
        
        def req(prev_result):
            obj_6033.BlockRequest()
            status = obj_6033.GetDibStatus()
            msg = obj_6033.GetDibMsg1()
            print("status : " + str(status))
            print("msg : " + msg)
            if status != 0:
                return None
            
            cnt = obj_6033.GetHeaderValue(7)
            list_item = []
            dicflag1 = {
                         ord(' '): '현금',
                         ord('Y'): '융자',
                         ord('D'): '대주',
                         ord('B'): '담보',
                         ord('M'): '매입담보',
                         ord('P'): '플러스론',
                         ord('I'): '자기융자',
                         }

            worktime = dt.datetime.now()
            workDate = str(worktime.year) + str(worktime.month).rjust(2, '0') + str(worktime.day)
            workHour = worktime.hour

            for i in range(cnt):
                item = {}
                code = obj_6033.GetDataValue(12, i)  # 종목코드
                item['code'] = code
                item['name'] = obj_6033.GetDataValue(0, i)  # 종목명
                item['ymd'] = workDate
                item['hour'] = workHour
                # item['현금신용'] = dicflag1[obj_6033.GetDataValue(1,i)] # 신용구분
                # print(code, '현금신용', item['현금신용'])
                item['balance'] = obj_6033.GetDataValue(7, i)  # 체결잔고수량
                item['sellcnt'] = obj_6033.GetDataValue(15, i)
                item['contract'] = obj_6033.GetDataValue(17, i)  # 체결장부단가
                item['buyprice'] = item['contract'] * item['balance']
                item['curprice'] = obj_6033.GetDataValue(9, i)
                item['curprofit'] = obj_6033.GetDataValue(10, i)
                item['yield'] = round(obj_6033.GetDataValue(11, i), 2)
                list_item.append(item)
            
            return list_item
        
        result = req([])
        while obj_6033.Continue:
            avoid()
            _list_item = req(result)
            if len(_list_item) > 0:
                result = _list_item + result
            else:
                break
        return result
            
