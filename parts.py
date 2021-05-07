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
        Dict["lastusd"] = str(x[9]).strip().split(" ")[0]
        Dict["lastupd"] = str(x[17]).strip().split(" ")[0]

        allparts.append(Dict)

    allparts.sort(key = lambda x:x["artid"])

    return render_template("parts.html",theme=theme,notheme=notheme,allparts=allparts,auth=authenticated,des=partd,par=partn)
