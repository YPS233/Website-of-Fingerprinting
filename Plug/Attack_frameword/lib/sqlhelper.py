# -*- coding:utf-8 -*-
import MySQLdb

class DBHelper():
    def excute_ddl_sql(self, dbname, sql):
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='806800',
            port=3306,
            charset='utf8',
            db=dbname
        )
        cursor = conn.cursor()
        try:
            res = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return res
        except Exception as e:
            cursor.close()
            conn.close()
            print(e)
            return 0

    def excute_dql_sql(self, dbname, sql, mode='single'):
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='806800',
            port=3306,
            charset='utf8',
            db=dbname)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            if mode == 'single':
                res = cursor.fetchone()
                cursor.close()
                conn.close()
                return res
            else:
                res = cursor.fetchall()
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            cursor.close()
            conn.close()
            print(e)

if __name__ == '__main__':
    db = DBHelper()
    print(db.excute_dql_sql('showsafe', "select * from job_status where url='http://192.168.25.143/'", mode='mu'))