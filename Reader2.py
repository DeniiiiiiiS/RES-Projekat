# Reader2-server.py

import socket
import mysql.connector

HOST = "127.0.0.1"
PORT = 8002

# pravljenje DATABASE DataSet2
DataBaseSet2 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
mycursor = DataBaseSet2.cursor()
mycursor.execute("CREATE DATABASE DataSet2")

# povezivanje na DATABASE DataSet2
DataBaseSet2 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DataSet2"
)
mycursor = DataBaseSet2.cursor()
# ovde sada treba da se kreira tabela DataSet2

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
