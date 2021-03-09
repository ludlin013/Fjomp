import mysql.connector
from flask import *

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="10.3.1.193",
    user="Administrator"
    )

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM postnumber")
result = mycursor.fetchall()
