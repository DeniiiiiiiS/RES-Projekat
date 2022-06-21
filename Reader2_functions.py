import mysql.connector
from mysql.connector import Error
from time import localtime, sleep
import codovi


def logger(message):
    time_now = localtime()
    with open("Reader2_Logger.txt", 'a') as file:
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
        logger("Reader2 tried to create database that already exists, attempting to connect.")
        return print("Reader2: Database database_reader already exists, attempting to connect...")
    else:
        mycur.execute("create database database_reader")
        logger("Reader2 successfully created database: [database_reader].")
        return print("Reader2: Creating database database_reader")


# kreiranje tabele za reader2 ako ne postoji
def create_table():
    mycursor = connection.cursor()
    mycursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE table_name = 'tabledata2'")
    myresult = mycursor.fetchall()
    if not myresult:
        mycursor.execute("create table tabledata2(id int, dataset int, code varchar(20), value int, date datetime "
                         "PRIMARY KEY default now())")
        logger("Reader2 successfully created table: [tabledata2].")
        print("Reader2: Creating tabledata2")
        return "Table created and ready to use!"
    else:
        print("Reader2: Table tabledata2 already exists, ready to use")
        return "Table ready to use!"


# funkcija koja vrsi provere
def insert_process(id_data, dataset, code_number, value):
    code = codovi.Code(code_number).name
    if not isinstance(id_data, int):
        return print("Reader2: ID is not valid!")
    elif value >= 2147483647 or value <= -2147483648:
        return print("Reader2: Value is not valid!")
    elif dataset != 2:
        return print("Reader2: Dataset is not valid!")
    elif code != 'CODE_CUSTOM' and code != 'CODE_LIMITSET':
        return print("Reader2: Code is NOT valid!")
    else:
        print(f"Reader2: Checking deadband for code[{code}]...")
        logger("Reader2 successfully executed function: [insert_process].")
        return check_deadband(id_data, dataset, code, value)


# funkcija koja proverava deadband uslov
def check_deadband(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(f"select value from tabledata2 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print("Reader2: Code does not exist in table, inserting data")
        logger("Reader2 successfully executed function: [check_deadband].")
        return insert(id_data, dataset, code, value)
    i = 0
    for row in myresult:
        if (abs(row[0] - value) / ((row[0] + value) / 2)) * 100 > 2:
            i += 1
    if i == myresult.__len__():
        print(f"Reader2: Difference between {value} and values in database is "
              f"greater than 2%, inserting data into table tabledata2")
        logger("Reader2 successfully executed function: [check_deadband].")
        return insert(id_data, dataset, code, value)
    else:
        logger("Reader2 successfully executed function: [check_deadband].")
        return print("Reader2: No insertion, difference between values is less than 2%")


# funkcija koja upisuje u tabelu podatke
def insert(id_data, dataset, code, value):
    mycursor = connection.cursor()
    mycursor.execute(
        f"insert into tabledata2(id, dataset, code, value, date) "
        f"values ({id_data}, {dataset}, '{code}', {value}, now())")
    connection.commit()
    logger("Reader2 successfully executed function: [insert].")
    return sleep(1)


# funkcija za dobavljanje poslednje vrednosti za izabrani code
def get_last_value_for_code2(code_number):
    mycursor = connection.cursor()
    code = codovi.Code(code_number).name
    mycursor.execute(
        f"select * from tabledata2 where date = (select max(date) from tabledata2 where code = '{code}');")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader2: Given code ['{code}'] does not exist in the table")
    else:
        print(f"Reader2: For CODE: [{myresult[0][2]}], the latest VALUE: [{myresult[0][3]}]")
    logger("Reader2 successfully executed function: [get_last_value_for_code].")


# ispis vrednosti za trazeni code
def read_values_by_code2(code_number):
    code = codovi.Code(code_number).name
    mycursor = connection.cursor()
    mycursor.execute(f"select * from tabledata2 where code = '{code}'")
    myresult = mycursor.fetchall()
    if not myresult:
        print(f"Reader2: Given code ['{code}'] does not exist in the table")
    else:
        print("Reader2: ID |///| DATASET |///| CODE              |///| VALUE |///| DATE       TIME")
        for x in myresult:
            print(f'Reader2: {f"{x[0]}":<9}{f"{x[1]}":<14}{f"{x[2]}":<24}{f"{x[3]}":<12}{f"{x[4]}":<10}')
    logger("Reader2 successfully executed function: [read_values_by_code].")


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
        print("Reader2: Connection to MySQL Database database_reader successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connect


connection = mydb_connection("localhost", "root", "root")
