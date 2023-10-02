import mysql.connector
database=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Reena@345',
)

#Prepare a cursor object
cursorObject=database.cursor()

#Create a database

cursorObject.execute("CREATE DATABASE payrecord")
print("We are all Done!")