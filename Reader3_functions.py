import mysql.connector
from mysql.connector import Error
from time import localtime, sleep
import codovi


def logger(message):
    time_now = localtime()
    with open("Reader3_Logger.txt", 'a') as file:
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
        logger("Reader3 tried to create database that already exists, attempting to connect.")
        return print("Reader3: Database database_reader already exists, attempting to connect...")
    else:
        mycur.execute("create database database_reader")
        logger("Reader3 successfully created database: [database_reader].")
        return print("Reader3: Creating database database_reader")


# kreiranje tabele za reader3 ako ne postoji
def create_table():
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata3'")
    myresult = mycursor.fetchall()
    if not myresult:
        mycursor.execute("create table tabledata3(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader3 successfully created table: [tabledata3].")
        print("Reader3: Creating tabledata3")
        return "Table created and ready to use!"
    else:
        print("Reader3: Table tabledata3 already exists, ready to use")
        return "Table ready to use!"


# funkcija koja vrsi provere
def insert_process(id_data, dataset, code_number, value):
    if not isinstance(code_number, int):
        print("Reader3: Code is not integer!")
        return "Code is not integer!"
    elif code_number != 5 and code_number != 6:
        print("Reader3: Code is not in range 5:6!")
        return "Code is not in range 5:6"
    code = codovi.Code(code_number).name
    if not isinstance(id_data, int):
        print("Reader3: ID is not valid!")
        return "ID is not valid!"
    elif value >= 2147483647 or value <= -2147483648:
        print("Reader3: Value is not valid!")
        return "Value is not valid!"
    elif dataset != 3:
        print("Reader3: Dataset is not valid!")
        return "Dataset is not valid!"
    else:
        print(f"Reader3: Checking deadband for code[{code}]...")
        logger("Reader3 successfully executed function: [insert_process].")
        return check_deadband(id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata3 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print("Reader3: Code does not exist in table, inserting data")
        logger("Reader3 successfully executed function: [check_deadband].")
        return insert(id_data, dataset, code, value)
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i == myresult.__len__():
        print(f"Reader3: Difference between {value} and values in database is "
              f"greater than 2%, inserting data into table tabledata3")
        logger("Reader3 successfully executed function: [check_deadband].")
        return insert(id_data, dataset, code, value)
    else:
        logger("Reader3 successfully executed function: [check_deadband].")
        return print("Reader3: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata3(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader3 successfully executed function: [insert].")
    sleep(1)
    return "Inserted successfully!"


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code3(code_number):
    mycursor = connection.cursor()
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata3 where date = (select max(date) from tabledata3 where code = '{code}');")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader3: Given code ['{code}'] does not exist in the table")
    else:
        print(f"Reader3: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")
    logger("Reader1 successfully executed function: [get_last_value_for_code].")


# ispis vrednosti za trazeni code
def read_values_by_code3(code_number):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata3 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader3: Given code ['{code}'] does not exist in the table")
    else:
        print("Reader3: ID |///| DATASET |///| CODE              |///| VALUE |///| DATE       TIME")
        for x in myresult:
            print(f'Reader3: {f"{x[0]}":<9}{f"{x[1]}":<14}{f"{x[2]}":<24}{f"{x[3]}":<12}{f"{x[4]}":<10}')
    logger("Reader3 successfully executed function: [read_values_by_code].")


# povezivanje na DATABASE database_reader
def mydb_connection(host_name, user_name, user_password):
    connect = None
    try:
        connect = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="database_reader"
        )
        print("Reader3: Connection to MySQL Database database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connect


connection = mydb_connection("localhost", "root", "root")