from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
import datetime

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



@app.route("/pdffile2", methods=["GET", "POST"])
def pdffile2():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    lastSerial = None
    lastSerial2 = []
    numberOfItems = None

    Dict = {}
    types = sql("SELECT","SELECT * FROM Modeltype")
    manufact = sql("SELECT","SELECT Vend_Code FROM Vendors")
    models = sql("SELECT","SELECT * FROM Models")
    charge = sql("SELECT","SELECT * FROM Chargemode")
    techs = sql("SELECT","SELECT Tech_ID FROM Technicians")
    office = sql("SELECT","SELECT * FROM Office")
    freight = sql("SELECT","SELECT * FROM FreightTypes")
    contact = sql("SELECT","SELECT * FROM Parameters")
    irnumber = request.args.get("ir")


    customer = ["","","","","","","","","","","","",""]
    irinfo = ["","","","","","","","","","","","",""]
    parts = []
    wo = []
    error = None
    found = False
    numbers = sql("SELECT","SELECT IR_Irno,IR_Opendate FROM IR")

    for x in numbers:
        if irnumber == str(x[0]):
            found = True
            irinfo = sql("SELECT","SELECT * FROM IR WHERE IR_Irno = '" + irnumber + "'")
            if irinfo[0][0] != None:
                customer = sql("SELECT","SELECT * FROM Customers WHERE Cust_CustID = '" + irinfo[0][0] + "'")
                customer = customer[0]
            else:
                customer = ["","","","","","","","","","","","",""]

            parts = sql("SELECT","SELECT * FROM IRParts WHERE IRP_IRno = '" + irnumber + "'")
            wo = list(sql("SELECT","SELECT * FROM WO WHERE WO_Irno = '" + irnumber + "'"))

            if len(irinfo) > 0:
                irinfo = irinfo[0]


    parts.sort(key = lambda x:len(x[3]))
    duplicateFrequencies = {}
    for x in parts:
        lastSerial2.append(x[3])
    for i in lastSerial2:
        duplicateFrequencies[i.strip()] = lastSerial2.count(i)

    return render_template("pdffile2.html", Dict=Dict, irnumber=irnumber, customer=customer, irinfo=irinfo, wo=wo, parts=parts, contact=contact, lastSerial=lastSerial, duplicateFrequencies=duplicateFrequencies)


@app.route("/ir",methods=["GET","POST"])
def ir():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    types = sql("SELECT","SELECT * FROM Modeltype")
    manufact = sql("SELECT","SELECT Vend_Code FROM Vendors")
    models = sql("SELECT","SELECT * FROM Models")
    charge = sql("SELECT","SELECT * FROM Chargemode")
    techs = sql("SELECT","SELECT Tech_ID FROM Technicians")
    office = sql("SELECT","SELECT * FROM Office")
    freight = sql("SELECT","SELECT * FROM FreightTypes")
    irnumber = request.args.get("ir")

    customer = ["","","","","","","","","","","","",""]
    irinfo = ["","","","","","","","","","","","",""]
    parts = []
    wo = []
    error = None
    found = False
    numbers = sql("SELECT","SELECT IR_Irno,IR_Opendate FROM IR")

    numbers.sort(key = lambda x:x[1])

    allir = []
    for n in numbers:
        allir.append(n[0])

    lastir = request.cookies.get("lastir")
    sortmode = request.cookies.get("irsort")
    user = request.cookies.get("username")

    if irnumber == None:
        allir.sort()
        irnumber = str(allir[len(allir)-1])
        if lastir == None:
            return redirect("/ir?ir="+irnumber)
        return redirect("/ir?ir="+lastir)
    else:

        for x in numbers:
            if irnumber == str(x[0]):
                found = True
                irinfo = sql("SELECT","SELECT * FROM IR WHERE IR_Irno = '" + irnumber + "'")
                if irinfo[0][0] != None:
                    customer = sql("SELECT","SELECT * FROM Customers WHERE Cust_CustID = '" + irinfo[0][0] + "'")
                    customer = customer[0]
                else:
                    customer = ["","","","","","","","","","","","",""]

                parts = sql("SELECT","SELECT * FROM IRParts WHERE IRP_IRno = '" + irnumber + "'")
                wo = sql("SELECT","SELECT * FROM WO WHERE WO_Irno = '" + irnumber + "'")

        if not found:
            error = "No IR With that Number"
        if len(irinfo) > 0:
            irinfo = irinfo[0]


        if sortmode == "no":
            allir.sort()
            max = allir[len(allir)-1]
            min = allir[0]

            next = max
            previous = min

            numbers.sort(key = lambda x:x[0])
            ni = int(irnumber) + 1
            pi = int(irnumber) - 1

            while ni not in allir and ni < max:
                ni += 1
            while pi not in allir and pi > min:
                pi -= 1
            if next < max:
                next = ni

            previous = pi

        else:
            max = allir[len(allir)-1]
            min = allir[0]

            next = max
            previous = min

            for x in range(len(numbers)):
                if numbers[x][0] == int(irnumber):
                    ni = x + 1
                    pi = x - 1
                    if ni < len(numbers) - 1:
                        next = numbers[ni][0]
                    else:
                        next = max
                    if pi > min:
                        previous = numbers[pi][0]
                    else:
                        previous = min
                    break
            if previous < min: previous = min

        print(previous," : ",next)




    types.sort(key= lambda type:type[0])
    manufact.sort(key= lambda vend:vend[0])
    models.sort(key= lambda model:model[1])
    techs.sort(key= lambda tech:tech[0])

    customers = []

    if request.method == 'POST':
        custid = request.form["ircustid"]

        allcustomer = sql("SELECT","SELECT * FROM Customers")

        for x in allcustomer:
            if custid.lower() == x[0].lower().strip():
                customer = x
                customers = []
                break

            elif custid.lower() in x[0].lower() or custid.lower() in x[2].lower():
                Dict = {}

                Dict["id"] = x[0]
                Dict["name"] = x[2]
                Dict["address"] = x[3]
                Dict["zip"] = x[5]
                Dict["city"] = x[6]
                Dict["owner"] = x[9]
                Dict["phone"] = x[10]
                Dict["type"] = x[1]

                customers.append(Dict)
                customer[0] = custid

    return render_template("ir.html",theme=theme,notheme=notheme,customers=customers,user=user,error=error,sortmode=sortmode,next=next,previous=previous,max=max,min=min,freight=freight,office=office,types=types,manufact=manufact,models=models,found=found,charge=charge,irnumber=irnumber,customer=customer,irinfo=irinfo,techs=techs,parts=parts,wo=wo)

@app.route("/newir",methods=["GET","POST"])
def newir():
    numbers = sql("SELECT","SELECT IR_Irno FROM IR")

    allir = []
    for n in numbers:
        allir.append(n[0])

    newir = str(allir[len(allir)-1]+1)
    print(newir)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #print("INSERT INTO IR (IR_Irno,IR_Opendate) VALUES ('" + newir + "','"+ str(datetime.datetime.now()) +"')")

    sql("INSERT","INSERT INTO IR (IR_Irno,IR_Opendate) VALUES ('" + newir + "','"+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"')")

    return redirect("/ir?ir="+newir)

@app.route("/delir",methods=["GET","POST"])
def delir():
    lastir = request.cookies.get("lastir")
    sql("INSERT", "DELETE FROM IR WHERE IR_Irno = '" + lastir + "'")

    return redirect("/ir?ir="+str(int(lastir)-1))

@app.route("/newunit/<a>",methods=["GET","POST"])
def newunit(a):

    lastir = request.cookies.get("lastir")


    sqlq = "INSERT INTO WO VALUES ('" + a + "','" + str(lastir) + "','0','','','','','','',NULL,NULL,NULL,'0','','','','0','')"

    sql("INSERT",sqlq)
    print(sqlq)
    #return "newunit"
    return redirect("/ir?ir="+str(lastir))

@app.route("/saveir",methods=["GET","POST"])
def saveir():
    irnum = request.form["saveirirn"]
    ircust = request.form["saveircusn"]
    opendate = request.form["saveiropendate"]
    recvdate = request.form["saveirredate"]
    shipdate = request.form["saveirshipdate"]
    techid = request.form["saveirrepairid"]
    note = request.form["saveirnotefield"]
    ccl = request.form["saveccl"]
    onsite = request.form["saveonsite"]
    infreight = request.form["saveirinfreight"]
    outfreight = request.form["saveirrefreight"]
    closed = request.form["saveirclosed"]
    openid = request.form["savetechid"]
    office = request.form["saveirloc"]

    if opendate != "":
        opendate = str(datetime.datetime.strptime(opendate+" 00:00:00.00", '%Y-%m-%d %H:%M:%S.%f'))
    if recvdate != "":
        recvdate = str(datetime.datetime.strptime(recvdate+" 00:00:00.00", '%Y-%m-%d %H:%M:%S.%f'))
    if shipdate != "":
        shipdate = str(datetime.datetime.strptime(shipdate+" 00:00:00.00", '%Y-%m-%d %H:%M:%S.%f'))

    sqlq = "UPDATE IR SET IR_custID = '" + ircust + "',IR_Opendate = '" + opendate + "',IR_Recvdate = '" + recvdate + "',IR_Shipdate = '" + shipdate + "',IR_TechID = '" + techid + "',IR_Ccl = '" + ccl + "',IR_Onsite = '" + onsite + "',IR_Notes = '" + note + "',IR_Infreight = '" + infreight + "',IR_Outfreight = '" + outfreight + "',IR_Closed = '" + closed + "',IR_OpenID = '" + openid + "',IR_Office= '" + office + "' WHERE IR_Irno = '"+ irnum +"'"

    sql("INSERT",sqlq)

    return redirect("/ir?ir="+str(irnum))


@app.route("/remunit",methods=["GET","POST"])
def remunit():

    lastir = request.cookies.get("lastir")

    sqlq = "DELETE FROM WO WHERE WO_ID = '" + request.form["unitid"] + "'"

    sql("INSERT",sqlq)
    #print(sqlq)

    return redirect("/ir?ir="+str(lastir))



@app.route("/savespare",methods=["GET","POST"])
def savespare():

    irnumber = request.form["irnumber"]
    ircustomer = request.form["ircustomer"]
    parts = sql("SELECT","SELECT * FROM IRParts WHERE IRP_IRno = '" + irnumber + "'")
    form = request.form

    n = 0
    item = {}
    allitems = []
    for x in form:
        if x.startswith(str(n)):
            item[x] = form[x]
        elif "irnumber" in x or "ircustomer" in x:
            pass
        else:
            if len(item) != 0:
                allitems.append(item)
            item = {}
            n = n + 1
            if x.startswith(str(n)):
                item[x] = form[x]

    if len(item) != 0:
        allitems.append(item)

    date = datetime.date.today()
    print(form)
    for x in allitems:
        number = 0
        description = ""
        price = 0
        qty = 0
        charge = 2
        model = ""
        serial = ""
        id = 0

        for y in x:
            if "spareid" in y:
                id = x[y]
            if "sparenumber" in y:
                number = x[y]
            if "sparedesc" in y:
                description = x[y]
            if "spareprice" in y:
                try:
                    price = float(x[y])
                except:
                    pass
            if "spareqty" in y:
                try:
                    qty = float(x[y])
                except:
                    pass
            if "sparecharge" in y:
                charge = x[y]
            if "sparemodel" in y:
                model = x[y]
            if "spareserial" in y:
                serial = x[y]

        sqlq = "UPDATE IRParts SET IRP_CustID = '" + ircustomer + "',IRP_Model = '" + model + "',IRP_Serial = '" + serial + "', IRP_Partno = '" + number + "', IRP_Part = '" + description + "', IRP_Qty = '" + str(qty) + "', IRP_Outprice = '" + str(price) + "', IRP_Chargemode = '" + charge + "' WHERE IRP_ID = '" + id + "' AND IRP_IRno = '" + irnumber + "'"
        print(sqlq)
        sql("INSERT",sqlq)


    return ('', 204)


@app.route("/newspare",methods=["GET","POST"])
def newspare():
    model = request.form["model"]
    serial = request.form["serial"]
    irn = request.form["irn"]

    sqlq = "INSERT INTO IRParts (IRP_Model, IRP_Serial, IRP_Date, IRP_IRno) VALUES ('" + model + "','" + serial + "','" + str(datetime.date.today())  + "','" + irn + "')"
    sql("INSERT",sqlq)

    return ('', 204)

@app.route("/remspare",methods=["GET","POST"])
def remspare():

    sqlq = "DELETE FROM IRParts WHERE IRP_ID = '" + request.form["partid"] + "'"

    sql("INSERT",sqlq)

    return ('', 204)

@app.route("/irsaveall",methods=["GET","POST"])
def unitsave():

    print(request.form)

    unitsave = 0
    sparesave = 0
    for x in request.form:
        if "irwoid" in x:
            unitsave += 1
        elif "spareid" in x:
            sparesave += 1

    print(unitsave, sparesave)

    allunitsql = sql("SELECT","SELECT WO_ID FROM WO")
    allunitsss = []

    print("units")
    for x in allunitsql:
        allunitsss.append(str(x[0]).strip())

    for x in range(unitsave):
        print(request.form[str(x)+"irwoid"])
        if request.form[str(x)+"irwoid"].strip() in allunitsss:
            print(str(x) + "irwoid")
            print("finns redan")
            saveunitq = "UPDATE WO SET WO_Custid = '"+request.form["ircustid"]+"', WO_Irno = '"+request.form["ir"]+"', WO_Unitno = '"+str(x+1)+"', WO_Type = '"+request.form[str(x)+"type"]+"', WO_Vendor = '"+request.form[str(x)+"vendor"]+"', WO_Model = '"+request.form[str(x)+"model"].split("%")[3].strip()+"', WO_Serial = '"+request.form[str(x)+"serial"]+"', WO_Problem = '"+request.form[str(x)+"reported"]+"', WO_Action = '"+request.form[str(x)+"action"]+"', WO_Chargemode = '"+request.form[str(x)+"charge"]+"', WO_Recvdate = '"+request.form["saveirredate"]+"', WO_Shipdate = '"+request.form["saveirshipdate"]+"', WO_Techid = '"+request.form["savetechid"]+"' WHERE WO_ID = '"+request.form[str(x)+"irwoid"]+"'"
            print(saveunitq)
            sql("INSERT",saveunitq)


    for x in range(sparesave):
        print("spare")
        savespareq = "UPDATE IRParts SET IRP_CustID = '"+request.form["ircustid"]+"', IRP_IRno = '"+request.form["ir"] + "', IRP_Model = '" + request.form[str(x)+"sparemodel"]+"', IRP_Serial = '"+request.form[str(x)+"spareserial"]+"', IRP_Partno = '"+request.form[str(x)+"sparenumber"]+"', IRP_Part = '"+request.form[str(x)+"sparedesc"]+"', IRP_Qty = '"+request.form[str(x)+"spareqty"]+"', IRP_Inprice = '"+"0"+"', IRP_Outprice = '"+request.form[str(x)+"spareprice"]+"', IRP_Chargemode = '"+request.form[str(x)+"sparecharge"]+"', IRP_Date = '"+request.form["saveirredate"]+"', IRP_Unitno = '"+"0"+"', IRP_Office = '"+request.form["saveirloc"]+"' WHERE IRP_ID = '"+request.form[str(x)+"spareid"]+"'"
        print("sparecharge:", request.form[str(x)+"sparecharge"])
        print(sparesave)
        sql("INSERT",savespareq )

    for x in range(unitsave):
        print()

    saveirq = "UPDATE IR SET IR_custID = '" + request.form["ircustid"] + "', IR_Irno = '" + request.form["ir"] + "', IR_Opendate = '"+request.form["saveiropendate"]+"', IR_Recvdate = '"+request.form["saveirredate"]+"', IR_Shipdate = '"+request.form["saveirshipdate"]+"', IR_TechID = '"+request.form["saveirrepairid"]+"', IR_Notrecv = '"+"0"+"', IR_Ccl = '"+"0"+"', IR_Onsite = '"+"0"+"', IR_Notes = '"+request.form["saveirnotefield"]+"', IR_Infreight = '"+request.form["saveirinfreight"]+"', IR_Outfreight = '"+request.form["saveirrefreight"]+"', IR_Closed = '"+request.form["saveirclosed"]+"', IR_OpenID = '"+request.form["savetechid"]+"', IR_Office = '"+request.form["saveirloc"]+"' WHERE IR_Irno = '"+request.form["saveirirn"]+"'"


    sql("INSERT",saveirq)

    return ('', 204)
