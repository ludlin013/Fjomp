import mysql.connector
from flask import *

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="10.3.1.193",
    user="sa",
    passwd="kamikaze",
    database="FJOMP"
    )

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM Winstat.dbo.Technicians")
result = mycursor.fetchall()

print(result)
