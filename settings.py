from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
import os

server = "10.3.1.193,50404\\FJOMP"
database = "Winstat"
username = "admin"
password = "admin"

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

    techs.sort(key = lambda x:x[0])
    vendors.sort(key = lambda x:x[0])

    if request.method == 'POST':
        techid = request.form.getlist('id')
        techfirst = request.form.getlist('firstname')
        techlast = request.form.getlist('lastname')
        techoffice = request.form.getlist('office')
        techtech = request.form.getlist('tech')
        print(techoffice)
        print(techtech)
        sqltechs = []
        updtechs = []

        for x in techs:
            sqltechs.append((x[0],x[1].strip(),x[2].strip(),str(x[4]),str(x[5])))

        print("=====================")
        print(range(len(techid)))
        for x in range(len(techid)):
            print(x)
            updtechs.append((techid[x],techfirst[x],techlast[x],techoffice[x],techtech[x]))

        deleteuser = [list(set(sqltechs) - set(updtechs))]
        newuser = [list(set(updtechs) - set(sqltechs))]
        #print(sqltechs[12])
        print(updtechs)

        for x in newuser[0]:
            if x[0] == "" or x[1] == "" or x[2] == "" or x[3] == "" or x[4] == "":
                pass
            else:
                sql("INSERT","INSERT INTO Technicians (Tech_ID,Tech_Firstname,Tech_Lastname,Tech_Office,Tech_Tech) VALUES ('" + x[0].upper()+"','"+ x[1]+"','"+ x[2]+"','"+ x[3]+"','"+ x[4]+"')")

        for x in deleteuser[0]:
            #print("DELETE FROM Technicians WHERE Tech_ID = '" + x[0] +"'")
            sql("INSERT","DELETE FROM Technicians WHERE Tech_ID = '" + x[0] +"'")

        return redirect(url_for("settings"))


    return render_template("settings.html",theme=theme,notheme=notheme,auth=authenticated,techs=techs,vendors=vendors, server=server, database=database, parameters=parameters,models=models)

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


@app.route("/savetechs",methods=["GET","POST"])
def savetechs():

    n = 0
    for x in request.form:
        n = x.replace("tech","").replace("office","")

    n = int(n) + 1

    alltechsql = sql("SELECT","SELECT Tech_ID FROM Technicians")
    alltech = []
    newtech = []

    for x in alltechsql :
        alltech.append(x[0])

    print(n)
    print(request.form)
    for x in range(n):
        try:
            newtech.append(request.form[str(x)+"id"])
            if request.form[str(x)+"id"] in alltech:
                print(x)
                try:
                    sqlq = "UPDATE Technicians SET Tech_Firstname = '"+request.form[str(x)+"firstname"]+"', Tech_Lastname = '"+request.form[str(x)+"lastname"]+"', Tech_Office = '"+request.form[str(x)+"office"]+"', Tech_Tech = '"+request.form[str(x)+"tech"]+"' WHERE Tech_nID = '"+request.form[str(x)+"tid"]+"'"
                    sql("INSERT", sqlq)
                except:
                    sqlq = "UPDATE Technicians SET Tech_Firstname = '"+request.form[str(x)+"firstname"]+"', Tech_Lastname = '"+request.form[str(x)+"lastname"]+"', Tech_Office = '"+request.form[str(x)+"office"]+"', Tech_Tech = '"+"0"+"' WHERE Tech_nID = '"+request.form[str(x)+"tid"]+"'"
                    sql("INSERT", sqlq)
            else:
                print(x)
                sqlq = "INSERT INTO Technicians (Tech_ID, Tech_Firstname, Tech_Lastname, Tech_Office, Tech_Tech) VALUES ('"+request.form[str(x)+"id"]+"','"+request.form[str(x)+"firstname"]+"','"+request.form[str(x)+"lastname"]+"','"+request.form[str(x)+"office"]+"','"+request.form[str(x)+"tech"]+"')"
                print(sqlq)
                sql("INSERT", sqlq)
        except:
            pass

    print(alltech)
    print(newtech)

    for x in alltech:
        if x not in newtech:
            sqlq = "DELETE FROM Technicians WHERE Tech_ID = '"+x+"'"
            print(sqlq)
            sql("INSERT",sqlq)


    return ('', 204)


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


@app.route("/savevariable",methods=["GET","POST"])
def savevariable():

    print(request.form)

    for x in request.form:
        #print(x.strip(),":", request.form[x].strip())
        sqlq = "UPDATE Parameters SET PM_Value = '" + request.form[x].strip() + "' WHERE PM_Name = '"+x.strip()+"'"
        print(sqlq)
        sql("INSERT",sqlq)

    return ('', 204)


@app.route("/savemodels",methods=["GET","POST"])
def savemodels():

    print(len(request.form)//6)

    for x in range(len(request.form)//6):
        print(request.form[str(x)+"model"])

    return ('', 204)
