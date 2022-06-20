import socket
import time
from time import sleep
from writer_functions import logger

HOST = "127.0.0.1"
PORT = 8001
address = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(address)
    logger("Uspesno konektovanje na ReplicatorSender server!")

    while True:
        print("WRITER: Please input your data")
        print("To stop sending data, type -1 as Code and END as Value")

        print("Enter desired Code:")
        code = input()
        print("Enter desired Value:")
        value = input()

        if code.isdigit() == False:
            print("Code must be integer between 1 and 8")
            logger("Uneta nevalidna vrednost za kod: non-integer")
            break
        if int(code) == -1 or value == "END":
            print("Zaustavljanje writera...")
            logger("Uneta vrednost za zaustavljanje rada writera")
            break

        if int(code) >= 1 and int(code) <= 8:
            sleep(2)
            data = str(code) + ";" + str(value)
            s.sendall(data.encode('utf-8'))
            logger("Uspesno poslani podaci na ReplicatorSender server!")
            print("Writer has sent your data to the next destination")
        else:
            print("Code must be integer between 1 and 8")
            logger("Uneta nevalidna vrednost za kod: broj nije izmedju 1 i 8")

        
logger("Uspesno zatvoren writer klijent")
