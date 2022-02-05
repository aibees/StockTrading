from module.core.Request import process

class StockChart:

    # code는 list 방식으로 따로 들어와서 request에 obj와 같이 넣는다.
    def RequestFromTo(self, codes, obj, date, caller):
        result_obj = process(codes, obj)





