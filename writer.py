# writer-client.py

import socket
import codovi
from time import sleep

HOST = "127.0.0.1"
PORT = 8001
address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(address)

    while True:
        print("WRITER: Please input your data")
        print("To stop sending data, type -1 as Code and END as Value")

        print("Enter desired Code:")
        code = input()
        print("Enter desired Value:")
        value = input()

        if code == -1 or value == "END":
            break

        if code == 0:
            data = codovi.Code.CODE_ANALOG + ";" + value
        elif code == 1:
            data = codovi.Code.CODE_DIGITAL + ";" + value
        elif code == 2:
            data = codovi.Code.CODE_CUSTOM + ";" + value
        elif code == 3:
            data = codovi.Code.CODE_LIMITSET + ";" + value
        elif code == 4:
            data = codovi.Code.CODE_SINGLENODE + ";" + value
        elif code == 5:
            data == codovi.Code.CODE_MULTIPLENODE + ";" + value
        elif code == 6:
            data = codovi.Code.CODE_CONSUMER + ";" + value
        elif code == 7:
            data = codovi.Code.CODE_SOURCE + ";" + value

        sleep(2)
        s.sendall(data.encode('utf-8'))


        print("Writer has sent your data to the next destination")

#data = "-1;END"
#s.sendall(data)
