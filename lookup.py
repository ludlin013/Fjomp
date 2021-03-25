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
    lookupdata = []
    delivnote_result = []
    irparts_result = []
    unitsfile_results = None
    unitshistory_results = None
    sentswap_results = []
    returnedswap_results = []


    if request.method == 'POST':
        looknumname = request.form["lookupnumname"]
        lookserial = request.form["lookupserial"]
        rbball = request.form["radiobuttons-lookup"]


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
            delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_Part ='"+looknumname+"' OR DN_Partno = '"+looknumname+"'")
            irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE IRP_Part ='"+looknumname+"' OR IRP_Partno = '"+looknumname+"'")
            sentswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_NewPart ='"+looknumname+"' OR SWP_NewPartno = '"+looknumname+"'")
            returnedswap = sql("SELECT", "SELECT * FROM Swap WHERE SWP_OldPart ='"+looknumname+"' OR SWP_OldPartno = '"+looknumname+"'")



        elif lookserial != "":

            if rbball == "exact":

                delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_Serial = '"+lookserial+"'")
                irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE IRP_Serial = '"+lookserial+"'")
                sentswap_results = sql("SELECT", "SELECT * FROM Swap WHERE SWP_NewSerial = '"+lookserial+"'")
                returnedswap_results = sql("SELECT", "SELECT * FROM Swap WHERE SWP_OldSerial ='"+lookserial+"'")
                unitsfile_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '0' AND Unit_Serial = '"+lookserial+"'")
                unitshistory_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '1' AND Unit_Serial = '"+lookserial+"'")

                print("IF lookserial")
                print(unitsfile_results, unitshistory_results)

            elif rbball == "partoff":

                delivnote_result = sql("SELECT", "SELECT * FROM DelivNotes WHERE DN_Serial LIKE'%"+lookserial+"%'")
                irparts_result = sql("SELECT", "SELECT * FROM IRParts WHERE IRP_Serial LIKE '%"+lookserial+"%'")
                sentswap_results = sql("SELECT", "SELECT * FROM Swap WHERE SWP_NewSerial LIKE '%"+lookserial+"%'")
                returnedswap_results = sql("SELECT", "SELECT * FROM Swap WHERE SWP_OldSerial LIKE '%"+lookserial+"%'")
                unitsfile_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '0' AND Unit_Serial LIKE '%"+lookserial+"%'")
                unitshistory_results = sql("SELECT", "SELECT * FROM Units WHERE Unit_History = '1' AND Unit_Serial LIKE '%"+lookserial+"%'")



        if checked_delivnotes == "1":
            for x in delivnote_result:
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
                    Dict["date_check"] = datetime.date(1900,1,1)

                lookupdata.append(Dict)


        if checked_irparts == "1":
            for x in irparts_result:
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
                    Dict["date_check"] = datetime.date(1900,1,1)

                lookupdata.append(Dict)


        if checked_sent_swapout == "1":
            for x in sentswap_results:
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
                    Dict["date_check"] = datetime.date(1900,1,1)

                lookupdata.append(Dict)


        if checked_returned_swapout == "1":
            for x in returnedswap_results:
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
                    Dict["date_check"] = datetime.date(1900,1,1)

                lookupdata.append(Dict)


        if checked_unit_file == "1":
            if unitsfile_results != None:
                for x in unitsfile_results:
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
                        Dict["date_check"] = datetime.date(1900,1,1)

                    lookupdata.append(Dict)


        if checked_unit_history == "1":
            if unitshistory_results != None:
                for x in unitshistory_results:
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
                        Dict["date_check"] = datetime.date(1900,1,1)

                    lookupdata.append(Dict)


        lookupdata.sort(key = lambda x:x["date_check"], reverse=True)


    return render_template("lookup.html",theme=theme,notheme=notheme,lookupdata=lookupdata, looknumname=looknumname, partname=partname)
