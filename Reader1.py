# Reader1-server.py

import socket
import mysql.connector
import pickle
from mysql.connector import Error

import codovi
import CollectionDescription
import historicalCollection
import DeltaCD
import receiverProperty

HOST = "127.0.0.1"
PORT = 8005
NUMBER_OF_BYTES = 1000000


# kreiranje DATABASE database_reader ako ne postoji
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
        return print("Reader1: Database database_reader already exists, attempting to connect...")
    else:
        print("Reader1: Creating database database_reader")
        return mycur.execute("create database database_reader")


# povezivanje na DATABASE database_reader
def mydb_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="database_reader"
        )
        print("Reader1: Connection to MySQL database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# kreiranje tabele za reader1 ako ne postoji
def create_table(connection):
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata1'")
    result = mycursor.fetchall()
    if not result:
        mycursor.execute("create table tabledata1(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        print("Reader1: Creating tabledata1")
    else:
        print("Reader1: Table tabledata1 already exists, ready to use")


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code(connection, code_number):
    mycursor = connection.cursor()
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata1 where date = (select max(date) from tabledata1 where code = '{code}');")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader1: Given code ['{code}'] does not exist in the table")
    else:
        print(f"Reader1: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")


# ispis vrednosti za trazeni code
def read_values_by_code(connection, code_number):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata1 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader1: Given code ['{code}'] does not exist in the table")
    else:
        print("Reader1: ID |///| DATASET |///| CODE          |///| VALUE |///| DATE")
        for x in myresult:
            print(f"Reader1: {x[0]}        {x[1]}             {x[2]}         {x[3]}           {x[4]}")


# funkcija koja proverava da li je code code_digital
def insert_process(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    if code == "CODE_DIGITAL":
        print(f"Reader1: Code is '{code}', inserting data into table tabledata1")
        return insert(connection, id_data, dataset, code, value)
    else:
        print("Reader1: Code isn't CODE_DIGITAL, checking deadband...")
        return check_deadband(connection, id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata1 where code = '{code}'")
    myresult = mycursor.fetchall()
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i >= 1:
        print("Reader1: Difference between values is greater than 2%, inserting data into table tabledata1")
        return insert(connection, id_data, dataset, f"'{code}'", value)

    else:
        print("Reader1: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata1(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    return connection.commit()


create_database()
connect = mydb_connection("localhost", "root", "root")
create_table(connect)

# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Reader1: Waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print(f"Reader1: Replicator receiver connected from {addr}")
        while True:
            inc_data = conn.recv(NUMBER_OF_BYTES)
            data = pickle.loads(inc_data)

            add_lista = data.add_list
            update_lista = data.update_list

            # upisivanje vrednosti u tabelu iz add_list-e
            for cdx in add_lista:
                id_add = cdx.getId()
                dataset_add = cdx.getDataset()
                hc_add = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_add:
                    code_add = cdy.getCode()
                    value_add = cdy.getValue()
                    insert(connect, id_add, dataset_add, code_add, value_add)

            # upisivanje vrednosti u tabelu iz update_list-e
            for cdx in update_lista:
                id_update = cdx.getId()
                dataset_update = cdx.getDataset()
                hc_update = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_update:
                    code_update = cdy.getCode()
                    value_update = cdy.getValue()
                    insert_process(connect, id_update, dataset_update, code_update, value_update)
