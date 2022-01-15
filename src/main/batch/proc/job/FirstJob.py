import pythoncom

from module.core.init import Init
from module.core.Request import process


def FirstJob() :
    print("FIrst Job in another file")
    target = ['A090710', 'A005930']
    for t in target :
        Daeshin_currCheck(t)


def Daeshin_currCheck(subject) :
    print("Daeshin Stock Batch started")
    pythoncom.CoInitialize()
    obj = Init()
    param = [subject]
    g_objCodeMgr = obj.getMngAgnt()
    result_obj = process(param, obj.getStockAgnt())

    item = {}
    item['종목명']= g_objCodeMgr.CodeToName(subject)
    item['현재가'] = result_obj.GetHeaderValue(11)  # 종가
    item['대비'] =  result_obj.GetHeaderValue(12)  # 전일대비
    print(item)
    
    pythoncom.CoUninitialize()
