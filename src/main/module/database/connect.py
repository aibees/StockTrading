from module.util.Config import Config
import pymysql


class Mysql:
    def __init__(self):
        self.checkSql = 'SELECT \'OK\' AS OK FROM DUAL'
        self.conf = Config()
        self.conn = None
        self.connection()

    def connection(self):
        self.conn = pymysql.connect(
            host=self.conf.getConfig('db_local', 'DB_HOST')
            , user=self.conf.getConfig('db_local', 'DB_USER')
            , port=3333
            , passwd=self.conf.getConfig('db_local', 'DB_PSWD')
            , db=self.conf.getConfig('db_local', 'DB_SCHM')
            , charset='utf8'
            , cursorclass=pymysql.cursors.DictCursor
        )

    def test(self):
        res = self.select(self.checkSql, None)
        return res

    # ----------------------------------
    # ------------ SELECT --------------
    def select(self, sql, params):
        return self.__fetch(sql, params)

    def __fetch(self, query, params):
        cursor = self.conn.cursor()
        cursor.execute(query, params)

        res = cursor.fetchall()  # fetchall : 조건에 맞는 모든 데이터 / fetchone : 조건에 맞는 데이터 중 1개
        return res

    # ----------------------------------

    # ----------------------------------
    # -------------- DML ---------------
    def insert(self, sql, params):
        self.__execute(sql, params)

    def update(self, sql, params):
        self.__execute(sql, params)

    def delete(self, sql, params):
        self.__execute(sql, params)

    def __execute(self, query, params):
        cursor = self.conn.cursor()
        cursor.execute(query, params)

        self.conn.commit()
        # self.conn.close()

    # ----------------------------------
