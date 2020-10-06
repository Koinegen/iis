from db_connector import DataBase
import json
import random
import json


def get_random_property(db: DataBase):
    query = """SELECT * FROM properties ORDER BY RAND() LIMIT 1;"""
    ans = db.select_execute(query)
    print(ans)
    return ans


class TestSession:
    def __init__(self, db: DataBase, cookies):
        self.db = db
        self.cookies = cookies
        self.properties = {}
        self.answers = []
        self.result = []
        self.languages = {}
        self.last_prop = None
        self.properties_count = None
        self._get_all_properties()
        self._get_all_langs()

    def accept_answer(self, ans_num):
        if self.last_prop[1] == int(ans_num):
            self.answers.append(self.last_prop[0])

    def check_results(self):
        if len(self.result) == 1:
            return f"Вам определенно стоит попробовать {self.result[0]}!"
        if (len(self.properties) > 0) and (len(self.result) == 0):
            return f"Поздравляю, вы меня победили, можете гордится собой, однако про язык выничего не узнаете"
        elif len(self.properties) == 0:
            if len(self.result) == 2:
                return f"Вам стоит присмотреться к этим двум языкам или даже их связке: {self.result[0]} и {self.result[1]}"
            elif self.result > int(self.properties_count / 2):
                return f"Вы вообще уверены что хотите заниматься программированием?"
            elif self.result < int(self.properties_count / 2):
                return f"Вам стоит быть конкретнее, на данный момент вам подходят все вот эти языки: {', '.join(self.result)}"
            else:
                print('Some problem here')
                raise Exception
        else:
            return False

    def _accept_languages(self):
        for language in self.languages.items():
            accept = True
            for prop in self.answers:
                if language[1].get(prop) == 0:
                    accept = False
                elif language[1].get(prop) == 1:
                    pass
                else:
                    print(f"lan = {language}\n"
                          f"prop = {prop}")
                    raise Exception
            if accept:
                if language[0] not in self.result:
                    self.result.append(language[0])
            else:
                if language[0] in self.result:
                    self.result.remove(language[0])

    def _get_all_langs(self):
        ans = db.select_lan_rows()
        for lan in ans:
            print(lan)
            self.languages.update({lan.get("lan_name"): json.loads(json.loads(lan.get("properties")))})
        print(self.languages)

    def _get_all_properties(self):
        query = """SELECT * FROM properties;"""
        ans = db.select_execute(query)
        for prop in ans:
            print(prop)
            self.properties.update({prop.get('property'): {'if_true': prop.get('if_true'),
                                                           'questions':
                                                               json.loads(prop.get('questions')).get("quest")}})
        self.properties_count = len(self.properties)
        print(self.properties)

    def get_next_question(self):
        _property = self._get_random_property()
        _prop_name = _property[0]
        _questions = _property[1].get("questions")
        self.last_prop = (_prop_name, _property[1].get('if_true'),)
        self.properties.pop(_prop_name)
        return _questions[random.randint(0, len(_questions) - 1)]

    def _get_random_property(self):
        return list(self.properties.items())[random.randint(0, len(self.properties.items()) - 1)]


if __name__ == '__main__':
    db = DataBase('localhost', 'lab1', 'elephant', 'lab1_new_schema')

    #ans = get_random_property(db)
    # a = eval(json.loads(ans[0].get('questions')))
    # print(type(a))

    sess = TestSession(db, "123")
    a = sess.get_next_question()
    print(a)
    # a = sess.get_next_question()
    # print(a)
