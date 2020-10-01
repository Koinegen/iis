import pymysql
from pymysql.cursors import DictCursor
import json


class DataBase:
    def __init__(self, host, user, password, schema):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=schema, charset='utf8mb4',
                                    cursorclass=DictCursor)

    def __del__(self):
        self.conn.close()

    def select_lan_rows(self, lan=None):
        with self.conn.cursor() as cursor:
            if lan is not None:
                query = f"""SELECT * FROM languages WHERE lan_name='{lan}';"""
            else:
                query = """SELECT * FROM languages;"""
            cursor.execute(query)
            return [row for row in cursor.fetchall()]

    def select_execute(self, string):
        with self.conn.cursor() as cursor:
            cursor.execute(string)
            return [row for row in cursor.fetchall()]


if __name__ == '__main__':
    db = DataBase('localhost', 'lab1', 'elephant', 'lab1_schema')
    ans = db.select_lan_rows()
    print(ans)
    # ans = db.console_execute("""SELECT * FROM languages;""")[0]
    # print(ans)
    # ans2 = dict(ans)
    # print(ans2)
    print(ans[0].get('properties'))
    print(type(json.loads(ans[0].get('properties'))))
    # print(json.dumps({'script':True,'oop':True}))