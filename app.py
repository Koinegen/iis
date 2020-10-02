from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", css_styles=url_for('static', filename="style.css"), jquery_s=url_for('static', filename="js.js"))


@app.route('/next')
def next():
    return render_template("next.html", css_styles=url_for('static', filename="style.css"), jquery_s=url_for('static', filename="js.js"))


if __name__ == '__main__':
    app.run()
