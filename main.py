from flask import Flask,render_template,request,redirect,url_for
import pyodbc

app = Flask(__name__)

server = "10.3.1.193,50404\\FJOMP"
database = "Winstat"
username = "admin"
password = "admin"
cursor = ""

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()


def sql(type,sqlquery):

    cursor.execute(sqlquery)

    if type == "SELECT":
        result = cursor.fetchall()
    elif type == "INSERT":
        mydb.commit()

    return result



def checklogin(username,password):
    usrs = sql("SELECT","SELECT Tech_ID, Tech_Firstname, Tech_Lastname, Tech_Pwd FROM Technicians")
    for usr in usrs:
        if username == usr[0].strip() and password == usr[3].strip():
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

def createcsv():
    with open("static/DB/s_parts.txt","r",encoding="ansi") as f:
        parts = f.read().rstrip().split("\n")

    with open("static/DB/s_parts.txte","r",encoding="ansi") as f:
        partse = f.read().strip().split("\n")

    allparts = []

    for x in parts:
        groupcode = x[1:1+4].strip()
        artid = x[5:5+17].strip()
        name = x[22:22+30].strip()
        qty = x[52:52+3].strip()
        price1 = x[65:65+17].strip()
        lp = x[102:102+15].strip()
        type = x[117:117+1].strip()
        price2 = x[124:124+17].strip()
        price3 = x[141:141+17].strip()
        price4 = x[158:158+17].strip()
        price5 = x[175:175+17].strip()
        price6 = x[192:192+17].strip()
        price7 = x[209:209+17].strip()
        price8 = x[226:226+17].strip()
        price9 = x[243:243+17].strip()

        Dict = {
        "groupcode" : x[1:1+4].strip(),
        "artid" : x[5:5+17].strip(),
        "name" : x[22:22+30].strip(),
        "qty" : x[52:52+3].strip(),
        "price1" : x[65:65+17].strip(),
        "lp" : x[102:102+15].strip(),
        "type" : x[117:117+1].strip(),
        "price2" : x[124:124+17].strip(),
        "price3" : x[141:141+17].strip(),
        "price4" : x[158:158+17].strip(),
        "price5" : x[175:175+17].strip(),
        "price6" : x[192:192+17].strip(),
        "price7" : x[209:209+17].strip(),
        "price8" : x[226:226+17].strip(),
        "price9" : x[243:243+17].strip()
        }
        if Dict not in allparts:
            allparts.append(Dict)

    for x in partse:
        groupcode = x[1:1+4].strip()
        artid = x[5:5+17].strip()
        name = x[22:22+30].strip()
        qty = x[52:52+3].strip()
        price1 = x[65:65+17].strip()
        lp = x[102:102+15].strip()
        type = x[117:117+1].strip()
        price2 = x[124:124+17].strip()
        price3 = x[141:141+17].strip()
        price4 = x[158:158+17].strip()
        price5 = x[175:175+17].strip()
        price6 = x[192:192+17].strip()
        price7 = x[209:209+17].strip()
        price8 = x[226:226+17].strip()
        price9 = x[243:243+17].strip()

        Dict = {
        "groupcode" : x[1:1+4].strip(),
        "artid" : x[5:5+17].strip(),
        "name" : x[22:22+30].strip(),
        "qty" : x[52:52+3].strip(),
        "price1" : x[65:65+17].strip(),
        "lp" : x[102:102+15].strip(),
        "type" : x[117:117+1].strip(),
        "price2" : x[122:122+17].strip(),
        "price3" : x[139:139+17].strip(),
        "price4" : x[156:156+17].strip(),
        "price5" : x[173:173+17].strip(),
        "price6" : x[190:190+17].strip(),
        "price7" : x[207:207+17].strip(),
        "price8" : x[224:224+17].strip(),
        "price9" : x[241:241+17].strip()
        }

        if Dict not in allparts:
            allparts.append(Dict)

    allparts.sort(key = lambda x:x["artid"])

    sqlparts = sql("SELECT","SELECT * FROM Parts")

    with open("static/units.csv","w") as f:
        for n in sqlparts:
            for x in n:
                f.write(str(x).strip()+";")
            f.write("\n")

    return allparts


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
            createcsv()
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

    allparts = []

    sqlq = sql("SELECT","SELECT * FROM Parts")

    for x in sqlq:

        Dict = {}

        Dict["artid"] = x[0].strip()
        Dict["name"] = x[1].strip()
        Dict["lp"] = str(x[12]).strip()
        Dict["qty"] = str(x[7]).strip()
        Dict["price1"] = str(x[6]).strip()
        Dict["inactive"] = str(x[14]).strip()
        Dict["lastusd"] = str(x[9]).strip()
        Dict["lastupd"] = str(x[17]).strip()

        allparts.append(Dict)

    allparts.sort(key = lambda x:x["artid"])

    return render_template("parts.html",theme=theme,notheme=notheme,allparts=allparts)

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
