import pythoncom

from flask_restx import Resource, Api, Namespace
from module.core.StockAccount import StockAccount

Account = Namespace('account')


@Account.route('')
class AccountRoot(Resource):
    def get(self):
        return "null"


@Account.route('/<string:Id>')
class detailInAccount(Resource):
    def get(self, stockId):
        return {
            'stockId': stockId
        }
