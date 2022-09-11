from flask import Flask, render_template
from toto import main
app = Flask(__name__)


@app.route('/')
def hello():
    response = main()
    print("response")
    if(response != ""):
        print("its good")
    return render_template("./index.html", text="Hi there !!")
    
@app.route('/start')
def hello2():
    return render_template("./index2.html", text="This text goes inside the HTML")