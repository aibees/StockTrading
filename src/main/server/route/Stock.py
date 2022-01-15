from flask_restx import Resource, Namespace

Stock = Namespace('Stock')


@Stock.route('')
class StockRoot(Resource):

    def get(self):
        return 'stock root'


@Stock.route('/<string:stockId>')
class StockById(Resource):

    def get(self, stockId):
        return {'id': stockId}
