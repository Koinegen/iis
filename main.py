import tkinter as tk
from lib import main_worker
from lib.db_connector import DataBase

db = DataBase("./data/lena_db")
test_session = main_worker.TestSession(db)
# db = DataBase("./data/lena_db")


def result(result_text):
    lbl.configure(text=f"{result_text}")
    lbl.grid(column=1, row=1)
    tk.Button(width=20, height=2, text="Выход", command=lambda: exit(0)).grid(column=1, row=2)
    tk.Button(width=20, height=2, text="Еще раз?", command=lambda: again()).grid(column=1, row=3)


def again():
    global test_session
    test_session = main_worker.TestSession(db)
    question()


def check_results(answer):
    test_session.accept_answer(answer)
    __result = test_session.check_results()
    if __result:
        result(__result)
    else:
        question()


def question():
    __question = test_session.get_question()
    if not __question:
        result("ne udalos'")
    lbl.configure(text=__question)
    tk.Button(width=20, height=2, text='Да', command=lambda: check_results(1)).grid(column=1, row=2)
    tk.Button(width=20, height=2, text='Нет', command=lambda: check_results(0)).grid(column=1, row=3)
    # __result = self.test_session.check_results()
    # if __result:
    #     self.result(__result)




if __name__ == '__main__':
    window = tk.Tk()
    window.title("Экспертная система")
    lbl = tk.Label(window, width=44, height=5, text="""Вас приветствует экспертна система,
         которая поможет вам с выбором линукс дистрибутива,
          который подходит именно вам\n
          Чтобы начать тест нажмите 'Начать'""")
    lbl.grid(column=1, row=1)
    print(lbl)
    tk.Button(width=43, height=3, text="Начать!", command=lambda: question()).grid(column=1, row=2)
    window.mainloop()