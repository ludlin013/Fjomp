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
    lastid = request.cookies.get('custid')
    userauth = request.cookies.get('auth')


    if table == None:
        table = "units"

    cust = request.args.get("customer")

    if cust == None:
        return redirect("/customers?customer=" + str(lastid))

    units = []
    customers = []
    wo = []
    delivnote = []
    swap = []
    swapstatusdict = {0:"Ingen åtgärd",2:"Skickad till kund",3:"Returnerad",4:"RMA till leverantör",5:"Åter från RMA",6:"Väntar på låneenhet",7:"Kallager",9:"Avslutad"}

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
                    wo = sql("SELECT","SELECT * FROM WO WHERE LOWER(WO_CustID) = LOWER('" + cust.strip() + "')")
                    wo.sort(key = lambda x:x[1],reverse=True)

                elif table == "deliverynotes":
                    delivnote = sql("SELECT","SELECT * FROM DelivNotes WHERE LOWER(DN_CustID) = LOWER('" + cust.strip() + "')")
                    delivnote.sort(key = lambda x:x[1],reverse=True)

                elif table == "swapouts":

                    swap = sql("SELECT","SELECT * FROM Swap WHERE LOWER(SWP_CustID) = LOWER('" + cust.strip() + "')")
                    swap.sort(key = lambda x:x[1],reverse=True)


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
                    elif sort == "revcat":
                        units.sort(key = lambda x:x[1],reverse = True)
                    elif sort == "type":
                        units.sort(key = lambda x:x[5])
                    elif sort == "revtype":
                        units.sort(key = lambda x:x[5], reverse = True)
                    elif sort == "vend":
                        units.sort(key = lambda x:x[2])
                    elif sort == "revvend":
                        units.sort(key = lambda x:x[2], reverse = True)
                    elif sort == "model":
                        units.sort(key = lambda x:x[3])
                    elif sort == "revmodel":
                        units.sort(key = lambda x:x[3], reverse = True)
                    elif sort == "serial":
                        units.sort(key = lambda x:x[4])
                    elif sort == "revserial":
                        units.sort(key = lambda x:x[4],reverse = True)
                    elif sort == "install":
                        units.sort(key = lambda x:x[6],reverse = True)
                    elif sort == "revinstall":
                        units.sort(key = lambda x:x[6])
                    elif sort == "warranty":
                        units.sort(key = lambda x:x[7],reverse = True)
                    elif sort == "revwarranty":
                        units.sort(key = lambda x:x[7])
                    elif sort == "charge":
                        units.sort(key = lambda x:x[8])
                    elif sort == "revcharge":
                        units.sort(key = lambda x:x[8], reverse = True)
                    elif sort == "replace":
                        units.sort(key = lambda x:x[9])
                    elif sort == "revreplace":
                        units.sort(key = lambda x:x[9], reverse = True)
                    else:
                        units.sort(key = lambda x:x[6],reverse = True)
                break

            elif cust.strip().lower() in x[0].strip().lower() or cust.strip().lower() in x[2].strip().lower() or cust.strip().lower() in x[9].strip().lower():
                customers.append(x)

        allcustget = sql("SELECT","SELECT Cust_CustID FROM Customers")

        allcustget.sort(key = lambda x:x[0])

        maxcust = ""
        mincust = ""
        next = ""
        previous = ""
        end = False

        for x in allcustget:
            if end:
                next = x[0]
                break
            if cust.strip().lower() == x[0].strip().lower():
                print(x[0])
                end = True
            if not end:
                previous = x[0]


        mincust = allcustget[0][0].strip()
        maxcust = allcustget[-1][0].strip()



    return render_template("customers.html",theme=theme,delivnote=delivnote,wo=wo,swap=swap,maxcust=maxcust,mincust=mincust,next=next,previous=previous,userauth=userauth,swapstatusdict=swapstatusdict,notheme=notheme,cat=cat,charge=charge,type=type,vend=vend,model=model,units=units,table=table,customers=customers,customer=customer,pricegroups=pricegroups)
