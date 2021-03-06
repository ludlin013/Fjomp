from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
import os

server = "P2019\\WSData"
database = "winstat"
username = "sa"
password = "kamikaze"

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()

def setTheme():
    theme = request.cookies.get('theme')
    if theme != "dark" and theme != "light":
        theme = "light"
    if theme == "light":
        notheme = "dark"
    elif theme == "dark":
        notheme = "light"
    return theme,notheme

def sql(type,sqlquery):

    cursor.execute(sqlquery)

    if type == "SELECT":
        result = cursor.fetchall()
    elif type == "INSERT":
        cnxn.commit()
        result = None

    return result


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
    models = sql("SELECT","SELECT * FROM Models")
    parameters = sql("SELECT","SELECT * FROM Parameters")
    pgs = sql("SELECT", "SELECT * FROM Pricegroups")
    office = sql("SELECT", "SELECT * FROM Office")

    techs.sort(key = lambda x:x[0])
    vendors.sort(key = lambda x:x[0])

    mail = ["","",""]

    if not request.cookies.get("delivmail") or request.cookies.get("delivmail") == "":
        mail[0] = "nisse@ekabss.com"
    else:
        mail[0] = request.cookies.get("delivmail")


    if not request.cookies.get("irmail") or request.cookies.get("irmail") == "":
        mail[1] = "nisse@ekabss.com"
    else:
        mail[1] = request.cookies.get("irmail")

    if not request.cookies.get("projmail") or request.cookies.get("projmail") == "":
        mail[2] = "nisse@ekabss.com"
    else:
        mail[2] = request.cookies.get("projmail")


    return render_template("settings.html",mail=mail,theme=theme,notheme=notheme,pgs=pgs,auth=authenticated,techs=techs,vendors=vendors, server=server, database=database, parameters=parameters,models=models,office=office)

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



@app.route("/import",methods=["GET","POST"])
def importdata():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    with open("static/IMPORTPATH.txt") as f:
        currentPath = f.read()

    fileexist = None
    if request.method == 'POST':
        if not os.path.isfile(request.form["path"]):
            fileexist = "No file in that location"
        else:
            with open("static/IMPORTPATH.txt","w") as g:
                g.write(request.form["path"])
            return(redirect("/import"))

    return render_template("importdata.html",theme=theme,notheme=notheme, currentPath=currentPath, fileexist=fileexist)

app.config['UPLOAD_FOLDER'] = "./static/bugs/"

@app.route("/bugreport",methods=["GET","POST"])
def bugreport():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    if request.method == 'POST':
        os.mkdir("./static/bugs/"+request.form["title"])
        with open("./static/bugs/"+request.form["title"]+"/"+request.form["title"]+".txt","w") as g:
            g.write(request.form["desc"] + "\n\nSubmitted by: " +request.cookies["username"])

        f = request.files['sc']
        print([f.filename])
        if f.filename != "":
            if "png" in f.filename or "jpeg" in f.filename or "jpg" in f.filename or "tif" in f.filename or "gif" in f.filename or "":
                f.save("./static/bugs/"+request.form["title"]+"/"+request.form["title"]+".png")


    return render_template("bugreport.html",theme=theme,notheme=notheme)

@app.route("/viewreport",methods=["GET","POST"])
def viewreport():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    bugs = os.listdir("static/bugs")
    bugdict = {}

    for x in bugs:
        if x == "!klara":
            bugs.remove(x)

    for x in bugs:
        with open("static/bugs/"+x+"/"+x+".txt") as f:
            bugdict[x] = f.read()

    return render_template("viewreport.html",theme=theme,notheme=notheme, bugs=bugs, bugdict=bugdict)

@app.route("/reportdone",methods=["GET","POST"])
def reportdone():

    os.rename("static/bugs/"+request.form["report"], "static/bugs/!klara/"+request.form["report"])

    return ("",204)



@app.route("/savecp",methods=["GET","POST"])
def savevariable():

    print(request.form)

    for x in request.form:
        #print(x)
        sqlq = "UPDATE Parameters SET PM_Value = '" + request.form[x].strip() + "' WHERE PM_Name = '"+x.strip()+"'"
        #print(sqlq)
        sql("INSERT",sqlq)

    return ('', 204)


@app.route("/savemodels",methods=["GET","POST"])
def savemodels():

    print(len(request.form)//6)
    print(request.form)

    for x in range(len(request.form)//6):
        print(request.form[str(x)+"model"])
        sqlq = "UPDATE Models SET Mod_Vendor = '"+request.form[str(x)+"vend"].strip()+"', Mod_Model = '"+request.form[str(x)+"model"].strip()+"', Mod_Unittype = '"+request.form[str(x)+"type"].strip()+"', Mod_Cat = '"+request.form[str(x)+"cat"].strip()+"', ModChargemode = '"+request.form[str(x)+"cha"]+"' WHERE Mod_ID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)

    return ('', 204)

@app.route("/newmodel",methods=["GET","POST"])
def newmodel():

    print("newmodel")

    return ('', 204)

@app.route("/savepg",methods=["GET","POST"])
def savepg():

    count = len(request.form)//3
    print(count)

    for x in range(count):
        sqlq = "UPDATE Pricegroups SET pg_no = '"+request.form[str(x)+"no"]+"', pg_Descript = '"+request.form[str(x)+"name"].replace("'","''")+"' WHERE pg_ID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)
        sql("INSERT", sqlq)

    return ('', 204)

@app.route("/newpg",methods=["GET","POST"])
def newpg():

    sql("INSERT", "INSERT INTO Pricegroups (pg_no, pg_Descript) VALUES ('','')")

    newid = sql("SELECT","SELECT * FROM Pricegroups")

    for x in newid:
        if x[1] == "NEWPG":
            newid = str(x[2])
            break

    return newid

@app.route("/rempg",methods=["GET","POST"])
def rempg():

    sql("INSERT", "DELETE FROM Pricegroups WHERE pg_ID = '"+request.form["id"]+"'")

    return ('', 204)


@app.route("/savete",methods=["GET","POST"])
def savete():

    count = len(request.form)//6

    for x in range(count):
        sqlq = "UPDATE Technicians SET Tech_ID = '"+request.form[str(x)+"ids"].upper()+"', Tech_Firstname = '"+request.form[str(x)+"first"]+"', Tech_Lastname = '"+request.form[str(x)+"last"]+"', Tech_Office = '"+request.form[str(x)+"office"]+"', Tech_Tech = '"+request.form[str(x)+"tech"]+"' WHERE Tech_nID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)
        sql("INSERT", sqlq)

    return ('', 204)

@app.route("/newte",methods=["GET","POST"])
def newte():

    sql("INSERT", "INSERT INTO Technicians (Tech_ID, Tech_Firstname, Tech_Lastname, Tech_Office, Tech_Tech, Tech_Pwd) VALUES (' ','NEWTE',' ','1','1','')")

    newid = sql("SELECT","SELECT * FROM Technicians")

    for x in newid:
        print(x)
        if x[1].strip() == "NEWTE":
            newid = str(x[8])
            break

    return newid

@app.route("/remte",methods=["GET","POST"])
def remte():

    sql("INSERT", "DELETE FROM Technicians WHERE Tech_nID = '"+request.form["id"]+"'")

    return ('', 204)
