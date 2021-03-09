from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def main():
    pass


app.run(host="0.0.0.0")
