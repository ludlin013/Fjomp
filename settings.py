from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
import os
import smtplib
import time
from email.message import EmailMessage

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
    try:
        active = request.cookies["active"]
    except:
        active = ""

    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]

    techs = sql("SELECT","SELECT * FROM Technicians")
    vendors = sql("SELECT","SELECT * FROM Vendors")
    models = sql("SELECT","SELECT * FROM Models")
    parameters = sql("SELECT","SELECT * FROM Parameters")
    pgs = sql("SELECT", "SELECT * FROM Pricegroups")
    office = sql("SELECT", "SELECT * FROM Office")
    freight = sql("SELECT", "SELECT * FROM FreightTypes")
    charge = sql("SELECT", "SELECT * FROM ChargeMode")

    techs.sort(key = lambda x:x[0])
    vendors.sort(key = lambda x:x[0])
    models.sort(key = lambda x:x[1])
    charge.sort(key = lambda x:x[0])

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

    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    chargeconv = {3: "Garanti 1 år",
    2: "Debiteras",
    4: "Fri service",
    5: "Garanti 2 år",
    8: "Garanti 3 år",
    6: "Utbyte",
    10: "DieboldNixdorf",
    11: "Garanti 90 dgr",
    12: "Garanti 6 mån",
    9: "Garanti 5 år",}


    return render_template("settings.html",chargeconv=chargeconv,charge=charge,freight=freight, active = active, usrtech=usrtech,usrstatus=usrstatus,mail=mail,theme=theme,notheme=notheme,pgs=pgs,auth=authenticated,techs=techs,vendors=vendors, server=server, database=database, parameters=parameters,models=models,office=office)

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


    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]
    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    return render_template("importdata.html",usrtech=usrtech,usrstatus=usrstatus,theme=theme,notheme=notheme, currentPath=currentPath, fileexist=fileexist)

app.config['UPLOAD_FOLDER'] = "./static/bugs/"

@app.route("/bugreport",methods=["GET","POST"])
def bugreport():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    if request.method == 'POST':
        os.mkdir("./static/bugs/"+request.form["title"].replace("/","-"))
        with open("./static/bugs/"+request.form["title"].replace("/","-")+"/"+request.form["title"].replace("/","-")+".txt","w") as g:
            g.write(request.form["desc"] + "\n\nSubmitted by: " +request.cookies["username"])

        msg = EmailMessage()
        msg.set_content(request.form["desc"] + "\n\nSubmitted by: " +request.cookies["username"])
        msg['Subject'] = request.form["title"]
        msg['From'] = 'ludviglinde3@gmail.com'
        msg['To'] = 'ludviglinde3@gmail.com'

        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login('ludviglinde3@gmail.com', 'rumckokuykqmxxnm')
        s.send_message(msg)
        s.quit()

        f = request.files['sc']
        print([f.filename])
        if f.filename != "":
            if "png" in f.filename or "jpeg" in f.filename or "jpg" in f.filename or "tif" in f.filename or "gif" in f.filename or "":
                f.save("./static/bugs/"+request.form["title"]+"/"+request.form["title"]+".png")

    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]
    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    return render_template("bugreport.html",usrtech=usrtech,theme=theme,notheme=notheme,usrstatus=usrstatus)

@app.route("/viewreport",methods=["GET","POST"])
def viewreport():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    bugs = os.listdir("static/bugs")
    bugdict = {}
    bugdate = {}

    for x in bugs:
        if x == "!klara":
            bugs.remove(x)

    for x in bugs:
        with open("static/bugs/"+x+"/"+x+".txt") as f:
            bugdict[x] = f.read()

    for x in bugs:
        bugdate[x] = time.ctime(os.path.getmtime("static/bugs/"+x)).split(" ")[1:]

    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]
    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    return render_template("viewreport.html",usrtech=usrtech,theme=theme,notheme=notheme, bugs=bugs, bugdict=bugdict, bugdate=bugdate, usrstatus=usrstatus)

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
    #print(request.form)

    for x in range(len(request.form)//6):
        #print(request.form[str(x)+"mod"])
        sqlq = "UPDATE Models SET Mod_Vendor = '"+request.form[str(x)+"ven"].strip()+"', Mod_Model = '"+request.form[str(x)+"mod"].strip()+"', Mod_Unittype = '"+request.form[str(x)+"typ"].strip()+"', Mod_Cat = '"+request.form[str(x)+"cat"].strip()+"', Mod_Chargemode = '"+request.form[str(x)+"cha"].strip()+"' WHERE Mod_ID = '"+request.form[str(x)+"id"]+"'"
        #print(sqlq)
        sql("INSERT",sqlq)


    return ('', 204)

@app.route("/newmodel",methods=["GET","POST"])
def newmodel():

    #print("newmodel")

    sql("INSERT", "INSERT INTO Models (Mod_Vendor, Mod_Model, Mod_Unittype, Mod_Cat, Mod_Chargemode) VALUES ('NEWMO','','','','')")


    return ('', 204)

@app.route("/newfe",methods=["GET","POST"])
def newfe():

    #print("newmodel")

    sql("INSERT", "INSERT INTO FreightTypes (Freight_ID, Freight_Description, Freight_Std) VALUES ('111','','')")


    return ('', 204)

@app.route("/newch",methods=["GET","POST"])
def newch():

    #print("newmodel")

    sql("INSERT", "INSERT INTO ChargeMode (CM_Type, CM_Description, CM_WarMonths) VALUES ('111','','')")


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

@app.route("/savech",methods=["GET","POST"])
def savech():

    count = len(request.form)//4

    for x in range(count):
        sqlq = "UPDATE ChargeMode SET CM_Type = '"+request.form[str(x)+"type"]+"', CM_Description = '"+request.form[str(x)+"desc"]+"', CM_WarMonths = '"+request.form[str(x)+"month"]+"' WHERE CM_ID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)
        sql("INSERT", sqlq)

    return ('', 204)

@app.route("/saveve",methods=["GET","POST"])
def saveve():

    count = len(request.form)//13
    print(count)

    for x in range(count):
        sqlq = "UPDATE Vendors SET Vend_Code = '"+request.form[str(x)+"code"]+"', Vend_Name = '"+request.form[str(x)+"name"]+"',Vend_Currency = '"+request.form[str(x)+"curr"]+"',Vend_Address1 = '"+request.form[str(x)+"add1"]+"', Vend_Address2 = '"+request.form[str(x)+"add2"]+"', Vend_Address3 = '"+request.form[str(x)+"add3"]+"', Vend_Zip = '"+request.form[str(x)+"zip"]+"', Vend_Country = '"+request.form[str(x)+"country"]+"',Vend_Phone = '"+request.form[str(x)+"phone"]+"', Vend_Fax = '"+request.form[str(x)+"fax"]+"', Vend_Contact = '"+request.form[str(x)+"contact"]+"', Vend_Mail = '"+request.form[str(x)+"mail"]+"' WHERE Vend_ID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)
        sql("INSERT", sqlq)

    return ('', 204)

@app.route("/savefe",methods=["GET","POST"])
def savefe():

    count = len(request.form)//4

    for x in range(count):
        sqlq = "UPDATE FreightTypes SET Freight_ID = '"+request.form[str(x)+"rid"]+"', Freight_Description = '"+request.form[str(x)+"desc"]+"',Freight_Std = '"+request.form[str(x)+"std"]+"' WHERE Freight_RID = '"+request.form[str(x)+"id"]+"'"
        print(sqlq)
        sql("INSERT", sqlq)

    return ('', 204)

@app.route("/newve",methods=["GET","POST"])
def newve():

    sql("INSERT", "INSERT INTO Vendors (Vend_Code, Vend_Name, Vend_Currency, Vend_Address1, Vend_Address2, Vend_Address3, Vend_Zip, Vend_Country, Vend_Phone, Vend_Fax, Vend_Contact, Vend_Mail) VALUES ('NEWVE','','','','','','','','','','','')")

    newid = sql("SELECT","SELECT * FROM Vendors")

    for x in newid:
        if x[1] == "NEWPG":
            newid = str(x[12])
            break

    return ('', 204)

@app.route("/newpg",methods=["GET","POST"])
def newpg():

    sql("INSERT", "INSERT INTO Pricegroups (pg_no, pg_Descript) VALUES ('111','')")

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

@app.route("/remch",methods=["GET","POST"])
def remch():

    sql("INSERT", "DELETE FROM ChargeMode WHERE CM_ID = '"+request.form["id"]+"'")

    return ('', 204)

@app.route("/remfe",methods=["GET","POST"])
def remfe():

    sql("INSERT", "DELETE FROM FreightTypes WHERE Freight_RID = '"+request.form["id"]+"'")

    return ('', 204)


@app.route("/remve",methods=["GET","POST"])
def remve():

    sql("INSERT", "DELETE FROM Vendors WHERE Vend_ID = '"+request.form["id"]+"'")

    return ('', 204)

@app.route("/remmod",methods=["GET","POST"])
def remmod():

    sql("INSERT", "DELETE FROM Models WHERE Mod_ID = '"+request.form["id"]+"'")
    print("DELETE FROM Models WHERE Mod_ID = '"+request.form["id"]+"'")
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

    sql("INSERT", "INSERT INTO Technicians (Tech_ID, Tech_Firstname, Tech_Lastname, Tech_Office, Tech_Tech, Tech_Pwd) VALUES ('NET','','','1','1','')")

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
