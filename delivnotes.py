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

    technames = sql("SELECT","SELECT Tech_ID, Tech_Firstname, Tech_Lastname FROM Technicians")
    name = {}

    for x in technames:
        name[x[0].strip()] = x[1].strip() + " " + x[2].strip()

    if len(sqlquery) != 0:
        for x in sqlquery:
            total = total + x[12]
            Dict["number"] = x[1]

            try:
                Dict["storenum"] = x[0].strip()
                Dict["storename"] = x[2].strip()
                Dict["referens"] = x[3].strip()
                Dict["date"] = x[4].strftime("%Y-%m-%d")
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
            except:
                pass

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
            Dict["street"] = " "
            Dict["zip"] = " "
            Dict["city"] = " "

    for x in sqlq:
        x[9] = str(x[9]).replace(".",",")
        x[11] = str(x[11]).replace(".",",")
        x[12] = str(x[12]).replace(".",",")

    total = f"{total:,}"
    total = str(total).replace(","," ").replace(".",",")

    sqlq.sort(key = lambda x:x[24])

    return render_template("pdffile.html", sqlq=sqlq, Dict=Dict, total=total, delivnote=delivnote, forcount=forcount, contact=contact, name=name)


@app.route("/delivnotes", methods=["GET","POST"])
def delivnotes():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()
    userauth = request.cookies.get('auth')


    sd = {0: "red",1:"yellow",2:"green",3:"blue"}
    usrstatus = sd[sql("SELECT", "SELECT Tech_Office FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]]

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
    mailadr = request.cookies.get("delivmail")

    print(mailadr)

    if not mailadr or mailadr == "":
        mailadr = "nisse@ekabss.com"

    allparts = sql("SELECT","SELECT * FROM Parts")

    Dict["sign"] = sql("SELECT", "SELECT Tech_ID FROM Technicians")
    Dict["sign"].sort(key = lambda x:x[0])
    Dict["pricegroup"] = dict(sql("SELECT", "SELECT pg_no, pg_Descript FROM Pricegroups"))
    Dict["sentfrom"] = dict(sql("SELECT", "SELECT OF_No, OF_Name FROM Office"))
    Dict["freight"] = dict(sql("SELECT", "SELECT Freight_ID, Freight_Description FROM FreightTypes"))

    Dict["DN_Sign"] = request.cookies.get("username").upper()
    Dict["DN_Freight"] = ""
    Dict["DN_PGDescription"] = ""
    Dict["dateformat"] = datetime.now()
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
        pricegroups = []


        for x in sqlquery:
            if x != None:
                try:
                    pgdict = {}
                    pgs = sql("SELECT","SELECT Part_Outprice, Part_Price2, Part_Price3, Part_Price4, Part_Price5, Part_Price6, Part_Price7, Part_Price8, Part_Price9 FROM Parts WHERE Part_Partno = '" + x[5] + "'")

                    pgdict[1] = pgs[0][0]
                    pgdict[2] = pgs[0][1]
                    pgdict[3] = pgs[0][2]
                    pgdict[4] = pgs[0][3]
                    pgdict[5] = pgs[0][4]
                    pgdict[6] = pgs[0][5]
                    pgdict[7] = pgs[0][6]
                    pgdict[8] = pgs[0][7]
                    pgdict[9] = pgs[0][8]

                    pricegroups.append(pgdict)
                except:
                    pricegroups.append({x[26]:""})

        if len(sqlquery) != 0:
            for x in sqlquery:

                if x[5] == None:
                    x[5] = ""
                if x[6] == None:
                    x[6] = ""
                if x[7] == None:
                    x[7] = ""
                if x[10] == None:
                    x[10] = 0
                if x[8] == None:
                    x[8] = 0
                if x[11] == None:
                    x[11] = 0
                if x[9] == None:
                    x[9] = 0
                if x[12] == None:
                    x[12] = 0




                sqlq.append(x)

                Dict["number"] = x[1]
                Dict["DN_Pricegroup"] = x[26]
                Dict["dateformat"] = datetime.now()

                try:
                    Dict["storenum"] = x[0].strip()
                    Dict["storename"] = x[2].strip()
                    Dict["referens"] = x[3].strip()
                    Dict["date"] = x[4].strftime("%d/%m/%Y")
                    Dict["dateformat"] = x[4]
                    Dict["DN_Sign"] = x[16]
                    Dict["notes"] = x[17].strip()
                    Dict["DN_Freight"] = x[15]
                    Dict["DN_Office"] = x[23]
                    Dict["DN_PGDescription"] = x[25]
                    Dict["netvalue"] = x[11]
                    Dict["DN_Closed"] = x[14]
                    Dict["offer"] = x[27]
                    Dict["finaloffer"] = x[28]
                except:
                    pass

            try:
                z = sql("SELECT", "SELECT * FROM Customers WHERE Cust_CustID = '"+Dict["storenum"]+"'")
                if len(z)!=0:
                    Dict["street"] = z[0][3].strip()
                    Dict["zip"] = z[0][5].strip()
                    if Dict["referens"] == "":
                        Dict["referens"] = z[0][9].strip()
                    Dict["storename"] = z[0][2].strip()
                    Dict["city"] = z[0][6].strip()
                else:
                    Dict["street"] = ""
                    Dict["zip"] = ""
                    Dict["city"] = ""
            except:
                pass
        else:

            notFound = "Delivery note not found"

    mailbody = ""
    nolen = []
    namelen = []
    for x in sqlq:
        try:
            nolen.append(len(x[5].strip()))
            namelen.append(len(x[6].strip()))
        except:
            nolen.append(1)
            namelen.append(1)

    technames = sql("SELECT","SELECT Tech_ID, Tech_Firstname, Tech_Lastname FROM Technicians")
    name = {}

    for x in technames:
        name[x[0].strip()] = x[1].strip() + " " + x[2].strip()

    try:
        mailbody += "Delivery note # " + str(Dict["number"]) + " Customer: " + Dict["storenum"] + "  " + Dict["storename"] + "%0D%0D"
        mailbody += "Created by: " + name[Dict["DN_Sign"]] + ", " + Dict["dateformat"].strftime("%Y-%m-%d") +"%0D" + "Customer ref: " + Dict["referens"] + "%0D%0D"
    except:
        pass

    for x in sqlq:
        try:
            mailno = x[5].strip()
            mailname = x[6].strip()
            mailqty = str(x[8]).strip()
        except:
            mailno = ""
            mailname = ""
            mailqty = ""

        fspace = "%09"
        sspace = "%09"

        if max(nolen) >= 10 and len(mailno) <= 12:
            fspace += "%09"
        if max(namelen) >= 10 and len(mailname) <= 13:
            sspace += "%09"

        mailbody += mailno+fspace+mailname+sspace+mailqty+"%0D"

    try:
        mailbody += "%0DFrakt: " + Dict["freight"][Dict["DN_Freight"][:-2]] + "%0Dhttp://p2019/delivnotes?dn="+str(Dict["number"])
    except:
        pass

    sqlq.sort(key = lambda x:x[24])

    print(sqlq)

    for x in sqlq:
        print(x[24])

    usrtech = sql("SELECT", "SELECT Tech_Tech FROM Technicians WHERE UPPER(Tech_ID) = '"+ request.cookies.get("username").upper() +"'")[0][0]

    return render_template("delivnotes.html",userauth=userauth,usrtech=usrtech,usrstatus=usrstatus,theme=theme,notheme=notheme,min=min,next=next,previous=previous,max=maxad,pricegroups=pricegroups,mailbody=mailbody,total=total, sqlq=sqlq, Dict=Dict, notFound=notFound, delivnote=delivnote, allparts=allparts, mailadr=mailadr)


@app.route("/savedeliv", methods=["GET","POST"])
def savedeliv():
    offices = sql("SELECT","SELECT OF_No, OF_Name FROM Office")
    office = {}

    for x in offices:
        office[x[1].strip()] = x[0]


    pricegroups = sql("SELECT","SELECT pg_no, pg_Descript FROM Pricegroups")
    pricegroup = {}

    for x in pricegroups:
        pricegroup[str(x[0])] = x[1].strip()

    def setTrue(tf):
        if tf == "true":
            return "1"
        return "0"

    for x in range((len(request.form)-13)//12):

        price = str(request.form["price"+str(x)])
        if price == "":
            price = "0"

        q = "UPDATE Delivnotes SET DN_CustID = '" + request.form["storeNum"].upper() + "', DN_no = " + str(request.form["noteNum"]) + ", DN_Name = '" + request.form["storeName"] + "', DN_Contact = '" + request.form["contact"] + "', DN_Date = '" + request.form["date"] + "', DN_Partno = '" + request.form["num"+str(x)] + "', DN_Part = '" + request.form["nam"+str(x)] + "', DN_Serial = '" + request.form["ser"+str(x)] + "', DN_Qty = '" + str(request.form["qty"+str(x)]) + "', DN_Price = '" + price + "', DN_Discount = '" + request.form["dc"+str(x)] + "', DN_Net = '" + str(request.form["net"+str(x)]) + "', DN_Total = '" + str(request.form["tot"+str(x)]) + "', DN_Nocharge = '" + setTrue(request.form["noc"+str(x)]) + "', DN_Bo = '" + setTrue(request.form["bao"+str(x)]) + "', DN_Closed = '" + setTrue(request.form["close"]) + "', DN_Freight = '" +  str(request.form["freight"]) + "', DN_Sign = '" + request.form["sign"] + "', DN_Notes = '" + request.form["notes"] + "', DN_Bodate = '1900-01-01 00:00:00.000', DN_Picklist = 0, DN_Location = '', DN_Projno = 0, DN_Office = '" + str(office[request.form["office"].strip()]) + "', DN_PgDescript = '" + pricegroup[request.form["pg"+str(x)].split(": ")[0]].replace("'","") +  "', DN_Pricegroup = '" + request.form["pg"+str(x)].split(": ")[0] + "', DN_Offer = '" + setTrue(request.form["offer"]) + "', DN_FinalOffer = '" +  setTrue(request.form["final"]) + "' WHERE DN_Id = '" + request.form["id"+str(x)] +"'"
        print(q)
        sql("INSERT",q)

    return ('', 204)


@app.route("/newdelunit", methods=["GET","POST"])
def newdelunit():


    sql("INSERT","INSERT INTO DelivNotes (DN_no,DN_Pricegroup) VALUES (" + request.form["notenum"] + "," + request.form["pg"] + ")")

    return redirect("/delivnotes?dn="+request.form["notenum"])

@app.route("/remdelunit", methods=["GET","POST"])
def remdelunit():


    sql("INSERT","DELETE FROM DelivNotes WHERE DN_Id = +' " + request.form["id"] +  "'")

    #sql("INSERT","INSERT INTO DelivNotes (DN_no,DN_Pricegroup) VALUES (" + request.form["notenum"] + "," + request.form["pg"] + ")")

    return redirect("/delivnotes?dn="+request.cookies.get('lastdn'))

@app.route("/newdeliverynote", methods=["GET","POST"])
def newdeliverynote():


    all = sql("SELECT","SELECT DN_no FROM DelivNotes")
    sortedall = []
    for x in all:
        sortedall.append(x[0])

    sortedall.sort()

    a = str(sortedall[-1] + 1)

    print(request.cookies.get("username").strip())

    sql("INSERT","INSERT INTO DelivNotes (DN_no,DN_Pricegroup,DN_Sign,DN_Date) VALUES (" + a + ", 1, '"+ request.cookies.get("username").strip() +"','1900-01-01 00:00:00.000')")

    return redirect("/delivnotes?dn="+a)

@app.route("/deletedeliverynote/<a>", methods=["GET","POST"])
def deletedeliverynote(a):

    print("DELETE FROM DelivNotes WHERE DN_no = '" + a + "'")

    sql("INSERT","DELETE FROM DelivNotes WHERE DN_no = '" + a + "'")

    a = str(int(a)-1)

    return redirect("/delivnotes?dn="+a)

@app.route("/copydelivery/<a>", methods=["GET","POST"])
def copydelivery(a):

    all = sql("SELECT","SELECT DN_no FROM DelivNotes")
    print(max(all)[0]+1)

    newnum = max(all)[0]+1

    copyfrom = sql("SELECT","SELECT * FROM DelivNotes WHERE DN_no = '" + a + "'")

    date = str(datetime.now().date())

    for x in copyfrom:
        qq = "INSERT INTO DelivNotes (DN_no,DN_Date,DN_Partno,DN_Part,DN_Qty,DN_Price,DN_Discount,DN_Net,DN_Total,DN_Nocharge,DN_Freight,DN_Bo,DN_Office,DN_PgDescript,DN_Pricegroup,DN_Offer,DN_FinalOffer ) VALUES ('" + str(newnum) + "','" + date + "','" + x[5].strip() + "','" + x[6].strip() + "','" + str(x[8]) + "','" + str(x[9]) + "','" + str(x[10]) + "','" + str(x[11]) + "','" + str(x[12]) + "','" + str(x[13]) + "','" + x[15] + "','" + str(x[18]) + "','" + str(x[23]) + "','" + x[25].replace("'","") + "','" + str(x[26]) + "','" + "0" + "','" + "0" + "')"


        print(qq)
        sql("INSERT", qq)
    return redirect("/delivnotes?dn="+str(newnum))

@app.route("/delivpartselect", methods=["GET","POST"])
def delivpartselect():

    print(request.form)

    allparts = sql("SELECT","SELECT Part_Partno, Part_Part, Part_Stock, Part_Outprice, Part_Price2, Part_Price3, Part_Price4, Part_Price5, Part_Price6, Part_Price7, Part_Price8, Part_Price9 FROM Parts WHERE Part_Inactive = '0'")
    result = ""
    allparts.sort(key=lambda x:x[0])

    for x in allparts:

        if request.form["partnum"].lower() in x[0].lower() and request.form["partname"].lower() in x[1].lower() :
            price = str(x[3])
            if request.form["pg"] != "1":
                print(request.form["pg"])
                price = x[int(request.form["pg"])+2]
                print(price)
            try:
                result += x[0].strip() + "\t" + x[1].strip() + "\t" + str(x[2]) + "\t" + str(price) + "\n"
            except: pass


    return result

@app.route("/delivstoreselect", methods=["GET","POST"])
def delivstoreselect():

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
                        result +=  "-\t"
                    try:
                        result +=   x[2].strip() + "\t"
                    except:
                        result +=  "-\t"
                    try:
                        result +=   x[3].strip() + "\t"
                    except:
                        result +=  "-\t"
                    try:
                        result +=   x[4].strip() + "\t"
                    except:
                        result +=  "-\t"
                    try:
                        result +=   x[5].strip() + "\t"
                    except:
                        result +=  "-\t"
                    try:
                        result +=   x[6].strip()
                    except:
                        pass

                    result +=  "\n"
        except: pass
    return result

@app.route("/savestore", methods=["GET","POST"])
def savestore():

    num = request.form["store"].upper()
    id = request.form["noteid"]
    contact = request.form["contact"]
    name = request.form["name"]
    pg = request.form["pg"]

    sqlq = "UPDATE DelivNotes SET DN_CustID = '"+num+"', DN_Contact = '"+contact+"', DN_Name = '"+name+"', DN_Pricegroup = '"+pg+"' WHERE DN_no = '"+id+"'"
    print(sqlq)
    sql("INSERT",sqlq)

    return ('', 204)

@app.route("/setpricegroup", methods=["GET","POST"])
def setpricegroup():

    pgid = request.form["pgid"]
    part = request.form["part"]

    prices = sql("SELECT", "SELECT Part_Outprice, Part_Price2, Part_Price3, Part_Price4, Part_Price5, Part_Price6, Part_Price7, Part_Price8, Part_Price9 FROM Parts WHERE Part_Partno = '"+part+"'")

    result = str(prices[0][int(pgid) - 1])

    return result


@app.route("/deliverymail/<num>", methods=["GET","POST"])
def deliverymail(num):

    mailadr = request.cookies.get("delivmail")

    print(mailadr)

    if not mailadr or mailadr == "":
        mailadr = "nisse@ekabss.com"

    note = sql("SELECT","SELECT * FROM DelivNotes WHERE DN_no = '"+num+"'")
    store = sql("SELECT","SELECT * FROM Customers WHERE Cust_CustID = '"+note[0][0]+"'")[0]
    freight = dict(sql("SELECT","SELECT Freight_ID, Freight_Description FROM FreightTypes"))

    print(freight)

    print(note)
    print(store)

    nolen = []
    namelen = []
    mailbody = " "
    for x in note:
        try:
            nolen.append(len(x[5].strip()))
            namelen.append(len(x[6].strip()))
        except:
            nolen.append(1)
            namelen.append(1)

    try:
        mailbody += "Delivery note # " + num + " Customer: " + note[0][0].strip() + " " + store[2] + "%0D%0D"
        mailbody += "Created by: " + note[0][16] + ", " + note[0][4].strftime("%Y-%m-%d") +"%0D" + "Customer ref: " + note[0][3] + "%0D%0D"
    except:
        pass

    for x in note:
        try:
            mailno = x[5].strip()
            mailname = x[6].strip()
            mailqty = str(x[8]).strip()
        except:
            mailno = ""
            mailname = ""
            mailqty = ""

        fspace = "%09"
        sspace = "%09"

        if max(nolen) >= 10 and len(mailno) <= 12:
            fspace += "%09"
        if max(namelen) >= 10 and len(mailname) <= 13:
            sspace += "%09"

        mailbody += mailno+fspace+mailname+sspace+mailqty+"%0D"


    mailbody += "%0DFrakt: " + freight[note[0][15].strip()+"  "] + "%0Dhttp://p2019/delivnotes?dn="+num

    mailbody = mailbody.replace("\"","")

    done = False

    if mailadr == "karin@ekabss.com":
        done = True

    return render_template("deliverymail.html", mailbody=mailbody, mailadr=mailadr, delivnote=num, store=store, note=note, done=done)


@app.route("/unshippeddelivnotes", methods=["GET","POST"])
def unshippeddelivnotes():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    date = request.cookies.get("filterdate")
    datestr = request.cookies.get("filterdate")
    if not datestr:
        datestr = "2021-12-01"
    if not date:
        date = datetime(2021,12,1)
    else:
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = date.split("-")[2]
        if day.startswith("0"):
            day = day[1:]

        date = datetime(int(year), int(month), int(day))

    sqlq = sql("SELECT","SELECT * FROM DelivNotes WHERE DN_Closed = '0'")
    all = {}

    sqlq.sort(key = lambda x:x[4], reverse = True)

    bo = {}

    for x in sqlq:
        if x[18] == 1:
            if x[4] > date:
                if x[5] not in bo:
                    bo[x[5]] = [x[5].strip(),x[6].strip(),x[8],[[x[0],x[2],x[1],x[8]]]]
                else:
                    bo[x[5]][2] += x[8]
                    bo[x[5]][3].append([x[0],x[2],x[1],x[8]])


    for x in sqlq:
        if x[4] > date:
            if x[27] is not None:
                if x[1] not in all:
                    all[x[1]] = {"total" : x[12], "date" : x[4].date(), "cust" : x[0], "no" : x[1], "off" : x[27], "finoff" : x[28]}
                else:
                    all[x[1]]["total"] = all[x[1]]["total"] + x[12]


    return render_template("notshipped.html",theme=theme,notheme=notheme, all=all, bo=bo, datestr=datestr)

@app.route("/getnspart", methods=["GET","POST"])
def getnspart():

    dnnr = request.form["nr"]

    sqlq = sql("SELECT","SELECT * FROM DelivNotes WHERE DN_no = '" + dnnr + "'")

    content = {"ref" : sqlq[0][3].strip() , "notes" : sqlq[0][17].strip()}
    partid = 0
    content["parts"] = []

    for x in sqlq:
        try:
            content["parts"].append([x[5].strip(),x[6].strip(),str(x[8]).split(".")[0],str(x[18])])
        except:
            pass


    return content
