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
        self.properties_count = self.db.get_langs_count()

    def accept_answer(self, ans_num):
        if ans_num == 1:
            self.answers.append(self.last_prop)

    def check_results(self):
        # TODO: Подумать над этой функцией!!!!
        if self.answers == []:
            return False
        self.result = self.db.get_langs_by_list_of_properties(self.answers)
        print(f"result: {self.result}")
        print(f"answers: {self.answers}")
        if len(self.result) == 1:
            print(self.result)
            __result_language = self.db.get_language_by_id(self.result[0].get('lan_id'))
            return f"Вам определенно стоит попробовать {__result_language}!"
        if (len(self.answers) > 0) and (len(self.result) == 0):
            print("check 2")
            return f"Поздравляю, вы меня победили, можете гордится собой, однако про язык вы ничего не узнаете"
        elif len(self.answers) == 0:
            if len(self.result) == 2:
                print("check 3")
                __result_service1 = self.db.get_language_by_id(self.result[0].get('lan_id'))
                __result_service2 = self.db.get_language_by_id(self.result[1].get('lan_id'))
                return f"Вам стоит присмотреться к этим двум языкам или даже их связке: {self.result[0].get('lan_id')} и {self.result[1].get('lan_id')}"
            elif len(self.result) > int(self.properties_count / 2):
                print("check 4")
                return f"Вы вообще уверены что хотите заниматься программированием?"
        else:
            return False

    def __remove_property(self):
        __new_prop_list = []
        for i in self.sorted_property_list:
            __temp = [x for x in i[1] if x not in self.used_prop]
            __new_prop_list.append((i[0], __temp))
        self.sorted_property_list = __new_prop_list
        # for i in self.sorted_property_list:
        #     for j in self.used_prop:
        #         if j in i[1]:
        #             i[1].remove(j)

    def __get_sorted_properties(self):
        _temp_dict = defaultdict(lambda: [])
        if self.answers == []:
            _result = self.db.get_sorted_property()
        else:
            __temp = [x.get('lan_id') for x in self.result]
            _result = self.db.get_sorted_property(__temp)
        for _row in _result:
            _temp_dict[_row['res']].append(_row['prop_id'])
        self.sorted_property_list = list(_temp_dict.items())
        print(_result)
        print(f"lol: {self.sorted_property_list}")

    def get_question(self):
        self.__get_sorted_properties()
        if self.last_prop is not None:
            self.__remove_property()
        self.sorted_property_list = list(filter(lambda x: True if x[1] != [] else False, self.sorted_property_list))
        print(f"kek: {self.sorted_property_list}")
        try:
            prop_id = self.sorted_property_list[0][1][random.randint(0, len(self.sorted_property_list[0][1]) - 1)]
        except IndexError:
            return False
        questions = self.db.get_question_by_property(prop_id).get('questions')
        self.last_prop = prop_id
        self.used_prop.append(prop_id)
        return questions[random.randint(0, len(questions) - 1)]


if __name__ == '__main__':
    # db = DataBase('localhost', 'lab1', 'elephant', 'lab1_schema')
    #
    # #ans = get_random_property(db)
    # # a = eval(json.loads(ans[0].get('questions')))
    # # print(type(a))
    #
    # sess = TestSession(db, "123")
    # print(sess.get_question())
    # sess.accept_answer(1)
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())
    # print(sess.get_question())

    a = [(3, [10, 51]), (2, [4, 9, 52, 54, 57, 61]), (1, [8, 16, 53, 60])]
    used_prop = []
    new_a = []
    for i in a:
        _temp = [x for x in i[1] if x not in used_prop]
        new_a.append((i[0], _temp))
    print(new_a)


    # a = sess.get_next_question()
    # print(a)
    # a = sess.get_next_question()
    # print(a)
