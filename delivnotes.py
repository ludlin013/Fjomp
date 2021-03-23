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


@app.route("/delivnotes", methods=["GET","POST"])
def delivnotes():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    sqlq = []
    Dict = {}
    notFound = None
    delivnote = ""



    Dict["sign"] = sql("SELECT", "SELECT Tech_ID FROM Technicians")
    Dict["pricegroup"] = dict(sql("SELECT", "SELECT pg_no, pg_Descript FROM Pricegroups"))
    Dict["sentfrom"] = sql("SELECT", "SELECT * FROM Office")
    Dict["freight"] = dict(sql("SELECT", "SELECT Freight_ID, Freight_Description FROM FreightTypes"))

    Dict["DN_Sign"] = request.cookies.get("username")
    Dict["DN_Freight"] = ""
    Dict["DN_PGDescription"] = ""
    total = 0
    delivnote = request.args.get("dn")

    #if request.method == 'GET':
    if delivnote != None:

        print(delivnote)

        sqlquery = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_no ='"+delivnote+"'")
        sqlq=[]


        #print(sqlquery)
        if len(sqlquery) != 0:
            for x in sqlquery:

                total += x[12]

                sqlq.append(x)

                Dict["storenum"] = x[0].strip()
                Dict["number"] = x[1]
                Dict["storename"] = x[2].strip()
                Dict["referens"] = x[3].strip()
                Dict["date"] = x[4].strftime("%d/%m/%Y")
                Dict["DN_Sign"] = x[16]
                Dict["notes"] = x[17].strip()
                Dict["DN_Freight"] = x[15]
                Dict["DN_Pricegroup"] = x[26]
                Dict["DN_PGDescription"] = x[25]
                Dict["netvalue"] = x[11]
                Dict["DN_Closed"] = x[14]
                Dict["offer"] = x[27]
                Dict["finaloffer"] = x[28]
                #print(x)

            z = sql("SELECT", "SELECT * FROM Customers WHERE Cust_CustID = '"+Dict["storenum"]+"'")
            Dict["street"] = z[0][3].strip()
            Dict["zip"] = z[0][5].strip()
            Dict["city"] = z[0][6].strip()
        else:

            notFound = "Delivery note not found"

    return render_template("delivnotes.html",theme=theme,notheme=notheme,total=total, sqlq=sqlq, Dict=Dict, notFound=notFound, delivnote=delivnote)