from db_connector import DataBase
import json
import random
from collections import defaultdict


class TestSession:
    def __init__(self, db: DataBase, cookies):
        self.db = db
        self.cookies = cookies
        self.properties = {}
        self.answers = []
        self.result = []
        self.languages = {}
        self.sorted_property_list = []
        self.last_prop = None
        self.used_prop = []
        self.properties_count = None
        # self.__get_sorted_properties()
        #self._get_all_properties()
        #self._get_all_langs()

    def accept_answer(self, ans_num):
        if ans_num == 1:
            self.answers.append(self.last_prop)

    def check_results(self):
        self.result = self.db.get_langs_by_list_of_properties(self.answers)
        if len(self.result) == 1:
            return f"Вам определенно стоит попробовать {self.result[0]}!"
        if (len(self.properties) > 0) and (len(self.result) == 0):
            return f"Поздравляю, вы меня победили, можете гордится собой, однако про язык вы ничего не узнаете"
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

    def __remove_property(self):
        for i in self.sorted_property_list:
            for j in self.used_prop:
                if j in i[1]:
                    i[1].remove(j)

    def __get_sorted_properties(self):
        _temp_dict = defaultdict(lambda: [])
        if self.answers == []:
            _result = self.db.get_sorted_property()
        else:
            _result = self.db.get_sorted_property(self.answers)
        for _row in _result:
            _temp_dict[_row[1]].append(_row[0])
        self.sorted_property_list = list(_temp_dict.items())

    def get_question(self):
        self.__get_sorted_properties()
        if self.last_prop is not None:
            self.__remove_property()
        self.sorted_property_list = list(filter(lambda x: True if x[1] != [] else False, self.sorted_property_list))
        prop_id = self.sorted_property_list[0][1][random.randint(0, len(self.sorted_property_list[0][1]) - 1)]
        questions = self.db.get_question_by_property(prop_id).get('questions')
        self.last_prop = prop_id
        self.used_prop.append(prop_id)
        return questions[random.randint(0, len(questions) - 1)]


if __name__ == '__main__':
    db = DataBase("../data/katia_bd.db")

    sess = TestSession(db, "123")
    print(sess.get_question())
    # sess.accept_answer(1)
    print(sess.get_question())
