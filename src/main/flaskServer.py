from flask import Flask, request, jsonify

from module.daeshin.Cybos import Cybos

app = Flask(__name__)
c = Cybos()

@app.route('/connection', methods=['GET', 'POST', 'DELETE'])
def handle_connect():
    c = Cybos()
    if request.method == 'GET':
        # check connection status
        return jsonify(c.connected())
    elif request.method == 'POST':
        # make connection
        data = request.get_json()
        _id = data['id']
        _pwd = data['pwd']
        _pwdcert = data['pwdcert']
        return jsonify(c.connect(_id, _pwd, _pwdcert))
    elif request.method == 'DELETE':
        # disconnect
        res = c.disconnect()
        c.kill_client()
        return jsonify(res)

@app.route('/code', methods=['GET'])
def get_NameToCode():
    c = Cybos()
    return {'code' : c.get_codeToName(request.args.get('name'))}

@app.route('/stockcandles', methods=['GET'])
def handle_stockcandles():
    c = Cybos()
    c.avoid_reqlimitwarning()
    stockcode = request.args.get('code')
    n = request.args.get('n')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not (n or date_from):
        return 'Need to provide "n" or "date_from" argument.', 400
    stockcandles = c.get_chart(stockcode, target='A', unit='D', n=n, date_from=date_from, date_to=date_to)
    return jsonify(stockcandles)

@app.route('/account', methods=['GET'])
def show_current_stock():
    c = Cybos()
    c.avoid_reqlimitwarning()
    return jsonify(c.getAccountList())



if __name__ == "__main__":
    app.run()

