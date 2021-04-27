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

    cat = []
    type = []
    vend = []
    model = []
    charge = []

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
                sort = request.cookies.get("custsort")

                if table == "irhistory":
                    pass

                else:
                    # Units #
                    units = sql("SELECT","SELECT * FROM Units WHERE LOWER(Unit_CustID) = LOWER('" + cust.strip() + "')")
                    cat = sql("SELECT","SELECT * FROM SystemCat")
                    type = sql("SELECT","SELECT * FROM Modeltype")
                    vend = sql("SELECT","SELECT Vend_Code FROM Vendors")
                    model = sql("SELECT","SELECT * FROM Models")
                    charge = sql("SELECT","SELECT * FROM Chargemode")

                    cat.sort()
                    type.sort()
                    vend.sort()
                    model.sort()
                    charge.sort()


                    if sort == "cat":
                        units.sort(key = lambda x:x[1])
                    elif sort == "type":
                        units.sort(key = lambda x:x[5])
                    elif sort == "vend":
                        units.sort(key = lambda x:x[2])
                    elif sort == "model":
                        units.sort(key = lambda x:x[3])
                    elif sort == "serial":
                        units.sort(key = lambda x:x[4])
                    elif sort == "install":
                        units.sort(key = lambda x:x[6],reverse = True)
                    elif sort == "warranty":
                        units.sort(key = lambda x:x[7],reverse = True)
                    elif sort == "charge":
                        units.sort(key = lambda x:x[8])
                    elif sort == "replace":
                        units.sort(key = lambda x:x[9])
                    else:
                        units.sort(key = lambda x:x[1])

                    for x in units:
                        print(x[2])

                break

            elif cust.strip().lower() in x[0].strip().lower() or cust.strip().lower() in x[2].strip().lower() or cust.strip().lower() in x[9].strip().lower():
                customers.append(x)





    return render_template("customers.html",theme=theme,notheme=notheme,cat=cat,charge=charge,type=type,vend=vend,model=model,units=units,table=table,customers=customers,customer=customer,pricegroups=pricegroups)
