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

def setTheme():
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
    return theme,notheme

@app.route("/")
def main():
    if "loggedin" in request.cookies:
        usr = request.cookies.get('username')
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("landing.html",cookie=usr,theme=theme,notheme=notheme)

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
    theme,notheme = setTheme()

    return render_template("login.html",error=error,username=usr,theme=theme,notheme=notheme)

@app.route("/landing")
def landing():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("landing.html",theme=theme,notheme=notheme)

@app.route("/customers")
def customers():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("customers.html",theme=theme,notheme=notheme)

@app.route("/parts")
def parts():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("parts.html",theme=theme,notheme=notheme)

@app.route("/delivnotes")
def delivnotes():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("delivnotes.html",theme=theme,notheme=notheme)

@app.route("/ir")
def ir():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("ir.html",theme=theme,notheme=notheme)

@app.route("/swapouts")
def swapouts():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("swapouts.html",theme=theme,notheme=notheme)

@app.route("/lookup")
def lookup():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("lookup.html",theme=theme,notheme=notheme)

@app.route("/settings")
def settings():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("settings.html",theme=theme,notheme=notheme)




app.run(host="0.0.0.0")
