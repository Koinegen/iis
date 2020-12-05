from lib.db_connector import DataBase
import json
import random
from collections import defaultdict


class TestSession:
    def __init__(self, db: DataBase):
        self.db = db
        self.answers = []
        self.result = []
        self.sorted_property_list = []
        self.last_prop = None
        self.used_prop = []
        self.properties_count = self.db.get_services_count()

    def accept_answer(self, ans_num):
        if ans_num == 1:
            self.answers.append(self.last_prop)

    def check_results(self):
        # TODO: Подумать над этой функцией!!!!
        self.result = self.db.get_services_by_list_of_properties(self.answers)
        if len(self.result) == 1:
            __result_service = self.db.get_service_by_id(self.result[0])
            return f"Вам определенно стоит попробовать {__result_service}!"
        if (len(self.answers) > 0) and (len(self.result) == 0):
            return f"Поздравляю, вы меня победили, можете гордится собой, однако про язык вы ничего не узнаете"
        elif len(self.answers) == 0:
            if len(self.result) == 2:
                __result_service1 = self.db.get_service_by_id(self.result[0])
                __result_service2 = self.db.get_service_by_id(self.result[1])
                return f"Вам стоит присмотреться к этим двум языкам или даже их связке: {__result_service1} и {__result_service2}"
            elif len(self.result) > int(self.properties_count / 2):
                return f"Вы вообще уверены что хотите заниматься программированием?"
        else:
            return False

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
        try:
            prop_id = self.sorted_property_list[0][1][random.randint(0, len(self.sorted_property_list[0][1]) - 1)]
        except IndexError:
            return False
        questions = self.db.get_question_by_property(prop_id).get('questions')
        self.last_prop = prop_id
        self.used_prop.append(prop_id)
        return questions[random.randint(0, len(questions) - 1)]


if __name__ == '__main__':
    db = DataBase("../data/katia_bd.db")

    sess = TestSession(db)
    print(sess.get_question())
    #sess.accept_answer(1)

