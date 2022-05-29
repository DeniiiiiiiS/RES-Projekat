# Reader3-server.py

import socket
import mysql.connector

HOST = "127.0.0.1"
PORT = 8003

# pravljenje DATABASE DataSet3
DataBaseSet3 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
mycursor = DataBaseSet3.cursor()
mycursor.execute("CREATE DATABASE DataSet1")

# povezivanje na DATABASE DataSet3
DataBaseSet3 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DataSet3"
)
mycursor = DataBaseSet3.cursor()
# ovde sada treba da se kreira tabela DataSet3

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
