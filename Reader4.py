# Reader4-server.py

import socket
import mysql.connector

HOST = "127.0.0.1"
PORT = 8004

# pravljenje DATABASE DataSet4
DataBaseSet4 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
mycursor = DataBaseSet4.cursor()
mycursor.execute("CREATE DATABASE DataSet1")

# povezivanje na DATABASE DataSet4
DataBaseSet4 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DataSet4"
)
mycursor = DataBaseSet4.cursor()
# ovde sada treba da se kreira tabela DataSet4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data)  # cisto radi provere sta stize na server
            if not data:
                break
