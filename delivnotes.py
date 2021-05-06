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
@app.route("/pdffile", methods=["GET", "POST"])
def pdffile():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    delivnote = None
    delivnote = request.args.get("dn")
    forcount = 0
    Dict = {}
    total = 0

    sqlquery = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_no ='"+delivnote+"'")
    Dict["freight"] = dict(sql("SELECT", "SELECT Freight_ID, Freight_Description FROM FreightTypes"))
    Dict["sentfrom"] = dict(sql("SELECT", "SELECT OF_No, OF_Name FROM Office"))
    contact = sql("SELECT","SELECT * FROM Parameters")
    sqlq=[]

    if len(sqlquery) != 0:
        for x in sqlquery:

            total += x[12]

            Dict["storenum"] = x[0].strip()
            Dict["number"] = x[1]
            Dict["storename"] = x[2].strip()
            Dict["referens"] = x[3].strip()
            Dict["date"] = x[4].strftime("%d/%m/%Y")
            Dict["DN_Sign"] = x[16]
            Dict["notes"] = x[17].strip()
            Dict["DN_Freight"] = x[15]
            Dict["DN_Office"] = x[23]
            Dict["DN_Pricegroup"] = x[26]
            Dict["DN_PGDescription"] = x[25]
            Dict["netvalue"] = x[11]
            Dict["DN_Closed"] = x[14]
            Dict["offer"] = x[27]
            Dict["finaloffer"] = x[28]

            if x[7].strip() != "":
                forcount+=1


            sqlq.append(x)

            for x in Dict["freight"]:
                if x.strip() == Dict["DN_Freight"].strip():
                    Dict["freighttype"] = Dict["freight"][x]

            for x in Dict["sentfrom"]:
                if x == Dict["DN_Office"]:
                    Dict["office"] = Dict["sentfrom"][x]


        z = sql("SELECT", "SELECT * FROM Customers WHERE Cust_CustID = '"+Dict["storenum"]+"'")
        if len(z)!=0:
            Dict["street"] = z[0][3].strip()
            Dict["zip"] = z[0][5].strip()
            Dict["city"] = z[0][6].strip()
        else:
            Dict["street"] = ""
            Dict["zip"] = ""
            Dict["city"] = ""

    return render_template("pdffile.html", sqlq=sqlq, Dict=Dict, total=total, delivnote=delivnote, forcount=forcount, contact=contact)


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
    delivnote = None

    numbers = []
    allnumbers = sql("SELECT","SELECT DN_no FROM DelivNotes")

    for n in allnumbers:
        numbers.append(n[0])
    numbers.sort()

    min = numbers[0]
    maxad = numbers[len(numbers) - 1]
    previous = min
    next = maxad
    lastdn = request.cookies.get("lastdn")



    Dict["sign"] = sql("SELECT", "SELECT Tech_ID FROM Technicians")
    Dict["sign"].sort(key = lambda x:x[0])
    Dict["pricegroup"] = dict(sql("SELECT", "SELECT pg_no, pg_Descript FROM Pricegroups"))
    Dict["sentfrom"] = dict(sql("SELECT", "SELECT OF_No, OF_Name FROM Office"))
    Dict["freight"] = dict(sql("SELECT", "SELECT Freight_ID, Freight_Description FROM FreightTypes"))

    Dict["DN_Sign"] = request.cookies.get("username")
    Dict["DN_Freight"] = ""
    Dict["DN_PGDescription"] = ""
    total = 0
    delivnote = request.args.get("dn")
    if delivnote == None and lastdn == None:
        return redirect("/delivnotes?dn=" + str(maxad))
    elif delivnote == None:
        return redirect("/delivnotes?dn=" + str(lastdn))


    if delivnote != None:


        if int(delivnote) < maxad:
            next = int(delivnote) + 1
            while next not in numbers and next < maxad:
                next += 1

        if int(delivnote) > min:
            previous = int(delivnote) - 1
            while previous not in numbers and previous > min:
                previous -= 1


        sqlquery = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_no ='"+delivnote+"'")
        sqlq=[]


        if len(sqlquery) != 0:
            for x in sqlquery:

                total += x[12]

                sqlq.append(x)

                Dict["storenum"] = x[0].strip()
                Dict["number"] = x[1]
                Dict["storename"] = x[2].strip()
                Dict["referens"] = x[3].strip()
                Dict["date"] = x[4].strftime("%d/%m/%Y")
                Dict["dateformat"] = x[4]
                Dict["DN_Sign"] = x[16]
                Dict["notes"] = x[17].strip()
                Dict["DN_Freight"] = x[15]
                Dict["DN_Office"] = x[23]
                Dict["DN_Pricegroup"] = x[26]
                Dict["DN_PGDescription"] = x[25]
                Dict["netvalue"] = x[11]
                Dict["DN_Closed"] = x[14]
                Dict["offer"] = x[27]
                Dict["finaloffer"] = x[28]

            z = sql("SELECT", "SELECT * FROM Customers WHERE Cust_CustID = '"+Dict["storenum"]+"'")
            if len(z)!=0:
                Dict["street"] = z[0][3].strip()
                Dict["zip"] = z[0][5].strip()
                Dict["city"] = z[0][6].strip()
            else:
                Dict["street"] = ""
                Dict["zip"] = ""
                Dict["city"] = ""
        else:

            notFound = "Delivery note not found"

    mailbody = ""
    nolen = []
    namelen = []
    for x in sqlq:
        nolen.append(len(x[5].strip()))
        namelen.append(len(x[6].strip()))

    technames = sql("SELECT","SELECT Tech_ID, Tech_Firstname, Tech_Lastname FROM Technicians")
    name = {}

    for x in technames:
        name[x[0].strip()] = x[1].strip() + " " + x[2].strip()

    mailbody += "Delivery note # " + str(Dict["number"]) + " Customer: " + Dict["storenum"] + "  " + Dict["storename"] + "%0D%0D"
    mailbody += "Created by: " + name[Dict["DN_Sign"]] + ", " + Dict["dateformat"].strftime("%Y-%m-%d") +"%0D" + "Customer ref: " + Dict["referens"] + "%0D%0D"


    for x in sqlq:
        mailno = x[5].strip()
        mailname = x[6].strip()
        mailqty = str(x[8]).strip()

        fspace = "%09"
        sspace = "%09"


        if max(nolen) >= 10 and len(mailno) <= 12:
            fspace += "%09"
        if max(namelen) >= 10 and len(mailname) <= 13:
            sspace += "%09"

        mailbody += mailno+fspace+mailname+sspace+mailqty+"%0D"

    try:
        mailbody += "%0DFrakt: " + Dict["freight"][Dict["DN_Freight"][:-2]]
    except:
        pass

    return render_template("delivnotes.html",theme=theme,notheme=notheme,min=min,next=next,previous=previous,max=maxad,mailbody=mailbody,total=total, sqlq=sqlq, Dict=Dict, notFound=notFound, delivnote=delivnote)

@app.route("/savedeliv", methods=["GET","POST"])
def savedeliv():


    return ('', 204)
