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

    cust = request.args.get("customer")

    units = []
    customers = []
    customer = ["","","","","","","","","","","","","","","","","","","","","",""]
    pricegroups = sql("SELECT","SELECT * FROM Pricegroups")

    pricegroups.sort(key = lambda x:x[0])

    if cust != None:
        allcustomers = sql("SELECT","SELECT * FROM Customers")

        for x in allcustomers:
            if cust.strip().lower() == x[0].strip().lower():
                customer = x
                customers = []
                customer[21] = str(customer[21])[0:10]
                customer[22] = str(customer[22])[0:10]
                customer[24] = str(customer[24])[0:10]
                if customer[24] == "1900-01-01":
                    customer[24] = ""
                table = request.cookies.get("custtable")

                if table == "irhistory":
                    pass

                else:
                    # Units #
                    units = sql("SELECT","SELECT * FROM Units WHERE LOWER(Unit_CustID) = LOWER('" + cust.strip() + "')")
                    print(units)






                break

            elif cust.strip().lower() in x[0].strip().lower() or cust.strip().lower() in x[2].strip().lower() or cust.strip().lower() in x[9].strip().lower():
                customers.append(x)





    return render_template("customers.html",theme=theme,notheme=notheme,units=units,table=table,customers=customers,customer=customer,pricegroups=pricegroups)
