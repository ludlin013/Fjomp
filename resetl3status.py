import pyodbc

server = "P2019\\WSData"
database = "winstat"
username = "sa"
password = "kamikaze"

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()

cursor.execute("UPDATE Technicians SET Tech_Office = '0'")

techs = cursor.commit()

cursor.close()
