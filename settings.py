from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc

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
