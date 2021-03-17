from flask import Flask,render_template,request,redirect,url_for
import pyodbc

app = Flask(__name__)

server = "10.3.1.193,50404\\FJOMP"
database = "Winstat"
username = "admin"
password = "admin"

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()


def sql(type,sqlquery):

    cursor.execute(sqlquery)

    if type == "SELECT":
        result = cursor.fetchall()
    elif type == "INSERT":
        cnxn.commit()
        result = None

    return result


def checklogin(username,password):
    usrs = sql("SELECT","SELECT Tech_ID, Tech_Firstname, Tech_Lastname, Tech_Pwd FROM Technicians")
    for usr in usrs:
        if usr[0].strip() == username and usr[3] == None:
            #print("set " + usr[0] + " password to " + password)
            #print("UPDATE Technicians SET Tech_Pwd = '" + password + "' WHERE Tech_ID = '"+ username +"'")
            sql("INSERT","UPDATE Technicians SET Tech_Pwd = '" + password + "' WHERE Tech_ID = '"+ usr[0] +"'")

        elif username == usr[0].strip() and password == usr[3].strip():
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

@app.route("/parts",methods=["GET","POST"])
def parts():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    authenticated = False
    if request.cookies["auth"] == "true":
        authenticated = True

    theme,notheme = setTheme()

    allparts = []
    sqlq = []
    partn = ""
    partd = ""
    parta = None

    if request.method == 'POST':
        partn = request.form["part-parts"]
        partd = request.form["description-parts"]
        try:
            parta = request.form.getlist("active-parts")[0]
        except:
            parta = ""


        sqlquery = "SELECT * FROM Parts"
        sqlq=[]

        for x in sql("SELECT", sqlquery):
        #    print(x[0],x[1],x[14])
            if partn.lower() in x[0].lower() and partd.lower() in x[1].lower():
                sqlq.append(x)

        #print(sqlq)




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

    return render_template("parts.html",theme=theme,notheme=notheme,allparts=allparts,auth=authenticated,des=partd,par=partn)

@app.route("/delivnotes", methods=["GET","POST"])
def delivnotes():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    sqlq = []
    Dict = {}

    if request.method == 'POST':
        delivnote = request.form["delivnotename-delivnote"]

        sqlquery = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_no ='"+delivnote+"'")
        sqlq=[]
        priceGroup={}
        if sqlquery:
            for x in sqlquery:
                sqlq.append(x)

                Dict["storenum"] = x[0].strip()
                Dict["number"] = x[1]
                Dict["storename"] = x[2].strip()
                Dict["referens"] = x[3].strip()
                Dict["date"] = x[4]
                Dict["sign"] = x[16].strip()
                Dict["notes"] = x[17].strip()
                Dict["freight"] = x[15]
                Dict["sentfrom"] = sql("SELECT", "SELECT * FROM Office WHERE OF_No = '"+str(x[23])+"'")
                print(x)

            z = sql("SELECT", "SELECT * FROM Customers WHERE Cust_CustID = '"+Dict["storenum"]+"'")
            priceGroup["pricegroup"] = sql("SELECT", "SELECT * FROM Pricegroups WHERE pg_no = '"+str(x[26])+"'")
            Dict["street"] = z[3].strip()
            Dict["zip"] = z[5].strip()
            Dict["city"] = z[6].strip()

    return render_template("delivnotes.html",theme=theme,notheme=notheme, sqlq=sqlq, Dict=Dict, priceGroup=priceGroup)

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
    return render_template("swapout.html",theme=theme,notheme=notheme)

@app.route("/lookup")
def lookup():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    return render_template("lookup.html",theme=theme,notheme=notheme)

@app.route("/settings",methods=["GET","POST"])
def settings():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    authenticated = False
    if request.cookies["auth"] == "true":
        authenticated = True
    theme,notheme = setTheme()

    techs = sql("SELECT","SELECT * FROM Technicians")
    vendors = sql("SELECT","SELECT * FROM Vendors")

    #print(techs)

    if request.method == 'POST':
        techid = request.form.getlist('id')
        techfirst = request.form.getlist('firstname')
        techlast = request.form.getlist('lastname')
        techoffice = request.form.getlist('office')
        techtech = request.form.getlist('tech')

        sqltechs = []
        updtechs = []

        for x in techs:
            sqltechs.append((x[0],x[1].strip(),x[2].strip(),str(x[4]),str(x[5])))

        print("=====================")
        for x in range(len(techid)):
            updtechs.append((techid[x],techfirst[x],techlast[x],techoffice[x],techtech[x]))

        deleteuser = [list(set(sqltechs) - set(updtechs))]
        newuser = [list(set(updtechs) - set(sqltechs))]

        for x in newuser[0]:
            if x[0] == "" or x[1] == "" or x[2] == "" or x[3] == "" or x[4] == "":
                pass
            else:
                sql("INSERT","INSERT INTO Technicians (Tech_ID,Tech_Firstname,Tech_Lastname,Tech_Office,Tech_Tech) VALUES ('" + x[0].upper()+"','"+ x[1]+"','"+ x[2]+"','"+ x[3]+"','"+ x[4]+"')")

        for x in deleteuser[0]:
            #print("DELETE FROM Technicians WHERE Tech_ID = '" + x[0] +"'")
            sql("INSERT","DELETE FROM Technicians WHERE Tech_ID = '" + x[0] +"'")

        return redirect(url_for("settings"))


    return render_template("settings.html",theme=theme,notheme=notheme,auth=authenticated,techs=techs,vendors=vendors)

@app.route("/settings/changepassword",methods=["GET","POST"])
def changepwd():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    if "loggedin" in request.cookies:
        usr = request.cookies.get('username')
    error = None
    print(usr)
    oldpass = sql("SELECT","SELECT Tech_Pwd FROM Technicians WHERE Tech_ID = '" + usr +"'")[0][0].strip()

    print(oldpass)

    if request.method == 'POST':
        oldpwd = request.form["oldpwd"]
        newpwd1 = request.form["newpwd"]
        newpwd2 = request.form["newpwd2"]

        print([oldpwd,newpwd1,newpwd2])
        if oldpwd == oldpass:
            if newpwd1 == newpwd2 and newpwd1 != "" and newpwd2 != "":
                sql("INSERT","UPDATE Technicians SET Tech_Pwd = '" + newpwd1 + "' WHERE Tech_ID = '"+ usr +"'")
                return render_template("passwordchanged.html",theme=theme,notheme=notheme)
            else:
                error = "Password don't match"
        else:
            error = "Invalid password"


    return render_template("changepwd.html",theme=theme,notheme=notheme,error=error)


app.run(host="0.0.0.0",port="80")
