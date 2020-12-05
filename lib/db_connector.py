import json
import sqlite3


class DataBase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_question_by_property(self, prop_id):
        query = f"""SELECT questions FROM properties WHERE id={prop_id}"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return json.loads(cursor.fetchall()[0][0])

    def get_services_by_list_of_properties(self, prop: list):
        __str_prop_list = [str(i) for i in prop]
        query = f"""select ser_id from (select ser_id, count(*) as n from service_to_prop where prop_id in ({','.join(__str_prop_list)}) group by ser_id) a where n={len(__str_prop_list)};"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def get_sorted_property(self, service_list=None) -> list:
        if service_list is None:
            query = """SELECT prop_id, count(*) as res FROM service_to_prop group by prop_id order by res desc;"""
        else:
            __str_service_list = [str(i) for i in service_list]
            query = f"""SELECT prop_id, count(*) as res from service_to_prop where ser_id in ({','.join(__str_service_list)}) group by prop_id order by res desc;"""
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [row for row in cursor.fetchall()]

    # def select_lan_rows(self, lan=None):
    #     with self.conn.cursor() as cursor:
    #         if lan is not None:
    #             query = f"""SELECT * FROM languages WHERE lan_name='{lan}';"""
    #         else:
    #             query = """SELECT * FROM languages;"""
    #         cursor.execute(query)
    #         return [row for row in cursor.fetchall()]
    #
    # def select_execute(self, string):
    #     with self.conn.cursor() as cursor:
    #         cursor.execute(string)
    #         return [row for row in cursor.fetchall()]


if __name__ == '__main__':
    db = DataBase('..\data\katia_bd.db')

    print(db.get_sorted_property())
    print(db.get_sorted_property([4]))
    print(db.get_services_by_list_of_properties([4]))
    print(db.get_question_by_property(4))
