
from threading import Thread as t
from batch.start import start_test
from module.database.connect import Mysql
from server.flaskServer import TradeServer

if __name__ == '__main__' :
    print("==== DB TEST ====")
    mysql = Mysql()
    print(mysql.test())

    sched_thread = t(target=start_test)
    sched_thread.start()

    serv = TradeServer()
    serv.run()
