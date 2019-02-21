from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "ahoj!"

app.run('127.0.0.1',5000,True)
