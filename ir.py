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

@app.route("/ir")
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
    #charge.append((0,""))
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
    numbers = sql("SELECT","SELECT IR_Irno FROM IR")
    max = numbers[len(numbers)-1][0]
    min = numbers[0][0]

    allir = sql("SELECT","SELECT * FROM IR")
    allir.sort(key = lambda x:x[3])

    next = max
    previous = min


    if irnumber == None:
        irnumber = str(max)

    next = int(irnumber) + 1
    previous = int(irnumber) - 1
    for x in numbers:
        if irnumber == str(x[0]):
            found = True
            irinfo = sql("SELECT","SELECT * FROM IR WHERE IR_Irno = '" + irnumber + "'")
            customer = sql("SELECT","SELECT * FROM Customers WHERE Cust_CustID = '" + irinfo[0][0] + "'")[0]
            parts = sql("SELECT","SELECT * FROM IRParts WHERE IRP_IRno = '" + irnumber + "'")
            wo = sql("SELECT","SELECT * FROM WO WHERE WO_Irno = '" + irnumber + "'")
    if not found:
        error = "No"
    if len(irinfo) > 0:
        irinfo = irinfo[0]

    while next in allir and next <= max:
        next += 1


    while previous in allir and previous > min:
        previous -= 1
    if next > max: next = max
    if previous < min: previous = min
    print(next,previous)




    types.sort(key= lambda type:type[0])
    manufact.sort(key= lambda vend:vend[0])
    models.sort(key= lambda model:model[1])
    techs.sort(key= lambda tech:tech[0])


    return render_template("ir.html",theme=theme,notheme=notheme,error=error,next=next,previous=previous,max=max,min=min,freight=freight,office=office,types=types,manufact=manufact,models=models,found=found,charge=charge,irnumber=irnumber,customer=customer,irinfo=irinfo,techs=techs,parts=parts,wo=wo)
