from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc

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


@app.route("/parts",methods=["GET","POST"])
def parts():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    authenticated = False
    if request.cookies["auth"] == "true":
        authenticated = True


    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]

    theme,notheme = setTheme()

    allparts = []
    pricegroups = dict(sql("SELECT", "SELECT pg_no, pg_Descript FROM Pricegroups"))
    pricegroupnum = []
    sqlq = []
    partn = ""
    partd = ""
    parta = None
    controll_variable = 0
    cookiepartn = request.cookies.get("lastpar")
    cookiepartd = request.cookies.get("lastdes")

    if request.method == 'POST':
        controll_variable = 1
        partn = request.form["part-parts"]
        partd = request.form["description-parts"]

        for x in pricegroups:
            pricegroupnum.append(str(x))

        try:
            parta = request.form.getlist("active-parts")[0]
        except:
            parta = ""

        if cookiepartn != None:
            partn = cookiepartn

        if cookiepartd != None:
            partd = cookiepartd


        sqlquery = "SELECT * FROM Parts"
        sqlq=[]

        if partn != "" or partd != "":
            for x in sql("SELECT", sqlquery):
                if partn.lower() in x[0].lower() and partd.lower() in x[1].lower():
                    sqlq.append(x)


    for x in sqlq:

        Dict = {}

        Dict["artid"] = x[0].strip()
        Dict["name"] = x[1].strip()
        Dict["lp"] = str(x[12]).strip()
        Dict["qty"] = str(x[7]).strip()
        Dict["price1"] = str(x[6]).strip()
        Dict["price2"] = str(x[15]).strip()
        Dict["price3"] = str(x[16]).strip()
        Dict["price4"] = str(x[23]).strip()
        Dict["price5"] = str(x[24]).strip()
        Dict["price6"] = str(x[25]).strip()
        Dict["price7"] = str(x[26]).strip()
        Dict["price8"] = str(x[27]).strip()
        Dict["price9"] = str(x[28]).strip()
        Dict["inactive"] = str(x[14]).strip()
        Dict["lastusd"] = str(x[9]).strip().split(" ")[0]
        Dict["lastupd"] = str(x[17]).strip().split(" ")[0]

        allparts.append(Dict)

    allparts.sort(key = lambda x:x["artid"])

    return render_template("parts.html",usrstatus=usrstatus,theme=theme,notheme=notheme,allparts=allparts,auth=authenticated,des=partd,par=partn, controll_variable=controll_variable, pricegroups=pricegroups, pricegroupnum=pricegroupnum)
