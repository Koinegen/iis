import json

import pymysql
from pymysql.cursors import DictCursor


class DataBase:
    def __init__(self, host, user, password, schema):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=schema, charset='utf8mb4',
                                    cursorclass=DictCursor)

    def __del__(self):
        self.conn.commit()
        self.conn.close()


    def insert_language(self, lan_name, *properties: str):
        with self.conn.cursor() as cursor:
            query1 = f"""INSERT IGNORE INTO languages(name)
          VALUES ("{lan_name}");"""
            cursor.execute(query1)
            for property in properties:
                query2 = f"""INSERT IGNORE INTO properties(property)
            VALUES ("{property}");"""
                cursor.execute(query2)

                query3 = f"""REPLACE INTO lab1_schema.lan_to_prop(lan_id,prop_id) 
SELECT languages.id, properties.id FROM lab1_schema.languages, lab1_schema.properties 
WHERE languages.name = "{lan_name}" 
AND properties.property = "{property}";"""

                cursor.execute(query3)

    def get_question_by_property(self, prop_id):
        query = f"""SELECT questions FROM lab1_schema.properties WHERE id={prop_id}"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return json.loads(cursor.fetchall()[0].get('questions'))

    def get_langs_by_list_of_properties(self, prop: list):
        __str_prop_list = [str(i) for i in prop]
        query = f"""select lan_id from (select lan_id, count(*) as n from lab1_schema.lan_to_prop where prop_id in ({','.join(__str_prop_list)}) group by lan_id) a where n={len(__str_prop_list)};"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return [row for row in cursor.fetchall()]

    def get_sorted_property(self, lan_list=None) -> list:
        if lan_list is None:
            query = """SELECT prop_id, count(*) as res FROM lab1_schema.lan_to_prop group by prop_id order by res desc;"""
        else:
            __str_lan_list = [str(i) for i in lan_list]
            query = f"""SELECT prop_id, count(*) as res from lab1_schema.lan_to_prop where lan_id in ({','.join(__str_lan_list)}) group by prop_id order by res desc;"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return [row for row in cursor.fetchall()]

    def insert_questions(self, prop, questions: list):
        __questions = json.dumps({"questions": questions}, ensure_ascii=False)
        query = f"""UPDATE lab1_schema.properties SET questions='{__questions}' WHERE property={prop}"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)

    def get_langs_count(self):
        query = """SELECT count(*) as res from lab1_schema.languages;"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            __result = cursor.fetchall()
            return __result.get("res")

    def get_language_by_id(self, lan_id):
        query = f"""SELECT name from lab1_schema.languages where id={lan_id};"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            __result = cursor.fetchall()
            return __result.get("name")



if __name__ == '__main__':
    db = DataBase('localhost', 'lab1', 'elephant', 'lab1_schema')
    #db.insert_language("java", "compile", "static_type", "high_level", "fast", "oop", "venv", "popular")
    # db.insert_language("python", "high_level", "popular", "web", "backend", "script", "oop")

    #print(db.get_langs_by_list_of_properties([4]))
    db.insert_questions("web", ["Хотите писать web???"])

    print(db.get_question_by_property(4))


    # db.add_new_property("frontend", 2, 1, ["Хотите писать скрипты для frontend-а?"])
    # ans = db.select_lan_rows()
    # print(ans)
    # ans = db.console_execute("""SELECT * FROM languages;""")[0]
    # print(ans)
    # ans2 = dict(ans)
    # print(ans2)
    # print(ans[0].get('properties'))
    # print(type(json.loads(ans[0].get('properties'))))
    # print(json.dumps({'script':True,'oop':True}))
