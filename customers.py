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


@app.route("/customers")
def customers():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    table = request.cookies.get('custtable')
    if table == None:
        table = "units"

    customer = request.args.get("customer")

    customers = ["" for x in range(35)]
    pricegroups = sql("SELECT","SELECT * FROM Pricegroups")

    pricegroups.sort(key = lambda x:x[0])

    if customer != None:

        customers = sql("SELECT","SELECT * FROM Customers WHERE Cust_CustID = '" + customer + "'")[0]
        print(customers)

        customers[21] = str(customers[21])[0:10]
        customers[22] = str(customers[22])[0:10]
        customers[24] = str(customers[24])[0:10]
        if customers[24] == "1900-01-01":
            customers[24] = ""

    return render_template("customers.html",theme=theme,notheme=notheme,table=table,customers=customers,pricegroups=pricegroups)
