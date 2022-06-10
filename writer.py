
import socket
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

        if int(code) == -1 or value == "END":
            break
        
        sleep(2)
        data = str(code) + ";" + str(value)
        s.sendall(data.encode('utf-8'))

        print("Writer has sent your data to the next destination")

s.close(address)

