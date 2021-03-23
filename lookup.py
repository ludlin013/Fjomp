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


@app.route("/lookup", methods=["GET","POST"])
def lookup():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    lookupdata = []

    if request.method == 'POST':
        looknumname = request.form["lookupnumname"]
        lookserial = request.form["lookserial"]

        print("!"+looknumname + "//"+lookserial+"!")

        allcust = sql("SELECT", "SELECT Cust_CustID,Cust_Name FROM Customers")
        cust = {}
        for x in allcust:
            cust[x[0].strip()] = x[1].strip()

        print(cust)
        if looknumname != "":
            delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_Part ='"+looknumname+"' OR DN_Partno = '"+looknumname+"'")
            irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE IRP_Part ='"+looknumname+"' OR IRP_Partno = '"+looknumname+"'")
            sentswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_NewPart ='"+looknumname+"' OR SWP_NewPartno = '"+looknumname+"'")
            returnedswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_OldPart ='"+looknumname+"' OR SWP_OldPartno = '"+looknumname+"'")

            print("-----Numname-----")

        elif lookserial != "":
            delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_Serial ='"+lookserial+"'")
            irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE IRP_Serial ='"+lookserial+"'")
            sentswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_NewSerial ='"+lookserial+"'")
            returnedswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_OldSerial ='"+lookserial+"'")
            unitsfile = sql("SELECT", "SELECT * FROM Unit WHERE Unit_History = '0' AND Unit_Serial ='"+lookserial+"'")
            unitshistory = sql("SELECT", "SELECT * FROM Unit WHERE Unit_History = '1' AND Unit_Serial ='"+lookserial+"'")

            print("-----Serial-----")

        for x in delivnote_result:
            Dict = {}

            Dict["type"] = "Deliverynote"
            Dict["ref"] = x[1]
            Dict["customerID"] = x[0]
            try:
                Dict["customerName"] = cust[x[0].strip()]
            except Exception:
                Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")
            Dict["date"] = x[4]
            Dict["serial"] = x[7]

            lookupdata.append(Dict)
        print("-----Delivnote-----")
        print(len(delivnote_result))
        for x in irparts_result:
            Dict = {}

            Dict["type"] = "IR Parts Used"
            Dict["ref"] = x[1]
            Dict["customerID"] = x[0]
            try:
                Dict["customerName"] = cust[x[0].strip()]
            except Exception:
                Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")
            Dict["date"] = x[10]
            Dict["serial"] = x[3]

            lookupdata.append(Dict)
        print(len(irparts_result))
        print("-----irparts-----")
        for x in sentswap:
            Dict = {}

            Dict["type"] = "Sent-Swapouts"
            Dict["ref"] = x[1]
            Dict["customerID"] = x[0]
            try:
                Dict["customerName"] = cust[x[0].strip()]
            except Exception:
                Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")
            Dict["date"] = x[3]
            Dict["serial"] = x[9]

            lookupdata.append(Dict)


        print(lookupdata)

    return render_template("lookup.html",theme=theme,notheme=notheme)
