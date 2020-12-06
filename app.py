from flask import Flask, render_template, url_for, request, make_response, session
from lib import main_worker
from lib.db_connector import DataBase

app = Flask(__name__)
db = DataBase('localhost', 'lab1', 'elephant', 'lab1_schema')
test_session = []


@app.route('/', methods=['GET'])
def index():
    test_session.clear()
    test_session.append(main_worker.TestSession(db))
    response = make_response(render_template("index.html", css_styles=url_for('static', filename="style.css"),
                           jquery_s=url_for('static', filename="js.js")))
    return response


@app.route('/next', methods=['GET', 'POST'])
def next():
    if request.method == 'GET':
        __question = test_session[0].get_question()
        return render_template("next.html", print_data=__question,
                               css_styles=url_for('static', filename="style.css"),
                               jquery_s=url_for('static', filename="js.js"))
    if request.method == 'POST':
        request.get_data()
        __answer = request.data
        if __answer == b'yes':
            test_session[0].accept_answer(1)
        elif __answer == b'no':
            test_session[0].accept_answer(0)
        elif __answer == b'dont_know':
            test_session[0].accept_answer(2)
        else:
            raise Exception
        __result = test_session[0].check_results()
        if __result:
            return render_template("result.html", data=__result, print_data="Вы завершили тест!",
                                   css_styles=url_for('static', filename="style.css"),
                                   jquery_s=url_for('static', filename="js.js"))
        __next_question = test_session[0].get_question()
        if not __next_question:
            return render_template("result.html", data="Мы не смогли подобрать для вас сервис(", print_data="Вы завершили тест!",
                                   css_styles=url_for('static', filename="style.css"),
                                   jquery_s=url_for('static', filename="js.js"))
        return render_template("next.html", data="Выберите ответ:", print_data=__next_question,
                               css_styles=url_for('static', filename="style.css"),
                               jquery_s=url_for('static', filename="js.js"))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
