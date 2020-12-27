import tkinter as tk
from lib import main_worker
from lib.db_connector import DataBase

db = DataBase("./data/lena_db")
test_session = main_worker.TestSession(db)


def result(result_text):
    btn_da.pack_forget()
    btn_net.pack_forget()
    lbl.configure(text=f"{result_text}")
    lbl.pack(side=tk.TOP)
    btn_exit.configure(width=20, height=2, text="Выход", command=lambda: exit(0))
    btn_exit.pack(side=tk.BOTTOM)
    btn_again.configure(width=20, height=2, text="Еще раз?", command=lambda: again())
    btn_again.pack(side=tk.BOTTOM)


def again():
    global test_session
    test_session = main_worker.TestSession(db)
    start()


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
    btn_str.destroy()


def start():
    btn_exit.pack_forget()
    btn_again.pack_forget()
    btn_da.configure(width=20, height=2, text='Да', command=lambda: check_results(1))
    btn_da.pack(side=tk.LEFT)
    btn_net.configure(width=20, height=2, text='Нет', command=lambda: check_results(0))
    btn_net.pack(side=tk.RIGHT)
    question()


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Экспертная система")
    window.geometry('600x400')
    lbl = tk.Label(window, width=80, height=6, text="""Вас приветствует экспертна система,
         которая поможет вам с выбором линукс дистрибутива,
          который подходит именно вам\n
          Чтобы начать тест нажмите 'Начать'""", background="#555", foreground="#ccc")
    lbl.pack(side=tk.TOP)
    print(lbl)
    btn_da = tk.Button()
    btn_net = tk.Button()
    btn_exit = tk.Button()
    btn_again = tk.Button()
    btn_str = tk.Button(width=43, height=3, text="Начать!", command=lambda: start(), background="#555", foreground="#ccc",
              padx="15", pady="6", font="15")
    btn_str.pack(side=tk.BOTTOM, fill=tk.Y)
    window.mainloop()