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

@app.route("/swapouts", methods=["GET","POST"])
def swapouts():
    if "loggedin" in request.cookies:
        pass
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

    allswap = list(map(clean,allswap))
    store = list(map(clean, sql("SELECT", "SELECT * FROM Customers Where Cust_CustID = '"+ allswap[0] +"'")[0]))
    parts = list(map(clean, sql("SELECT", "SELECT Part_Part, Part_Partno FROM Parts")))
    techsql = list(map(clean, sql("SELECT", "SELECT Tech_ID FROM Technicians")))
    predef = list(map(clean, sql("SELECT", "SELECT SWT_Descript, SWT_Text FROM SwapText")))
    techs = []

    for x in techsql:
        techs.append(x[0])


    #print(techsql)
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
        print(x, y)
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





    return render_template("swapout.html",usrtech=usrtech,usrstatus=usrstatus,theme=theme,notheme=notheme,techs=techs,predef=predef,swapout=swapout,min=min,previous=previous,next=next,maxad=maxad,allswap=allswap,swstatus=swstatus, store=store,part=part)

@app.route("/swapsave", methods=["GET","POST"])
def swapsave():

    print(request.form)

    return ('', 204)

@app.route("/swapnew",methods=["GET","POST"])
def swapnew():

    allswap = sql("SELECT","SELECT SWP_CustId, SWP_No FROM Swap")

    allswapnr = list(map(getnr,allswap))
    allswapnr.sort()

    
    maxad = allswapnr[len(allswapnr) - 1]

    print(maxad+1)

    sql("INSERT","INSERT INTO Swapouts (DN_no,DN_Pricegroup,DN_Sign,DN_Date) VALUES (" + a + ", 1, '"+ request.cookies.get("username").strip() +"','1900-01-01 00:00:00.000')")

    return redirect("/delivnotes?dn="+a)
