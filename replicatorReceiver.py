import socket
import pickle
import CollectionDescription
import DeltaCD

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


delta_cd1 = DeltaCD.DeltaCD()
delta_cd2 = DeltaCD.DeltaCD()
delta_cd3  = DeltaCD.DeltaCD()
delta_cd4 = DeltaCD.DeltaCD()

#socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(address0)
replicatorReceiverServer.listen()


def checker(code, delta, i):
    if code == 0:
        delta.dodajNovi(buffer[i].id)
        code += 1
    else:
        delta.azurirajPostojeci(buffer[i].id)
    


while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA)
    buffer = pickle.loads(data)
    
    checker(codeOneCounter, delta_cd1, 0)
    checker(codeTwoCounter, delta_cd2, 1)
    checker(codeThreeCounter, delta_cd3, 2)
    checker(codeFourCounter, delta_cd4, 3)

    '''
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

    if(delta_cd2.add_list.count + delta_cd1.update_list.count == 10):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address2)
                msg = pickle.dumps(delta_cd2)  
                replicatorReceiverClient.send(msg)

    if(delta_cd3.add_list.count + delta_cd1.update_list.count == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address3)
                msg = pickle.dumps(delta_cd3)  
                replicatorReceiverClient.send(msg)     

    if(delta_cd4.add_list.count + delta_cd1.update_list.count == 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorReceiverClient:
                replicatorReceiverClient.connect(address4)
                msg = pickle.dumps(delta_cd1)  
                replicatorReceiverClient.send(msg)  
