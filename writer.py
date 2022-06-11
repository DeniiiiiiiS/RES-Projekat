
import socket
import time
from time import sleep

HOST = "127.0.0.1"
PORT = 8001
address = (HOST, PORT)

def logger(message):
    time_now = time.localtime()
    with open("writer.txt", 'a') as f:
        f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, {message}\n")

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

        if int(code) == -1 or value == "END":
            break
        
        sleep(2)
        data = str(code) + ";" + str(value)
        s.sendall(data.encode('utf-8'))
        logger("Uspesno poslani podaci na ReplicatorSender server!")


        print("Writer has sent your data to the next destination")

s.close(address)
logger("Uspesno zatvoren writer klijent")
