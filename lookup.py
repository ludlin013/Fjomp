from flask import Flask,render_template,request,redirect,url_for
from __main__ import *
import pyodbc
import datetime
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


@app.route("/lookup", methods=["GET","POST"])
def lookup():
    if "loggedin" in request.cookies:
        pass
    else:
        return redirect(url_for("login"))
    theme,notheme = setTheme()

    partname = ""
    looknumname = ""
    lookserial = ""
    controll_variable = 0
    current_date = datetime.now().date()
    date = datetime(1900,1,1).date()
    startDate = datetime(2010, 1, 1).date()
    rbball = "exact"
    try:
        lastbtwdate1 = request.cookies.get("lastbtwdate1")
        lastbtwdate2 = request.cookies.get("lastbtwdate2")
    except:
        pass

    print(lastbtwdate1)
    if lastbtwdate1 != None:
        if len(lastbtwdate1) > 0:
            btwdate1 = lastbtwdate1
    else:
        btwdate1 = datetime(2010, 1, 1).date()

    if lastbtwdate2 != None:
        if len(lastbtwdate2) > 0:
            btwdate2 = lastbtwdate2
    else:
        btwdate2 = current_date

    try:
        numnamecookie = request.cookies.get("lastlooknumname")
        serialcookie = request.cookies.get("lastserial")
        if not serialcookie:
            serialcookie = ""
    except:
        pass

    print([btwdate1])
    print([btwdate2])
    lookupdata = []
    delivnote_result = []
    irparts_result = []
    unitsfile_results = None
    unitshistory_results = None
    sentswap_results = []
    returnedswap_results = []

    part = ["","","","","","","","","","","","",""]
    parts = []


    if request.method == 'POST':
        controll_variable = 1
        looknumname = request.form["lookupnumname"]
        lookserial = request.form["lookupserial"]
        if request.cookies.get("rbball") != "" and request.cookies.get("rbball") != None:
            try:
                rbball = request.cookies.get("rbball")
            except:
                pass
        btwdate1 = datetime.strptime(request.form["btwdate1"], '%Y-%m-%d').date()
        btwdate2 = datetime.strptime(request.form["btwdate2"], '%Y-%m-%d').date()

        if numnamecookie != None:
            if len(numnamecookie) > 0 and looknumname == "":
                try:
                    looknumname = numnamecookie
                except:
                    pass
            elif len(serialcookie) > 0 and lookserial == "":
                try:
                    lookserial = serialcookie
                except:
                    pass




        allparts = sql("SELECT", "SELECT Part_Part, Part_Partno FROM Parts")

        for x in allparts:
            if looknumname.lower() == x[0].lower().strip():
                part = x
                parts = []
                break

            elif looknumname.lower() in x[0].lower() or looknumname.lower() in x[1].lower():
                Dict = {}

                Dict["name"] = x[0]
                Dict["num"] = x[1]

                parts.append(Dict)
                part[0] = looknumname



        try:
            checked_delivnotes = request.form["delivnotes_check"]
        except:
            checked_delivnotes = "0"
        try:
            checked_ir = request.form["ir_check"]
        except:
            checked_ir = "0"
        try:
            checked_irparts = request.form["irparts_check"]
        except:
            checked_irparts = "0"
        try:
            checked_sent_swapout = request.form["sent_swapout_check"]
        except:
            checked_sent_swapout = "0"
        try:
            checked_returned_swapout = request.form["returned_swapout_check"]
        except:
            checked_returned_swapout = "0"
        try:
            checked_unit_file = request.form["unit_file_check"]
        except:
            checked_unit_file = "0"
        try:
            checked_unit_history = request.form["unit_history_check"]
        except:
            checked_unit_history = "0"


        partname = sql("SELECT", "SELECT Part_Part FROM Parts WHERE Part_Partno ='"+looknumname+"' OR Part_Part = '"+looknumname+"'")
        if partname == []:
            partname = [["Nothing found"]]

        allcust = sql("SELECT", "SELECT Cust_CustID,Cust_Name FROM Customers")
        cust = {}
        for x in allcust:
            cust[x[0].strip()] = x[1].strip()


        if looknumname != "":
            delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE UPPER(DN_Part) ='"+looknumname.upper()+"' OR UPPER(DN_Partno) = '"+looknumname.upper()+"'")
            irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE UPPER(IRP_Part) ='"+looknumname.upper()+"' OR UPPER(IRP_Partno) = '"+looknumname.upper()+"'")
            sentswap = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_NewPart) ='"+looknumname.upper()+"' OR UPPER(SWP_NewPartno) = '"+looknumname.upper()+"'")
            returnedswap = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_OldPart) ='"+looknumname.upper()+"' OR UPPER(SWP_OldPartno) = '"+looknumname.upper()+"'")



        elif lookserial != "":

            if rbball == "exact":

                delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE UPPER(DN_Serial) = '"+lookserial.upper()+"'")
                irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE UPPER(IRP_Serial) = '"+lookserial.upper()+"'")
                sentswap_results = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_NewSerial) = '"+lookserial.upper()+"'")
                returnedswap_results = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_OldSerial) ='"+lookserial.upper()+"'")
                unitsfile_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '0' AND UPPER(Unit_Serial) = '"+lookserial.upper()+"'")
                unitshistory_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '1' AND UPPER(Unit_Serial) = '"+lookserial.upper()+"'")


            elif rbball == "partoff":

                delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE UPPER(DN_Serial) LIKE'%"+lookserial.upper()+"%'")
                irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE UPPER(IRP_Serial) LIKE '%"+lookserial.upper()+"%'")
                sentswap_results = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_NewSerial) LIKE '%"+lookserial.upper()+"%'")
                returnedswap_results = sql("SELECT", "SELECT * FROM Swap WHERE UPPER(SWP_OldSerial) LIKE '%"+lookserial.upper()+"%'")
                unitsfile_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '0' AND UPPER(Unit_Serial) LIKE '%"+lookserial.upper()+"%'")
                unitshistory_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '1' AND UPPER(Unit_Serial) LIKE '%"+lookserial.upper()+"%'")



        if checked_delivnotes == "1":
            for x in delivnote_result:
                date = datetime(1900,1,1).date()
                if x[4].date() != None:
                    date = x[4].date()
                if btwdate1 < date < btwdate2:
                    Dict = {}
                    Dict["url"] = "/delivnotes?dn="+str(x[1])
                    Dict["type"] = "Deliverynote"
                    Dict["ref"] = x[1]
                    Dict["customerID"] = x[0]
                    Dict["serial"] = x[7]
                    Dict["date"] = x[4]

                    try:
                        Dict["customerName"] = cust[x[0].strip()]

                    except Exception:
                        Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                    if x[4] != None:
                        Dict["date_check"] = x[4].date()

                    else:
                        Dict["date_check"] = datetime(1900,1,1).date()

                    lookupdata.append(Dict)


        if checked_irparts == "1":
            for x in irparts_result:
                date = datetime(1900,1,1).date()
                if x[10].date() != None:
                    date = x[10].date()
                if btwdate1 < date < btwdate2:
                    Dict = {}
                    Dict["url"] = "/ir?ir="+str(x[1])
                    Dict["type"] = "IR Parts Used"
                    Dict["ref"] = x[1]
                    Dict["customerID"] = x[0]
                    Dict["serial"] = x[3]
                    Dict["date"] = x[10]

                    try:
                        Dict["customerName"] = cust[x[0].strip()]

                    except Exception:
                        Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                    if x[10] != None:
                        Dict["date_check"] = x[10].date()

                    else:
                        Dict["date_check"] = datetime(1900,1,1).date()

                    lookupdata.append(Dict)


        if checked_sent_swapout == "1":
            for x in sentswap_results:
                date = datetime(1900,1,1).date()
                if x[3] != None:
                    date = x[3]
                if btwdate1 < date < btwdate2:
                    Dict = {}
                    Dict["url"] = "/swapouts?so="+str(x[1])
                    Dict["type"] = "Sent-Swapouts"
                    Dict["ref"] = x[1]
                    Dict["customerID"] = x[0]
                    Dict["date"] = x[3]
                    Dict["serial"] = x[9]

                    try:
                        Dict["customerName"] = cust[x[0].strip()]

                    except Exception:
                        Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                    if x[3] != None:
                        Dict["date_check"] = x[3]

                    else:
                        Dict["date_check"] = datetime(1900,1,1).date()

                    lookupdata.append(Dict)


        if checked_returned_swapout == "1":
            for x in returnedswap_results:
                date = datetime(1900,1,1).date()
                if x[3] != None:
                    date = x[3]
                if btwdate1 < date < btwdate2:
                    Dict = {}
                    Dict["url"] = "/swapouts?so="+str(x[1])
                    Dict["type"] = "Returned-Swapouts"
                    Dict["ref"] = x[1]
                    Dict["customerID"] = x[0]
                    Dict["date"] = x[3]
                    Dict["serial"] = x[6]

                    try:
                        Dict["customerName"] = cust[x[0].strip()]

                    except Exception:
                        Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                    if x[3] != None:
                        Dict["date_check"] = x[3]

                    else:
                        Dict["date_check"] = datetime(1900,1,1).date()

                    lookupdata.append(Dict)


        if checked_unit_file == "1":
            if unitsfile_results != None:
                for x in unitsfile_results:
                    date = datetime(1900,1,1).date()
                    if x[6] != None:
                        date = x[6]
                    if btwdate1 < date < btwdate2:
                        Dict = {}
                        Dict["url"] = "/"
                        Dict["type"] = "Unit-File"
                        Dict["ref"] = ""
                        Dict["customerID"] = x[0]
                        Dict["date"] = x[6]
                        Dict["serial"] = x[4]

                        try:
                            Dict["customerName"] = cust[x[0].strip()]

                        except Exception:
                            Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                        if x[6] != None:
                            Dict["date_check"] = x[6]

                        else:
                            Dict["date_check"] = datetime(1900,1,1).date()

                        lookupdata.append(Dict)


        if checked_unit_history == "1":
            if unitshistory_results != None:
                for x in unitshistory_results:
                    date = datetime(1900,1,1).date()
                    if x[6] != None:
                        date = x[6]
                    if btwdate1 < date < btwdate2:
                        Dict = {}
                        Dict["url"] = "/"
                        Dict["type"] = "Unit-History"
                        Dict["ref"] = ""
                        Dict["customerID"] = x[0]
                        Dict["date"] = x[6]
                        Dict["serial"] = x[4]

                        try:
                            Dict["customerName"] = cust[x[0].strip()]

                        except Exception:
                            Dict["customerName"] = sql("SELECT", "SELECT Cust_Name FROM Customers WHERE Cust_CustID = '" + x[0] + "'")

                        if x[6] != None:
                            Dict["date_check"] = x[6]
                        else:
                            Dict["date_check"] = datetime(1900,1,1).date()

                        lookupdata.append(Dict)



        lookupdata.sort(key = lambda x:x["date_check"], reverse=True)


    return render_template("lookup.html",theme=theme,notheme=notheme,lookupdata=lookupdata, looknumname=looknumname, partname=partname, btwdate1=btwdate1, btwdate2=btwdate2, lookserial=lookserial, rbball=rbball, parts=parts, part=part, controll_variable=controll_variable, startDate=startDate, current_date=current_date)
