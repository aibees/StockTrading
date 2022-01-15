
from module.core.init import Init
from module.core.Request import process


class StockAccount :
    def __init__(self):
        self.modules = Init()
        self.util = self.modules.getUtil()
        self.Td6033 = self.modules.getTd6033()
        self.accNum = self.util.AccountNumber[0] # 계좌번호
        self.flag = self.util.GoodsList(self.accNum, 1) # 주식상품 구분
        self.account = self.callAccountInfo()
        # 처음 init에서 계좌잔고와 정보 load
        # 이후에는 체결 이후나 필요할 시 update 하는 방식
    
    def getAccountInfo(self) :
        return self.account
    
    def callAccountInfo(self) :
        # param : 계좌번호, flag, 최대요청건수
        param = [self.accNum, self.flag[0], 10]
        result_obj = process(param, self.Td6033)
        
        cnt = result_obj.GetHeaderValue(7) # 결과 건수
        result = []
        for i in range(cnt) :
            item = {}
            code = result_obj.GetDataValue(12, i) #종목코드
            item['stockId'] = code
            item['stockNm'] = result_obj.GetDataValue(0, i) #종목명
            item['credit'] = result_obj.GetDataValue(1, i) #신용구분
            item['amount'] = result_obj.GetDataValue(7, i) #수량
            item['sellAmt'] = result_obj.GetDataValue(15, i) #매도가능수량
            item['cPrice'] = result_obj.GetDataValue(9, i) / item['amount'] #현재평가금액
            item['sPrice'] = result_obj.GetDataValue(17, i) #매수당시금액 (1주)
            result.append(item)
        
        self.account = result
        return result
        