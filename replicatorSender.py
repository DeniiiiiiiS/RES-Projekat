import socket


HOST = "127.0.0.1"
PORT1 = 8001
PORT2 = 8002

#podaci = List



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderServer:
    replicatorSenderServer.bind(HOST, PORT1)
    replicatorSenderServer.listen()
    conn, addr = replicatorSenderServer.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode("utf-8")
            #skladisti podatak
            if not data:    #ili nekako da se oznaci kraj slanja podatka od klijenta
                break

  

replicatorSenderClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorSenderClient.connect(HOST, PORT2)
#treba da se salju podaci na replicatorReceiver


