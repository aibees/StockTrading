from flask import Flask
from flask_restx import Api
from server.route import Chart, Stock, Account, Batch


class TradeServer :
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.__addNameSpace()

    def __addNameSpace(self):
        self.api.add_namespace(Chart, '/chart')
        self.api.add_namespace(Account, '/account')
        self.api.add_namespace(Stock, '/stock')
        self.api.add_namespace(Batch, '/batch')

    def run(self):
        self.app.run(debug=True, host='localhost', port=2635)