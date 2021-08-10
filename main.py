from flask import Flask,render_template,request,redirect,url_for
import pyodbc
from datetime import datetime
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/static/uploads'

import customers,parts,delivnotes,ir,swapouts,lookup,settings

server = "P2019\\WSData"
database = "winstat"
username = "sa"
password = "kamikaze"


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
            return True

        elif username.lower() == usr[0].strip().lower() and password == usr[3].strip():
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

    sqlunits = sql("SELECT","SELECT * FROM Units")
    sqlunits.sort(key = lambda x:x[0])

    with open("static/units.csv","w") as f:
        f.write("Unit_CustID;Unit_Cat;Unit_Vendor;Unit_Model;Unit_Serial;Unit_type;Unit_installdate;Unit_Warend;Unit_Chargemode;Unit_Repldate;Unit_Notes;Unit_History;Unit_ID\n")
        for n in sqlunits:
            for x in n:
                f.write(str(x).strip()+";")
            f.write("\n")

    return


@app.route("/importDo",methods=["GET","POST"])
def importdo():
    print("Importing")
    with open("static/IMPORTPATH.txt") as f:
        filepath = f.read()
        try:
            with open(filepath) as g:
                g = g.read().split("\n")
                g.pop(-1)
        except:
            print("No file")
            return("No file")


    allparts = []
    for x in g:
        dic = {}

        dic["moms"] = x[0:1].strip()
        dic["varugrupp"] = x[1:5].strip()
        dic["artid"] = x[5:22]
        dic["benamn"] = x[22:52].strip()
        dic["antal"] = x[52:55].strip()
        dic["snittpris"] = x[55:65].strip()
        dic["pris1"] = x[65:82].strip()
        dic["anm1"] = x[82:92].strip()
        dic["anm2"] = x[92:102].strip()
        dic["lagerfack"] = x[102:117].strip()
        dic["artikeltyp"] = x[117:118].strip()
        dic["lagerbest"] = x[118:122].strip()
        dic["pris2"] = x[122:139].strip()
        dic["pris3"] = x[139:156].strip()
        dic["pris4"] = x[156:173].strip()
        dic["pris5"] = x[173:190].strip()
        dic["pris6"] = x[190:207].strip()
        dic["pris7"] = x[207:224].strip()
        dic["pris8"] = x[224:241].strip()
        dic["pris9"] = x[241:258].strip()


        allparts.append(dic)

    dbparts = sql("SELECT","SELECT * FROM Parts")

    artids = []

    for x in dbparts:
        if x[0] != None:
            artids.append(x[0].strip())
        else:
            print(x)

    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    importedparts = 0

    sql("INSERT","UPDATE Parts SET Part_Inactive = '1'")

    total = len(sql("SELECT","SELECT Part_Partno FROM Parts"))
    newparts = ""

    for x in allparts:
        if x["artid"] == None:
            print(x)
            continue
        if x["artid"].strip() in artids:
            updatepartsq = "UPDATE Parts SET Part_Partno = '"+x["artid"].strip()+"', Part_Part = '"+x["benamn"]+"', Part_Vendor = '"+x["varugrupp"]+"', Part_Inprice = '"+x["snittpris"]+"', Part_Outprice = '"+x["pris1"]+"', Part_Stock = '"+x["antal"]+"', Part_Location = '"+x["lagerfack"]+"', Part_Inactive = '0', Part_Price2 = '"+x["pris2"]+"', Part_Price3 = '"+x["pris3"]+"', Part_Latupdat = '"+nowtime+"', Part_Price4 = '"+x["pris4"]+"', Part_Price5 = '"+x["pris5"]+"', Part_Price6 = '"+x["pris6"]+"', Part_Price7 = '"+x["pris7"]+"', Part_Price8 = '"+x["pris8"]+"', Part_Price9 = '"+x["pris9"]+"' WHERE Part_Partno = '"+x["artid"]+"'"
            #print(updatepartsq)
            importedparts += 1
            sql("INSERT",updatepartsq)
        else:
            print(x)
            newparts+=x['artid'].strip()+"\t"
            insertpartsq = "INSERT INTO Parts (Part_Partno, Part_Part, Part_Vendor, Part_Inprice, Part_Outprice, Part_Stock, Part_Location, Part_Price2, Part_Price3, Part_Latupdat, Part_Price4, Part_Price5, Part_Price6, Part_Price7, Part_Price8, Part_Price9, Part_Inactive) VALUES ('"+x['artid'].strip()+"','"+x['benamn']+"','"+x['varugrupp']+"','"+x['snittpris']+"','"+x['pris1']+"','"+x['antal']+"','"+x['lagerfack']+"','"+x['pris2']+"','"+x['pris3']+"','"+nowtime+"','"+x['pris4']+"','"+x['pris5']+"','"+x['pris6']+"','"+x['pris7']+"','"+x['pris8']+"','"+x['pris9']+"', '0')"
            print(insertpartsq)
            #sql("INSERT",insertpartsq)


    print(os.remove(filepath))
    print(newparts)
    print("New parts:", len(allparts) - importedparts)
    return(str(len(allparts))+"%%"+str(len(allparts)-importedparts)+"%%"+str(total-len(allparts))+"%%"+newparts)

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
            if request.form['username'].upper() in authusr:
                auth = True

                ################################
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

app.run(host="0.0.0.0",port="80")
