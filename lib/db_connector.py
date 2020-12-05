import json
import sqlite3


class DataBase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_question_by_property(self, prop_id):
        self.conn = sqlite3.connect(self.db_path)
        query = f"""SELECT questions FROM properties WHERE id={prop_id}"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        resp = cursor.fetchall()
        return json.loads(str(resp[0][0]))

    def get_services_by_list_of_properties(self, prop: list):
        self.conn = sqlite3.connect(self.db_path)
        __str_prop_list = [str(i) for i in prop]
        query = f"""select ser_id from (select ser_id, count(*) as n from service_to_prop where prop_id in ({','.join(__str_prop_list)}) group by ser_id) a where n={len(__str_prop_list)};"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def get_sorted_property(self, service_list=None) -> list:
        self.conn = sqlite3.connect(self.db_path)
        if service_list is None:
            query = """SELECT prop_id, count(*) as res FROM service_to_prop group by prop_id order by res desc;"""
        else:
            __str_service_list = [str(i) for i in service_list]
            query = f"""SELECT prop_id, count(*) as res from service_to_prop where ser_id in ({','.join(__str_service_list)}) group by prop_id order by res desc;"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [row for row in cursor.fetchall()]

    def get_services_count(self):
        self.conn = sqlite3.connect(self.db_path)
        query = """SELECT count(*) as res from services;"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()[0][0]

    def get_service_by_id(self, service_id):
        self.conn = sqlite3.connect(self.db_path)
        query = f"""SELECT name from services where id={service_id};"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()[0][0]


if __name__ == '__main__':
    db = DataBase('..\data\katia_bd.db')

    print(db.get_service_by_id(2))
    print(db.get_services_count())
    print(db.get_sorted_property())
    print(db.get_sorted_property([4]))
    print(db.get_services_by_list_of_properties([4]))
    print(db.get_question_by_property(4))
