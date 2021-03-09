from flask import Flask,render_template,request

app = Flask(__name__)

def checklogin(username,password):
    print(username)
    print(password)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    error = None
    if request.method == 'POST':
        if checklogin(request.form['username'],
            request.form['password']):
            return main()
        else:
            error = "Invalid"
    return render_template("login.html")

app.run(host="0.0.0.0")
