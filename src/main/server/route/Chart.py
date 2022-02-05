# import sys
# sys.path.append('../')
import json

import win32com
from flask import request
from flask_restx import Resource, Api, Namespace
from module.core.Socket import TCPClient
from module.core.init import Init

Chart = Namespace('chart')


@Chart.route('')
class ChartRoot(Resource):

    def get(self) :
        agnt = Init()
        retcode = ""
        return retcode

@Chart.route('/<string:stockId>')
class StockChart(Resource):
    def get(self, stockId):
        data = {
            'stockId' : stockId
        }

        transport = TCPClient()
        transport.connect()
        transport.sendData(json.dumps(data))