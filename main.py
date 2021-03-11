from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)

def checklogin(username,password):
    #temporary csv file
    with open("usr.csv","r") as f:
        usrs = f.read().split("\n")
    for usr in usrs:
        if usr != "":
            u = usr.split(";")
            if u[0] == username and u[1] == password:
                return True
    return False

def setTheme():
    theme = request.cookies.get('theme')
    if theme != "dark" and theme != "light":
        theme = "light"
    if theme == "light":
        notheme = "dark"
    elif theme == "dark":
        notheme = "light"
    return theme,notheme

@app.route("/")
def main():
    if "loggedin" in request.cookies:
        usr = request.cookies.get('username')
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    with open("static/DB/s_parts.txt","r",encoding="ansi") as f:
        parts = f.read()

    return render_template("landing.html",cookie=usr,theme=theme,notheme=notheme)

@app.route("/login",methods=["GET","POST"])
def login():
    error = None
    if request.method == 'POST':
        check = request.form.get("check")
        if checklogin(request.form['username'],request.form['password']):
            with open("static/authuser.csv","r",encoding="utf-8") as f:
                authusr = f.read().strip().split("\n")
            auth = False
            if request.form['username'] in authusr:
                auth = True
            return render_template("loginscript.html",auth=auth,checkbox=check,username=request.form['username'])
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
    with open("static/DB/s_parts.txte","r",encoding="ansi") as f:
        partse = f.read().strip().split("\n")

    with open("static/DB/s_parts.txt","r",encoding="ansi") as f:
        parts = f.read().split("\n")

    for x in partse:
        print([x[1:4].strip(), x[5:12].strip(), x[22:52].strip(), x[52:55].strip(),x[55:65].strip(), x[65:82].strip(), x[82:92].strip(), x[92:10].strip(), x[102:117].strip(), x[117:118].strip(), x[118:122].strip(), x[122:139].strip(), x[139:156].strip(), x[156:173].strip(), x[173:190].strip(), x[190:207].strip(), x[207:224].strip(), x[224:241].strip(), x[241:258].strip()])
    print("====================================")
    for x in parts:
        print([x[1:5].strip(), x[5:22].strip(), x[22:52].strip(),x[52:55].strip(), x[55:65].strip(), x[65:82].strip(), x[82:92].strip(), x[92:102].strip(), x[102:117].strip(), x[117:118].strip(), x[118:122].strip(), x[122:139].strip(), x[139:156].strip(), x[156:173].strip(), x[173:190].strip(), x[190:207].strip(), x[207:224].strip(), x[224:241].strip(), x[241:258].strip()])


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
    authenticated = False
    if request.cookies["auth"] == "true":
        authenticated = True
    theme,notheme = setTheme()
    return render_template("settings.html",theme=theme,notheme=notheme,auth=authenticated)




app.run(host="0.0.0.0",port="80")
