import socket
import pickle
import CollectionDescription
import DeltaCD
import time

HOST = "127.0.0.1" 
PORT0 = 8002    # serverski port
PORT1 = 8005    # klijentski port za reader1
PORT2 = 8006    # klijentski port za reader2
PORT3 = 8006    # klijentski port za reader3
PORT4 = 8007    # klijentski port za reader4
BROJ_BAJTOVA_KOJI_SE_PRIMA = 1000000

address0 = (HOST, PORT0)
address1 = (HOST, PORT1)
address2 = (HOST, PORT2)
address3 = (HOST, PORT3)
address4 = (HOST, PORT4)

codeOneCounter, codeTwoCounter, codeThreeCounter, codeFourCounter = 0

buffer = []
delta_cd = []

delta_cd1 = DeltaCD.DeltaCD()
delta_cd2 = DeltaCD.DeltaCD()
delta_cd3  = DeltaCD.DeltaCD()
delta_cd4 = DeltaCD.DeltaCD()

delta_cd.append(delta_cd1); delta_cd.append(delta_cd2); delta_cd.append(delta_cd3); delta_cd.append(delta_cd4);

#socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(address0)
replicatorReceiverServer.listen()

time_now = time.localtime()
                
with open("replicatorReceiver.txt", 'time_now') as f:
    f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno otvoren server za osluskivanje!\n")


'''
def checker(code, delta, i):
    if code == 0:
        delta.dodajNovi(buffer[i].id)
        code += 1
    else:
        delta.azurirajPostojeci(buffer[i].id)
'''    


while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA)
    buffer = pickle.loads(data)

    time_now = time.localtime()
                
    with open("replicatorReceiver.txt", 'time_now') as f:
        f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno primljeni podaci na server!\n")

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
            else:
                delta.azurirajPostojeci(buffer[i])
        i += 1

    '''   
    checker(codeOneCounter, delta_cd1, 0)
    checker(codeTwoCounter, delta_cd2, 1)
    checker(codeThreeCounter, delta_cd3, 2)
    checker(codeFourCounter, delta_cd4, 3)

    
    if codeOneCounter == 0:
        delta_cd1.dodajNovi(buffer[0].id)
        codeOneCounter += 1
    else:
        delta_cd1.azurirajPostojeci(buffer[0].id)

    if codeTwoCounter == 0:
        delta_cd2.dodajNovi(buffer[1].id)
        codeTwoCounter += 1
    else:
        delta_cd2.azurirajPostojeci(buffer[1].id)

    if codeThreeCounter == 0:
        delta_cd3.dodajNovi(buffer[2].id)
        codeThreeCounter += 1
    else:
        delta_cd3.azurirajPostojeci(buffer[2].id)

    if codeFourCounter == 0:
        delta_cd4.dodajNovi(buffer[3].id)
        codeFourCounter += 1
    else:
        delta_cd4.azurirajPostojeci(buffer[3].id)

    '''

    if(delta_cd1.add_list.count + delta_cd1.update_list.count == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address1)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)
                time_now = time.localtime()
                
                with open("replicatorReceiver.txt", 'time_now') as f:
                    f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno poslani podaci na Reader 1!\n")

    if(delta_cd2.add_list.count + delta_cd1.update_list.count == 10):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address2)
                msg = pickle.dumps(delta_cd2)  
                replicatorReceiverClient.send(msg)
                time_now = time.localtime()
                
                with open("replicatorReceiver.txt", 'time_now') as f:
                    f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno poslani podaci na Reader 2!\n")

    if(delta_cd3.add_list.count + delta_cd1.update_list.count == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address3)
                msg = pickle.dumps(delta_cd3)  
                replicatorReceiverClient.send(msg)
                time_now = time.localtime()
                
                with open("replicatorReceiver.txt", 'time_now') as f:
                    f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno poslani podaci na Reader 3!\n")     

    if(delta_cd4.add_list.count + delta_cd1.update_list.count == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address4)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)
                time_now = time.localtime()
                
                with open("replicatorReceiver.txt", 'time_now') as f:
                    f.write(f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}, Uspesno poslani podaci na Reader 4!\n") 
