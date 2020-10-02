from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", css_styles=url_for('static', filename="style.css"),
                           jquery_s=url_for('static', filename="js.js"))


@app.route('/next', methods=['GET', 'POST'])
def next():
    if request.method == 'GET':
        return render_template("next.html", print_data="ЭТО ГЕТ ЗАПРОС",
                               css_styles=url_for('static', filename="style.css"),
                               jquery_s=url_for('static', filename="js.js"))
    if request.method == 'POST':
        request.get_data()
        return render_template("next.html", data=request.data, print_data="ЭТО ПОСТ ЗАПРОС",
                               css_styles=url_for('static', filename="style.css"),
                               jquery_s=url_for('static', filename="js.js"))


if __name__ == '__main__':
    app.run()
