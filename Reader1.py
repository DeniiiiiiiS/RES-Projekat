# Reader1-server.py

import socket
import mysql.connector
import pickle

import CollectionDescription
import historicalCollection
import DeltaCD
import receiverProperty

HOST = "127.0.0.1"
PORT = 8005
NUMBER_OF_BYTES = 1000000


# pravljenje DATABASE database_reader ako ne postoji
def create_database():
    sqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root")
    mycur = sqldb.cursor()
    mycur.execute("SELECT IF(EXISTS( SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                  " WHERE SCHEMA_NAME = 'database_reader'), 'Yes', 'No') as exist")
    myresult = mycur.fetchone()
    if myresult[0] == "Yes":
        print("Database already exists, connecting to database_reader")
    else:
        print("Creating database")
        mycursor.execute("create database database_reader")


# povezivanje na DATABASE database_reader
DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="database_reader"
)
mycursor = DB.cursor()
# kreiranje tabele tabledata1 ako ne postoji
mycursor.execute("create table tabledata1 (id int, dataset int, "
                 "code varchar(20), value int, date datetime PRIMARY KEY default now())")


# funkcija koja proverava code
def insert_process(id_data, dataset, code, value):
    if code == "CODE_DIGITAL":
        print("Code is CODE_DIGITAL, inserting data into table tabledata1")
        return insert(id_data, dataset, code, value)
    else:
        return check_deadband(id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, dataset, code, value):
    mycursor.execute("select value from tabledata1 where code = %s", code)
    myresult = mycursor.fetchall()
    i = 0
    j = 0
    for row in myresult:
        if (abs(row[i] - value) / ((row[i] + value) / 2)) * 100 > 2:
            j += 1
        i += 1
    if j >= 1:
        print("Difference between values is greater than 2%, inserting data into table DataSet1")
        return insert(id_data, dataset, code, value)
    else:
        print("No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, dataset, code, value):
    mycursor.execute("insert into tabledata1(id, dataset, code, value, date), VALUES (%s, %s, %s, %s, now())",
                     (id_data, dataset, code, value))


# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Replicator receiver connected from {addr}")
        while True:
            inc_data = conn.recv(NUMBER_OF_BYTES)
            data = pickle.loads(inc_data)

            add_lista = data.add_list
            update_lista = data.update_list

            for cdx in add_lista:
                id_add = cdx.getId()
                dataset_add = cdx.getDataset()
                hc_add = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_add:
                    code_add = cdy.getCode()
                    value_add = cdy.getValue()
                    insert(id_add, dataset_add, code_add, value_add)

            for cdx in update_lista:
                id_add = cdx.getId()
                dataset_add = cdx.getDataset()
                hc_add = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_add:
                    code_add = cdy.getCode()
                    value_add = cdy.getValue()
                    insert_process(id_add, dataset_add, code_add, value_add)
