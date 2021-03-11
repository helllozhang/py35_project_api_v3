import pymysql
from common.handler_conf import conf

class HandlerDB:
    def __init__(self,*args,**kwargs):
        self.con = pymysql.Connect(
            host=conf.get('mysql', 'host'),
            port=conf.getint('mysql', 'port'),
            user=conf.get('mysql', 'user'),
            password=conf.get('mysql', 'password'),
            charset='utf8',
            # cursorclass=pymysql.cursors.DictCursor
            *args, **kwargs
        )

    def find_all(self,sql):
        """返回查询到的所有数据"""
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self,sql):
        """返回一条数据"""
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self,sql):
        """sql执行完后,返回数据条数"""
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        self.con.close()


if __name__ == '__main__':
    sql = "SELECT * FROM futureloan.member LIMIT 5;"
    db = HandlerDB()
    res = db.find_one(sql)
    print(res)