from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

def checklogin(username,password):
    #temporary csv file
    with open("usr.csv","r") as f:
        usrs = f.read().split("\n")
    for usr in usrs:
        if usr != "":
            u = usr.split(",")
            if u[0] == username and u[1] == password:
                return True
    return False

@app.route("/")
def main():
    print(request.cookies.get('username'))
    if "loggedin" in request.cookies:
        usr = request.cookies.get('username')
    else:
        return redirect(url_for("login"))
    return render_template("landing.html",cookie=usr)

@app.route("/login",methods=["GET","POST"])
def login():
    error = None
    if request.method == 'POST':
        check = request.form.get("check")
        if check == "":
            print(check)
        if checklogin(request.form['username'],request.form['password']):
            return render_template("loginscript.html",checkbox=check,username=request.form['username'])
        else:
            error = "Invalid username or password"
    usr = request.cookies.get('username')
    theme = request.cookies.get('theme')
    if theme != "dark" and theme != "light":
        print("new")
        theme = "light"

    if theme == "light":
        print(theme)
        notheme = "dark"
    elif theme == "dark":
        print(theme)
        notheme = "light"

    return render_template("login.html",error=error,username=usr,theme=theme,notheme=notheme)

app.run(host="0.0.0.0")
