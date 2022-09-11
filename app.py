from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("./index.html", text="This text goes inside the HTML")

@app.route('/start')
def hello2():
    return render_template("./index2.html", text="This text goes inside the HTML")