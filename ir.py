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

            elif custid.lower() in x[0].lower():
                Dict = {}

                Dict["id"] = x[0]
                Dict["name"] = x[2]
                Dict["address"] = x[3]
                Dict["zip"] = x[5]
                Dict["city"] = x[6]
                Dict["owner"] = x[9]
                Dict["phone"] = x[10]

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

@app.route("/saveir",methods=["GET","POST"])
def saveir():
    print(request.form["ircustid"])
    return "save"
