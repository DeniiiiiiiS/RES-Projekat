import socket
import pickle
import collectionDescription
import deltaCD

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


delta_cd1 = deltaCD.DeltaCD()
delta_cd2 = deltaCD.DeltaCD()
delta_cd3  = deltaCD.DeltaCD()
delta_cd4 = deltaCD.DeltaCD()

#socket za primanje podataka
replicatorReceiverServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorReceiverServer.bind(address0)
replicatorReceiverServer.listen()


while True:
    conn, addr = replicatorReceiverServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA)
    podaci = pickle.loads(data)
    
    delta_cd1.dodajNovi(podaci[0].id)
    delta_cd2.dodajNovi(podaci[1].id)
    delta_cd3.dodajNovi(podaci[2].id)
    delta_cd4.dodajNovi(podaci[3].id)

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

