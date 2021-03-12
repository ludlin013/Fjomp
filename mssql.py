import pyodbc

server = "localhost,50404"
database = "Winstat"
username = "admin"
password = "admin"

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    )

cursor = cnxn.cursor()

cursor.execute("SELECT Part_Part,Part_Latuse,Part_Latupdat  FROM Parts")

techs = cursor.fetchall()


for x in techs:
    print(x)

cursor.close()
