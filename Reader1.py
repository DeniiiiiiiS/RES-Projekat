# Reader1-server.py
import pickle
import socket
import mysql.connector
from time import sleep
from time import localtime
from mysql.connector import Error

import codovi
import CollectionDescription
import historicalCollection
import DeltaCD
import receiverProperty

HOST = "127.0.0.1"
PORT = 8005
NUMBER_OF_BYTES = 1000000

counter = 0

def logger(message):
    time_now = localtime()
    with open("Reader1_Logger.txt", 'a') as file:
        log = f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, " \
            f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}" \
            f" -> {message}\n"
        file.write(f"{log}")
        file.close()
        return log


# kreiranje DATABASE database_reader ako ne postoji
def connect_to_database():
    sqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root")
    mycur = sqldb.cursor()
    mycur.execute("SELECT IF(EXISTS( SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA"
                  " WHERE SCHEMA_NAME = 'database_reader'), 'Yes', 'No') as exist")
    myresult = mycur.fetchone()
    if myresult[0] == "Yes":
        logger("Reader1 tried to create database that already exists, attempting to connect.")
        return print("Reader1: Database database_reader already exists, attempting to connect...")
    else:
        mycur.execute("create database database_reader")
        logger("Reader1 successfully created database: [database_reader].")
        return print("Reader1: Creating database database_reader")


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
        print("Reader1: Connection to MySQL Database database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


# kreiranje tabele za reader1 ako ne postoji
def create_table(connection):
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata1'")
    myresult = mycursor.fetchall()
    if not myresult:
        mycursor.execute("create table tabledata1(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader1 successfully created table: [tabledata1].")
        print("Reader1: Creating tabledata1")
        return "Table created and ready to use!"
    else:
        print("Reader1: Table tabledata1 already exists, ready to use")
        return "Table ready to use!"


# funkcija koja proverava da li je code code_digital
def insert_process(connection, id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    if code == 'CODE_DIGITAL':
        print(f"Reader1: Code is '{code}', inserting data into table tabledata1")
        logger("Reader1 successfully executed function: [insert_process].")
        return insert(connection, id_data, dataset, code, value)
    else:
        print("Reader1: Code isn't CODE_DIGITAL, checking deadband...")
        logger("Reader1 successfully executed function: [insert_process].")
        return check_deadband(connection, id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(connection, id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata1 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print("Reader1: Code does not exist in table, inserting data")
        logger("Reader1 successfully executed function: [check_deadband].")
        return insert(connection, id_data, dataset, code, value)
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i == myresult.__len__():
        print(f"Reader1: Difference between {value} and values in database is "
              f"greater than 2%, inserting data into table tabledata1")
        logger("Reader1 successfully executed function: [check_deadband].")
        return insert(connection, id_data, dataset, code, value)
    else:
        logger("Reader1 successfully executed function: [check_deadband].")
        return print("Reader1: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(connection, id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata1(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader1 successfully executed function: [insert].")
    return sleep(1)


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
    logger("Reader1 successfully executed function: [get_last_value_for_code].")


# ispis vrednosti za trazeni code
def read_values_by_code(connection, code_number):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata1 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader1: Given code ['{code}'] does not exist in the table")
    else:
        print("Reader1: ID |///| DATASET |///| CODE              |///| VALUE |///| DATE       TIME")
        for x in myresult:
            print(f'Reader1: {f"{x[0]}":<9}{f"{x[1]}":<14}{f"{x[2]}":<24}{f"{x[3]}":<12}{f"{x[4]}":<10}')
    logger("Reader1 successfully executed function: [read_values_by_code].")


#def start_reader1():
connect_to_database()
connection = mydb_connection("localhost", "root", "root")
logger("Reader1 successfully connected to database.")
create_table(connection)
# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        print("Reader1: Waiting for connection...")
        logger("Reader1 waiting for connection.")
        conn, addr = s.accept()
        print(f"Reader1: Replicator receiver connected from {addr}")
        logger("ReplicatorReceiver successfully connected to Reader1.")
        
        inc_data = conn.recv(NUMBER_OF_BYTES)
        data = pickle.loads(inc_data)
        logger("Reader1 successfully received data from replicatorReceiver.")
        add_lista = data.add_list
        update_lista = data.update_list
        # upisivanje vrednosti u tabelu iz add_list-e
        logger("Reader1 started reading data from add_list.")
        for cdx in add_lista:
            id_add = cdx.getId()
            dataset_add = cdx.getDataset()
            hc_add = cdx.getHistoricalCollection().getNiz()
            for cdy in hc_add:
                code_add = cdy.getCode()
                value_add = cdy.getValue()
                if counter != 10:
                    insert_process(connection, id_add, dataset_add, code_add, value_add)
                    counter += 1
                else:
                    counter = 0
                    break
                
        # upisivanje vrednosti u tabelu iz update_list-e
        logger("Reader1 started reading data from update_list.")
        for cdx in update_lista:
            id_update = cdx.getId()
            dataset_update = cdx.getDataset()
            hc_update = cdx.getHistoricalCollection().getNiz()
            for cdy in hc_update:
                code_update = cdy.getCode()
                value_update = cdy.getValue()
                if counter != 10:
                    insert_process(connection, id_update, dataset_update, code_update, value_update)
                    counter += 1
                else:
                    counter = 0
                    break