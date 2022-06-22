import mysql.connector
from mysql.connector import Error
from time import localtime, sleep
import codovi

codenotint = "Code is not integer!"
message1 = f"Reader4: {codenotint}"
codenotrange = "Code is not in range 7:8!"
message2 = f"Reader4: {codenotrange}"


def logger(message):
    time_now = localtime()
    with open("Reader4_Logger.txt", 'a') as file:
        log = f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, " \
            f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}" \
            f" -> {message}\n"
        file.write(f"{log}")
        file.close()
        return log


def get_fetchall(mycursor):
    return mycursor.fetchall()


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
        logger("Reader4 tried to create database that already exists, attempting to connect.")
        return print("Reader4: Database database_reader already exists, attempting to connect...")
    else:
        mycur.execute("create database database_reader")
        logger("Reader4 successfully created database: [database_reader].")
        return print("Reader4: Creating database database_reader")


# kreiranje tabele za reader4 ako ne postoji
def create_table():
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata4'")
    myresult = mycursor.fetchall()
    if not myresult:
        mycursor.execute("create table tabledata4(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader4 successfully created table: [tabledata4].")
        print("Reader4: Creating tabledata4")
        return "Table created and ready to use!"
    else:
        print("Reader4: Table tabledata4 already exists, ready to use")
        return "Table ready to use!"


# funkcija koja proverava da li je code code_digital
def insert_process(id_data, dataset, code_number, value):
    message = "Reader4 successfully executed function: [insert_process]."
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 7 and code_number != 8:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    if not isinstance(id_data, int):
        print("Reader4: ID is not valid!")
        logger(message)
        return "ID is not valid!"
    elif value >= 2147483647 or value <= -2147483648:
        print("Reader4: Value is not valid!")
        logger(message)
        return "Value is not valid!"
    elif dataset != 4:
        print("Reader4: Dataset is not valid!")
        logger(message)
        return "Dataset is not valid!"
    else:
        print(f"Reader4: Checking deadband for code [{code}]...")
        logger(message)
        return check_deadband(id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, dataset, code, value):
    message = "Reader4 successfully executed function: [check_deadband]."
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata4 where code = '{code}'")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print("Reader4: Code does not exist in table, inserting data")
        logger(message)
        return insert(id_data, dataset, code, value)
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i == myresult.__len__():
        print(f"Reader4: Difference between {value} and values in database is "
              f"greater than 2%, inserting data into table tabledata4")
        logger(message)
        return insert(id_data, dataset, code, value)
    else:
        logger(message)
        return print("Reader4: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata4(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader4 successfully executed function: [insert].")
    sleep(1)
    return "Inserted successfully!"


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code4(code_number):
    message = "Reader4 successfully executed function: [get_last_value_for_code]."
    mycursor = connection.cursor()
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 7 and code_number != 8:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata4 where date = (select max(date) from tabledata4 where code = '{code}');")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print(f"Reader4: Given code ['{code}'] does not exist in the table")
        logger(message)
        return "Code doesnt exist"
    else:
        print(f"Reader4: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")
        logger(message)
        return "Exists, printed"


# ispis vrednosti za trazeni code
def read_values_by_code4(code_number):
    message = "Reader4 successfully executed function: [read_values_by_code]."
    if not isinstance(code_number, int):
        print(message1)
        logger(message)
        return codenotint
    elif code_number != 7 and code_number != 8:
        print(message2)
        logger(message)
        return codenotrange
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata4 where code = '{code}'")
    myresult = get_fetchall(mycursor)
    if not myresult:
        print(f"Reader4: Given code ['{code}'] does not exist in the table")
        logger(message)
        return "Code doesnt exist"
    else:
        print("Reader4: ID |///| DATASET |///| CODE              |///| VALUE |///| DATE       TIME")
        for x in myresult:
            print(f'Reader4: {f"{x[0]}":<9}{f"{x[1]}":<14}{f"{x[2]}":<24}{f"{x[3]}":<12}{f"{x[4]}":<10}')
        logger(message)
        return "Exists, printed"


# povezivanje na DATABASE database_reader
def mydb_connection(host_name, user_name, user_password):
    connect = None
    try:
        connect = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="database_reader",
            buffered=True
        )
        print("Reader4: Connection to MySQL Database database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connect


connection = mydb_connection("localhost", "root", "root")
