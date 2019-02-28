import time
import flask
from flask import Flask
from flask import Response
app = Flask(__name__)

@app.route('/')
def hello_world(): 
    now = time.asctime()
    XD=["a","b","c"]
    return flask.render_template("sample.html", now=str(now),arr=XD)

app.run('0.0.0.0', 5000, True)
