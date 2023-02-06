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
    result = None

    if type == "SELECT":
        result = cursor.fetchall()
    elif type == "INSERT":
        try:
            cnxn.commit()
        except:
            result = None
            return "-1"

    return result


@app.route("/customers")
def customers():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    table = request.cookies.get('custtable')
    lastid = request.cookies.get('lastcu')
    userauth = request.cookies.get('auth')


    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]


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

                if not customer[2]:
                    customer[2] = ""
                if not customer[3]:
                    customer[3] = ""
                if not customer[6]:
                    customer[6] = ""
                if not customer[5]:
                    customer[5] = ""
                if not customer[10]:
                    customer[10] = ""

                if not customer[20]:
                    customer[20] = ""
                if not customer[19]:
                    customer[19] = ""
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
                    vend = sql("SELECT","SELECT Vend_Code, Vend_Name FROM Vendors")
                    model = sql("SELECT","SELECT * FROM Models")
                    charge = sql("SELECT","SELECT * FROM Chargemode")


                    cat.sort()
                    type.sort()
                    vend.sort()
                    model.sort(key=lambda x:x[1])
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

            elif str(cust).strip().lower() in str(x[0]).strip().lower() or str(cust).strip().lower() in str(x[2]).strip().lower() or str(cust).strip().lower() in str(x[9]).strip().lower():
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
                end = True
            if not end:
                previous = x[0]


        mincust = allcustget[0][0].strip()
        maxcust = allcustget[-1][0].strip()

    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]


    ###  Skapa från modeller  ###

    #modelcsv = sql("SELECT", "SELECT * FROM Models")
    #modelcsv.sort(key = lambda x:x[1])
    #with open("models.csv","w") as f:
    #    for x in modelcsv:
    #        for y in x:
    #            try:
    #                f.write(y.strip()+",")
    #            except:
    #                f.write(str(y)+",")
    #        f.write("\n")

    #with open("models.csv","r",encoding="latin-1") as f:
    #    for x in f.read().split("\n"):
    #        if x != "":
    #            n = x.split(";")
    #            modelname = n[1].replace("\"\"\"",'\"')
    #            if modelname.startswith("\""):
    #                modelname = modelname[1:]
    #            modelname = n[1].replace("\"\"",'\"')
    #            if modelname.startswith("\""):
    #                modelname = modelname[1:-1]
    #            #sqla = "UPDATE Units SET Unit_Chargemode = '" + n[6] + "' WHERE Unit_Model = '"+modelname+"'"
    #            sqla = "UPDATE Models SET Mod_Chargemode = '" + n[6] + "' WHERE Mod_Model = '"+modelname+"'"
    #            print(sqla)
    #            sql("INSERT",sqla)


    return render_template("customers.html",usrtech=usrtech,theme=theme,delivnote=delivnote,wo=wo,swap=swap,maxcust=maxcust,usrstatus=usrstatus,mincust=mincust,next=next,previous=previous,userauth=userauth,swapstatusdict=swapstatusdict,notheme=notheme,cat=cat,charge=charge,type=type,vend=vend,model=model,units=units,table=table,customers=customers,customer=customer,pricegroups=pricegroups)


@app.route("/custremunit", methods=["GET","POST"])
def custremunit():


    inactive = request.form["inactive"]

    if inactive == "false":
        lq = "UPDATE Units SET Unit_History = '1' WHERE Unit_ID = '"+request.form["id"]+"'"
    else:
        lq = "DELETE FROM Units WHERE Unit_ID = '"+request.form["id"]+"'"



    sql("INSERT",lq)

    return ("",204)

@app.route("/removecust", methods=["GET","POST"])
def removecust():


    sql("DELETE","DELETE FROM Customers WHERE Cust_CustID = '"+request.form["custid"]+"'")

    return ("",204)

@app.route("/newcustomer", methods=["GET","POST"])
def newcustomer():

    id = request.form["id"]

    allids = sql("SELECT","SELECT Cust_CustID FROM Customers")

    for x in allids:
        if id.lower() in x[0].lower():
            return redirect("/customers")
    if id.lower().startswith("mc"):
        sql("INSERT","INSERT INTO Customers (Cust_CustID, Cust_type) VALUES ('"+id.upper()+"','McD')")
    else:
        sql("INSERT","INSERT INTO Customers (Cust_CustID) VALUES ('"+id.upper()+"')")

    return redirect("/customers?customer="+id)


def truefalse(input):
    if input == "false":
        return "0"
    else:
        return "1"


@app.route("/customersave", methods=["GET","POST"])
def customersave():

    sqlq = "UPDATE Customers SET Cust_Name = '"+request.form["custname"]+"', Cust_OwnID = '"+request.form["custho"]+"', Cust_street1 = '"+request.form["custadress"]+"', Cust_zip = '"+request.form["custzip"]+"', Cust_city = '"+request.form["custcity"]+"', Cust_phone1 = '"+request.form["custphone"]+"', Cust_invStreet1 = '"+request.form["custname"]+"', Cust_invStreet2 = '"+request.form["custadress"]+"', Cust_invZip = '"+request.form["custzip"]+"', Cust_invCity = '"+request.form["custcity"]+"', Cust_owner = '"+request.form["custowner"]+"', Cust_Opendate = '"+request.form["custopen"]+"', Cust_Installdate ='"+request.form["custinst"]+"', Cust_Closed = '"+request.form["custclose"]+"', Cust_DT = '"+truefalse(request.form["custdt"])+"', Cust_WT = '"+truefalse(request.form["custwt"])+"', Cust_Pricegroup = '"+request.form["custgroup"]+"' WHERE Cust_CustID = '"+request.form["custnr"]+"'"

    sql("INSERT",sqlq)

    return ("",204)


@app.route("/customernewunit", methods=["GET","POST"])
def customernewunit():


    sqlq = "INSERT INTO Units (Unit_CustID, Unit_Vendor, Unit_Model, Unit_Serial, Unit_installdate, Unit_Warend, Unit_Chargemode, Unit_History) VALUES ('"+request.form["customer"]+"','"+request.form["vendor"]+"','"+request.form["model"].split("%")[0]+"','"+request.form["serial"].upper()+"','"+request.form["date"]+"','"+request.form["warranty"]+"', '"+request.form["charge"]+"', '0')"
    
    if (sqlq == "-1"):
        return ("Error adding unit, try again!",200)
    sql("INSERT",sqlq)

    return ("Unit added!",200)
    #return redirect("/customers?customer="+request.form["customer"])


@app.route("/unitedit", methods=["GET","POST"])
def unitedit():


    sqlq = "UPDATE Units SET Unit_Vendor = '"+request.form["vendor"]+"', Unit_Model = '"+request.form["model"]+"', Unit_serial = '"+request.form["serial"]+"', Unit_installdate = '"+request.form["install"]+"', Unit_Warend = '"+request.form["warend"]+"', Unit_Chargemode = '"+request.form["charge"]+"', Unit_Repldate = '"+request.form["replace"]+"' WHERE Unit_ID = '"+request.form["id"]+"'"
    sql("INSERT",sqlq)

    return ("",204)


@app.route("/custstoreselect", methods=["GET","POST"])
def custstoreselect():

    s = request.form["search"].lower()

    custs = sql("SELECT","SELECT Cust_CustID, Cust_Name, Cust_street1, Cust_zip, Cust_city, Cust_Contact, Cust_Pricegroup FROM Customers")
    result = ""
    custs.sort(key=lambda x:x[0])

    for x in custs:
        try:
            if s in x[0].lower() or s in x[1].lower() or s in x[2].lower() or s in x[3].lower() or s in x[4].lower() or s in x[5].lower():
                try:
                    result += x[0].strip() + "\t" + x[1].strip() + "\t" + x[2].strip() + "\t" + x[3].strip() + "\t" + x[4].strip() + "\t" + x[5].strip() + "\t" + str(x[6]) + "\n"
                except:
                    result += x[0].strip() + "\t"
                    try:
                        result +=   x[1].strip() + "\t"
                    except:
                        result +=  "\t"
                    try:
                        result +=   x[2].strip() + "\t"
                    except:
                        result +=  "\t"
                    try:
                        result +=   x[3].strip() + "\t"
                    except:
                        result +=  "\t"
                    try:
                        result +=   x[4].strip() + "\t"
                    except:
                        result +=  "\t"
                    try:
                        result +=   x[5].strip() + "\t"
                    except:
                        result +=  "\t"
                    try:
                        result +=   x[6].strip()
                    except:
                        pass

                    result +=  "\n"


        except: pass
    return result
