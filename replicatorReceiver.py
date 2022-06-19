import socket
import pickle
import CollectionDescription
import DeltaCD
import time

HOST = "127.0.0.1" 
PORT0 = 8002    # serverski port
PORT1 = 8005    # klijentski port za reader1
PORT2 = 8006    # klijentski port za reader2
PORT3 = 8007    # klijentski port za reader3
PORT4 = 8008    # klijentski port za reader4
BROJ_BAJTOVA_KOJI_SE_PRIMA = 1000000

address0 = (HOST, PORT0)
address1 = (HOST, PORT1)
address2 = (HOST, PORT2)
address3 = (HOST, PORT3)
address4 = (HOST, PORT4)

codeOneCounter = 0
codeTwoCounter = 0
codeThreeCounter = 0
codeFourCounter = 0

buffer = []
delta_cd = []
address = []
address.append(address1); address.append(address2); address.append(address3); address.append(address4);

delta_cd1 = DeltaCD.DeltaCD()
delta_cd2 = DeltaCD.DeltaCD()
delta_cd3  = DeltaCD.DeltaCD()
delta_cd4 = DeltaCD.DeltaCD()

delta_cd.append(delta_cd1); delta_cd.append(delta_cd2); delta_cd.append(delta_cd3); delta_cd.append(delta_cd4);

def logger(message):
    time_now = time.localtime()
    with open("receiver.txt", 'a') as f:
        f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, {message}\n")

def send(i):
    if(len(delta_cd[i].add_list) + len(delta_cd[i].update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address[i])
                msg = pickle.dumps(delta_cd[i])  
                replicatorReceiverClient.send(msg)
                i+=1
                logger("Uspesno poslani podaci na Reader {i}!")

#socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(address0)
replicatorReceiverServer.listen()
print("Cekanje na konekciju...")
logger("Uspesno otvoren server za osluskivanje!")


while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA)
    buffer = pickle.loads(data)

    logger("Uspesno primljeni podaci na server!")

    i = 0
    for delta in delta_cd:

        kodovi = []

        id_iz_buff = buffer[i].getId()
        dataset_iz_buff = buffer[i].getDataset()
        for y in buffer[i].getHistoricalCollection().getNiz():
            code_iz_buff = y.getCode()
            value_iz_buff = y.getValue()
            if code_iz_buff not in kodovi:
                delta.dodajNovi(buffer[i])
                kodovi.append(code_iz_buff)
                logger("Uspesno dodan novi kod u add listu!")
            else:
                delta.azurirajPostojeci(buffer[i])
                logger("Uspesno dodan vec postojeci kod u update listu!")
        i += 1

    for k in range (1, 5):
        send(k)


    '''
    if(len(delta_cd1.add_list) + len(delta_cd1.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address1)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 1!")

    if(len(delta_cd2.add_list) + len(delta_cd2.update_list) == 10):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address2)
                msg = pickle.dumps(delta_cd2)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 2!")

    if(len(delta_cd3.add_list) + len(delta_cd3.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address3)
                msg = pickle.dumps(delta_cd3)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 3!")

    if(len(delta_cd4.add_list) + len(delta_cd4.update_list) == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address4)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)
                logger("Uspesno poslani podaci na Reader 4!") 
    '''
