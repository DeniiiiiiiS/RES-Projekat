import socket, pickle
import time
import receiverProperty, historicalCollection, collectionDescription, codovi


MAX_BROJ_WRITERA = 10
BROJ_BAJTOVA_KOJI_SE_PRIMA = 1000
HOST = "127.0.0.1"
PORT1 = 8001;   PORT2 = 8002;
INTERVAL_SLANJA = 90    #U SEKUNDAMA IZRAZENO

cd1 = collectionDescription.CollectionDescription(1, "neki_data_set")
cd2 = collectionDescription.CollectionDescription(2, "neki_data_set")
cd3 = collectionDescription.CollectionDescription(3, "neki_data_set")
cd4 = collectionDescription.CollectionDescription(4, "neki_data_set")

buffer = []
buffer.append(cd1); buffer.append(cd2); buffer.append(cd3); buffer.append(cd4); 


def konvertuj_u_ReceiverProperty(data):
    split_karakter = ";"
    podatak = data.split(split_karakter)
    code = podatak[0]
    value = podatak[1]
    a = receiverProperty.ReceiverProperty(int(code),value)
    return a

def  ubaci_u_CollectionDescription(recProp):
    if recProp.code == codovi.Code.CODE_ANALOG.value or recProp.code == codovi.Code.CODE_DIGITAL.value:
        cd1.dodaj_u_HistoricalCollection(recProp)
    elif recProp.code == codovi.Code.CODE_CUSTOM.value or recProp.code == codovi.Code.CODE_LIMITSET.value:
        cd2.dodaj_u_HistoricalCollection(recProp)
    elif recProp.code == codovi.Code.CODE_SINGLENODE.value or recProp.code == codovi.Code.CODE_MULTIPLENODE.value:
        cd3.dodaj_u_HistoricalCollection(recProp)
    elif recProp.code == codovi.Code.CODE_CONSUMER.value or recProp.code == codovi.Code.CODE_SOURCE.value:
        cd4.dodaj_u_HistoricalCollection(recProp)

def isprazniBuffer(buffer_cdova):
    buffer_cdova[0].isprazniHistoricalCollection()
    buffer_cdova[1].isprazniHistoricalCollection()
    buffer_cdova[2].isprazniHistoricalCollection()
    buffer_cdova[3].isprazniHistoricalCollection()


#socket za primanje podataka
replicatorSenderServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorSenderServer.bind((HOST, PORT1))
replicatorSenderServer.listen(MAX_BROJ_WRITERA)
conn, addr = replicatorSenderServer.accept()
trenutak_pocetka_prijema_podataka = time.time()

while True:
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8")  #sacuva se primljeni podatak

    

    rc = konvertuj_u_ReceiverProperty(data)
    ubaci_u_CollectionDescription(rc)
    
    if time.time() >  (trenutak_pocetka_prijema_podataka + INTERVAL_SLANJA):    #AKO JE PROSLO 90 SEKUNDI POSALJI OBJEKAT CD RECEIVERU
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderClient:
            replicatorSenderClient.connect((HOST, PORT2))
            msg = pickle.dumps(buffer)  #KONVERTUJE SE NIZ CDOVA U BAJTOVE
            replicatorSenderClient.send(msg)
            isprazniBuffer(buffer)
            trenutak_pocetka_prijema_podataka = time.time() #POSTAVI NA TRENUTNO VREME












# PRVA IMPLEMENTACIJA
'''
while True:
    conn, addr = replicatorSenderServer.accept()
    data = conn.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8")  #sacuva se primljeni podatak
    podaci.append(data) # OVDE TREBA DA SE PODATAK UBACi U OBJEKAT KLASE CD 
    if data == "kraj":  #OVO WRITER TREBA DA POSLAJE KAO KRAJ SLANJA PODATAKA
        break;

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderClient:
    replicatorSenderClient.connect((HOST, PORT2))
    replicatorSenderClient.sendall(bytes(podaci, "utf-8"))  #TREBA DA SE TAJ OBJEKAT CD POSALJE REPLICATOR SENDERU

'''




