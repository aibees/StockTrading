import win32com.client
from flask import render_template, make_response, request, redirect
from flask_restx import Resource, Namespace
from module.database.Transaction.CodeTransaction import CodeTransaction

import json

from module.database.Transaction.StockTransaction import StockTransaction

Stock = Namespace('Stock')
g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')

@Stock.route('')
class StockRoot(Resource):

    def get(self):
        return ''


@Stock.route('/<string:stockId>')
class StockById(Resource):

    def get(self, stockId):
        return {'id': stockId}


@Stock.route('/interests')
class StockShow(Resource):
    def get(self):
        tran_code = CodeTransaction()
        tran_stock = StockTransaction()
        sectorBox = tran_code.SelectSectorCode('stock', 'sector')
        interestCodes = tran_stock.SelectWholeInterestCode()

        return make_response(render_template('stockcode.html', sectors=sectorBox, resultData=interestCodes))

    def post(self):
        param = {
            'sector': request.form.get("combo1"),
            'class': request.form.get("combo2"),
            'code': request.form.get("code"),
            'name': g_objCodeMgr.CodeToName(request.form.get("code"))
        }
        tran = StockTransaction()
        tran.InsertInterestCode(param)
        return redirect("/stock/interests")


@Stock.route('/interests/search')
class StockSearchData(Resource):
    def get(self):
        param = {
            'sector': request.args.get("sector"),
            'class': ('' if request.args.get("class") is None else request.args.get("class"))
        }
        print(param)
        tran = StockTransaction()
        searchData = tran.SelectWholeInterestCodeByCondition(param)
        return json.dumps(searchData)


@Stock.route('/interests/combo')
class StockComboData(Resource):
    def get(self):
        clcd = request.args.get('clcd')
        other = request.args.get('other')
        tran = CodeTransaction()
        sectorBox = tran.selectCategoryCode('stock', clcd, other)
        return json.dumps(sectorBox)



