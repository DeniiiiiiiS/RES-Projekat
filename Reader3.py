# Reader3-server.py

import socket
import mysql.connector
import pickle
from time import sleep
import time
from mysql.connector import Error

import codovi
import CollectionDescription
import historicalCollection
import DeltaCD
import receiverProperty

HOST = "127.0.0.1"
PORT = 8007
NUMBER_OF_BYTES = 1000000
time_now = time.localtime()


def logger(message):
    try:
        with open("Reader3_Logger.txt", 'a') as file:
            file.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                       f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec} -> "
                       f"{message}\n")
    finally:
        file.close()


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
        logger("Reader3 tried to create database that already exists, attempting to connect.")
        return print("Reader3: Database database_reader already exists, attempting to connect...")
    else:
        print("Reader3: Creating database database_reader")
        logger("Reader3 successfully created database: [database_reader].")
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
        print("Reader3: Connection to MySQL Database database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# kreiranje tabele za reader3 ako ne postoji
def create_table(connection):
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata3'")
    result = mycursor.fetchall()
    if not result:
        mycursor.execute("create table tabledata3(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader3 successfully created table: [tabledata3].")
        print("Reader3: Creating tabledata3")
    else:
        print("Reader3: Table tabledata3 already exists, ready to use")


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code(connection, code_number):
    mycursor = connection.cursor()
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata3 where date = (select max(date) from tabledata3 where code = '{code}');")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader3: Given code ['{code}'] does not exist in the table")
    else:
        print(f"Reader3: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")
    logger("Reader3 successfully executed function: [get_last_value_for_code].")


# ispis vrednosti za trazeni code
def read_values_by_code(connection, code_number):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata3 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader3: Given code ['{code}'] does not exist in the table")
    else:
        print("Reader3: ID |///| DATASET |///| CODE          |///| VALUE |///| DATE")
        for x in myresult:
            print(f"Reader3: {x[0]}        {x[1]}             {x[2]}         {x[3]}           {x[4]}")
    logger("Reader3 successfully executed function: [read_values_by_code].")


# funkcija koja proverava da li je code code_digital
def insert_process(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    if code == "CODE_DIGITAL":
        print(f"Reader3: Code is '{code}', inserting data into table tabledata3")
        logger("Reader3 successfully executed function: [insert_process].")
        return insert(connection, id_data, dataset, code, value)
    else:
        print("Reader3: Code isn't CODE_DIGITAL, checking deadband...")
        logger("Reader3 successfully executed function: [insert_process].")
        return check_deadband(connection, id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata3 where code = '{code}'")
    myresult = mycursor.fetchall()
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i >= 1:
        print("Reader3: Difference between values is greater than 2%, inserting data into table tabledata3")
        logger("Reader3 successfully executed function: [check_deadband].")
        return insert(connection, id_data, dataset, f"'{code}'", value)
    else:
        logger("Reader3 successfully executed function: [check_deadband].")
        print("Reader3: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata3(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader3 successfully executed function: [insert].")
    return sleep(1)


create_database()
connect = mydb_connection("localhost", "root", "root")
logger("Reader3 successfully connected to database.")
create_table(connect)

# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Reader3: Waiting for connection...")
    logger("Reader3 waiting for connection.")
    conn, addr = s.accept()
    with conn:
        print(f"Reader3: Replicator receiver connected from {addr}")
        logger("ReplicatorReceiver successfully connected to Reader3.")
        while True:
            inc_data = conn.recv(NUMBER_OF_BYTES)
            data = pickle.loads(inc_data)
            logger("Reader3 successfully received data from replicatorReceiver.")
            add_lista = data.add_list
            update_lista = data.update_list

            # upisivanje vrednosti u tabelu iz add_list-e
            logger("Reader3 started reading data from add_list.")
            for cdx in add_lista:
                id_add = cdx.getId()
                dataset_add = cdx.getDataset()
                hc_add = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_add:
                    code_add = cdy.getCode()
                    value_add = cdy.getValue()
                    insert_process(connect, id_add, dataset_add, code_add, value_add)

            # upisivanje vrednosti u tabelu iz update_list-e
            logger("Reader3 started reading data from update_list.")
            for cdx in update_lista:
                id_update = cdx.getId()
                dataset_update = cdx.getDataset()
                hc_update = cdx.getHistoricalCollection().getNiz()
                for cdy in hc_update:
                    code_update = cdy.getCode()
                    value_update = cdy.getValue()
                    insert_process(connect, id_update, dataset_update, code_update, value_update)
