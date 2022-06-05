import socket

HOST = "127.0.0.1" 
PORT0 = 8002    # serverski port
PORT1 = 8005    # klijentski port za reader1
PORT2 = 8006    # klijentski port za reader2
PORT3 = 8006    # klijentski port za reader3
PORT4 = 8007    # klijentski port za reader4
BROJ_BAJTOVA_KOJI_SE_PRIMA = 100

podaci = [] #OVDE TREBA DA BUDE OBJEKAT KLASE DeltaCD

#socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(HOST, PORT0)
replicatorReceiverServer.listen()

while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8")  #sacuva se primljeni podatak
    podaci.append(data) # OVDE TREBA DA SE PODATAK UBACI U OBJEKAT KLASE DeltaCD 
    if data == "kraj":  #OVO replicatorSender TREBA DA POSALJE KAO KRAJ SLANJA PODATAKA
        break;

# Preostaje imeplementacija logike slanja podatka na Reader u skladu sa uslovom

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Reader:
    Reader.connect((HOST, PORT2))
    Reader.sendall(bytes(podaci, "utf-8"))  #TREBA DA SE TAJ OBJEKAT DeltaCD POSALJE nekom Reader-u 
