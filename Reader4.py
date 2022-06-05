# Reader4-server.py

import socket
import mysql.connector
import datetime
from difflib import SequenceMatcher

HOST = "127.0.0.1"
PORT = 8008

# pravljenje DATABASE DataSet4
DataBaseSet4 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
mycursor = DataBaseSet4.cursor()
mycursor.execute("CREATE DATABASE DataSet4")

# povezivanje na DATABASE DataSet1
DataBaseSet4 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DataSet1"
)
mycursor = DataBaseSet4.cursor()
# kreiranje tabele DataSet4
mycursor.execute("CREATE TABLE DataSet4 (ID int PRIMARY KEY, "
                 "CODE VARCHAR(50), VALUE VARCHAR(100), DATE DATETIME)")


# funkcija koja proverava code
def insert_process(id_data, code, value):
    if code == "CODE_DIGITAL":
        print("Code is CODE_DIGITAL, inserting data into table DataSet4")
        return insert(id_data, code, value)
    else:
        return check_deadband(id_data, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, code, value):
    mycursor.execute("SELECT VALUE from DataSet4")
    myresult = mycursor.fetchall()
    for row in myresult:
        if SequenceMatcher(a=row.values(), b=value).ratio() < 0.98:
            print("Difference between values is greater than 2%, inserting data into table DataSet1")
            return insert(id_data, code, value)
        else:
            print("Difference between values is less than 2%, skipping insert")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, code, value):
    mycursor.execute("INSERT INTO DataSet4(ID, CODE, VALUE, DATE), VALUES (%s, %s, %s, %s)",
                     (id_data, code, value, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Replicator receiver connected from {addr}")
        while True:
            data = conn.recv(1024).decode()
            # ovde treba da se izvuku code i value iz lista vrednosti
            # i ubace u funkciju insert_process(id_data, code, value)
            # koja ce pokrenuti lanac funkcija za upis u tabelu
            if not data:
                break
