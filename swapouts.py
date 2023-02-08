from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
from datetime import datetime

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

    if type == "SELECT":
        result = cursor.fetchall()
    elif type == "INSERT":
        cnxn.commit()
        result = None

    return result

def getnr(x):
    return x[1];

def clean(n):
    return n.strip() if type(n) is str else n

def extract(n):
    return n[0]

@app.route("/swapouts", methods=["GET","POST"])
def swapouts():
    if "loggedin" in request.cookies:
        usr = request.cookies.get('username')
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    sd = {0: "red",1:"yellow",2:"green"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]
    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    swapout = None
    swapout = request.args.get("sw")
    lastsw = request.cookies.get("lastsw")


    allswap = sql("SELECT","SELECT * FROM Swap")

    allswapnr = list(map(getnr,allswap))
    allswapnr.sort()



    min = allswapnr[0]
    maxad = allswapnr[len(allswapnr) - 1]
    previous = min
    next = maxad

    if swapout == None and lastsw == None:
        return redirect("/swapouts?sw=" + str(maxad))
    elif swapout == None:
        return redirect("/swapouts?sw=" + str(lastsw))


    for x in allswap:
        if int(x[1]) == int(swapout):
            allswap = x

    if len(allswap)>48:
        return redirect("/swapouts?sw="+str(lastsw))

    allswap = list(map(clean,allswap))
    try:
        store = list(map(clean, sql("SELECT", "SELECT * FROM Customers Where Cust_CustID = '"+ allswap[0] +"'")[0]))
    except:
        store = ["" for x in range(10)]
    parts = list(map(clean, sql("SELECT", "SELECT Part_Part, Part_Partno FROM Parts")))
    techsql = list(map(clean, sql("SELECT", "SELECT Tech_ID FROM Technicians")))
    predef = list(map(clean, sql("SELECT", "SELECT SWT_Descript, SWT_Text FROM SwapText")))
    vendors = list(map(clean, sql("SELECT", "SELECT Vend_Code,Vend_Name FROM Vendors")))

    techs = []

    vendors.sort(key = lambda x:x[0])

    #print(vendors)
    
    for x in techsql:
        techs.append(x[0])


    recycled = len(sql("SELECT",f"SELECT * FROM Swap WHERE SWP_NewSerial = '{allswap[5].strip()}'"))

    techs.sort()

    part = []

    for x in parts:
        try:
            #print(int(x[1]))
            if int(x[1].strip()) >= 1000 and int(x[1].strip()) <= 1099:
                part.append((x[0].replace("UTBYTE ","").strip(),x[1].strip()))
        except:
            pass

    part.sort()

    for x,y in enumerate(allswap):
        #print(x, y)
        pass

    for x,y in enumerate(store):
        #print(x, y)
        pass

    swstatus = {0:"Ingen åtgärd",
    2:"Skickad till kund",
    3:"Returnerad",
    4:"RMA till leverantör",
    5:"Åter från RMA",
    6:"Väntar på låneenhet",
    7:"Kallager",
    9:"Avslutad"}


    if swapout != None:

        if int(swapout) < maxad:
            next = int(swapout) + 1
            while next not in allswapnr and next < maxad:
                next += 1

        if int(swapout) > min:
            previous = int(swapout) - 1
            while previous not in allswapnr and previous > min:
                previous -= 1
        if maxad == '':
            maxad=next
    print(min,previous,next,maxad)

    columns = list(map(extract,sql("SELECT","select Column_name from Information_schema.columns where Table_name like 'Swap'")))


    chargemode = ["Garanti", "Debiteras", "Kontrakt", "Rep.garant", "Skrotad"]




    return render_template("swapout.html",chargemode=chargemode,vendors=vendors,recycled=recycled,usrtech=usrtech,usr=usr,usrstatus=usrstatus,theme=theme,notheme=notheme,columns=columns,techs=techs,predef=predef,swapout=swapout,min=min,previous=previous,next=next,maxad=maxad,allswap=allswap,swstatus=swstatus, store=store,part=part)

@app.route("/swapsave", methods=["GET","POST"])
def swapsave():

    print(request.form)

    return ('', 204)

@app.route("/swapnew",methods=["GET","POST"])
def swapnew():

    allswap = sql("SELECT","SELECT SWP_CustId, SWP_No FROM Swap")

    allswapnr = list(map(getnr,allswap))
    allswapnr.sort()

    
    newnr = allswapnr[len(allswapnr) - 1] + 1

    print(f"INSERT INTO Swapouts (SWP_No,SWP_Date) VALUES ('{newnr}','{datetime.now().strftime('%Y-%m-%d')}')")

    sql("INSERT",f"INSERT INTO Swap (SWP_No,SWP_Date,SWP_CustId,SWP_Contact,SWP_Notes,SWP_Problem,SWP_OldPart,SWP_OldSerial,SWP_NewPart,SWP_NewSerial,SWP_RmaNo,SWP_RmaVendor,SWP_RmaCharge) VALUES ('{newnr}','{datetime.now().strftime('%Y-%m-%d')}','','','','','','','','','','','')")

    return redirect("/swapouts?sw="+str(newnr))


@app.route("/deleteswap/<a>", methods=["GET","POST"])
def deleteswap(a):

    print("DELETE FROM Swap WHERE SWP_No = '" + a + "'")

    sql("INSERT",f"DELETE FROM Swap WHERE SWP_No = '{a}'")

    
    high = list(map(extract,sql("SELECT","select SWP_No from Swap")))

    high.sort(reverse=True)

    swpno = int(a)

    while swpno not in high:
        swpno = swpno-1

    return redirect("/swapouts?sw="+str(swpno))



@app.route("/swapstoreselect", methods=["GET","POST"])
def swapstoreselect():

    s = request.form["search"].lower()

    custs = sql("SELECT","SELECT Cust_CustID, Cust_Name, Cust_street1, Cust_zip, Cust_city, Cust_Owner, Cust_phone1 FROM Customers")
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


@app.route("/swapsavestore", methods=["GET","POST"])
def swapsavestore():

    num = request.form["store"].upper()
    id = request.form["noteid"]
    contact = request.form["SWP_Contact"]
    #name = request.form["name"]

    sqlq = f"UPDATE Swap SET SWP_CustId = '{num}',SWP_Contact = '{contact}' where SWP_No = '{id}'"
    #print(sqlq)
    sql("INSERT",sqlq)

    return ('', 204)



@app.route("/swapsaveitem", methods=["GET","POST"])
def swapsaveitem():

    swap = request.form["swap"].upper()
    itemtype = request.form["type"]
    item = request.form["item"]

    sqlq = f"UPDATE Swap SET {itemtype} = '{item}' where SWP_No = '{swap}'"
    
    sql("INSERT",sqlq)

    return ('', 204)