#install mysql client
#run: sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
#pip install mysqlclient
#pip install mysql
#pip install mysql-connector
#pip install mysql-connector-python


import mysql.connector

db=mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    passwd= 'Login12*'
)

#Prepare a cursor object
cursorObject = db.cursor()

#create a database
cursorObject.execute("CREATE DATABASE CRM")

print("Database Created")

""" After all installation and setup to create database run:python3 database_file_name.py """