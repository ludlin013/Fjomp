import pyodbc

server = "10.3.1.193,50404\\FJOMP"
database = "Winstat"
username = "admin"
password = "admin"

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()

cursor.execute("SELECT Part_Latuse,Part_Latupdat  FROM Parts")

techs = cursor.fetchall()


for x in techs:
    print(x[0],x[1])

cursor.close()
