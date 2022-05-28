import socket

MAX_BROJ_WRITERA = 10
BROJ_BAJTOVA_KOJI_SE_PRIMA = 100
HOST = "127.0.0.1"
PORT1 = 8001
PORT2 = 8002

podaci = [] #OVDE TREBA DA BUDE OBJEKAT KLASE CD



#socket za primanje podataka
replicatorSenderServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorSenderServer.bind(HOST, PORT1)
replicatorSenderServer.listen(MAX_BROJ_WRITERA)


while True:
    conn, addr = replicatorSenderServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8")  #sacuva se primljeni podatak
    podaci.append(data) # OVDE TREBA DA SE PODATAK UBACi U OBJEKAT KLASE CD 
    if data == "kraj":  #OVO WRITER TREBA DA POSLAJE KAO KRAJ SLANJA PODATAKA
        break;

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderClient:
    replicatorSenderClient.connect((HOST, PORT2))
    replicatorSenderClient.sendall(bytes(podaci, "utf-8"))  #TREBA DA SE TAJ OBJEKAT CD POSALJE REPLICATOR SENDERU





# DRUGA IMPLEMENTACIJA(SLOZENIJA ALI VRV BOLJA)
'''
import time

INTERVAL_SLANJA = 60    #U SEKUNDAMA IZRAZENO


while True:
    conn, addr = replicatorSenderServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8")  #sacuva se primljeni podatak
    trenutak_pocetka_prijema_podataka = time.time()
    podaci.append(data) # OVDE TREBA DA SE PODATAK UBACi U OBJEKAT KLASE CD
    if time.time() >  (trenutak_pocetka_prijema_podataka + INTERVAL_SLANJA):    #AKO JE PROSLO 60 SEKUNDI POSALJI OBJEKAT CD RECEIVERU
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderClient:
            replicatorSenderClient.connect((HOST, PORT2))
            replicatorSenderClient.sendall(bytes(podaci, "utf-8"))  #TREBA DA SE TAJ OBJEKAT CD POSALJE REPLICATOR SENDERU
            #   TU SAD TREBA DA SE ISPRAZNI CD OBJEKAT, DA BI SE U NJEMU NALAZILI SAMO NOVI PODACI
'''