import mysql.connector

mydb = mysql.connector.connect(
    host="FJOMP",
    user="admin",
    password="kamikaze",
    database="FJOMP"
    )

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM Winstat.dbo.Technicians")
result = mycursor.fetchall()

print(result)
