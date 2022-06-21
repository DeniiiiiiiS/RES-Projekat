import socket, pickle
import time
from tracemalloc import start
import receiverProperty, historicalCollection, CollectionDescription, codovi
import threading
from sender_functions import konvertuj_u_ReceiverProperty
from sender_functions import Logger


MAX_BROJ_WRITERA = 10
BROJ_BAJTOVA_KOJI_SE_PRIMA = 1000
HOST = "127.0.0.1"
PORT1 = 8001;   PORT2 = 8002;
INTERVAL_SLANJA = 5    #U SEKUNDAMA IZRAZENO

cd1 = CollectionDescription.CollectionDescription(1, 1)
cd2 = CollectionDescription.CollectionDescription(2, 2)
cd3 = CollectionDescription.CollectionDescription(3, 3)
cd4 = CollectionDescription.CollectionDescription(4, 4)

buffer = []
buffer.append(cd1); buffer.append(cd2); buffer.append(cd3); buffer.append(cd4); 

def  ubaci_u_CollectionDescription(recProp):
    if recProp.code == codovi.Code.CODE_ANALOG.value or recProp.code == codovi.Code.CODE_DIGITAL.value:
        if recProp.receiver_value == 666:
            return False
        else:
            cd1.dodaj_u_HistoricalCollection(recProp)
            return True
    elif recProp.code == codovi.Code.CODE_CUSTOM.value or recProp.code == codovi.Code.CODE_LIMITSET.value:
        if recProp.receiver_value == 666:
            return False
        else:    
            cd2.dodaj_u_HistoricalCollection(recProp)
            return True
    elif recProp.code == codovi.Code.CODE_SINGLENODE.value or recProp.code == codovi.Code.CODE_MULTIPLENODE.value:
        if recProp.receiver_value == 666:
            return False
        else:    
            cd3.dodaj_u_HistoricalCollection(recProp)
            return True
    elif recProp.code == codovi.Code.CODE_CONSUMER.value or recProp.code == codovi.Code.CODE_SOURCE.value:
        if recProp.receiver_value == 666:
            return False
        else:
            cd4.dodaj_u_HistoricalCollection(recProp)
            return True
    return False

def isprazniBuffer():
    buffer[0].isprazniHistoricalCollection()
    buffer[1].isprazniHistoricalCollection()
    buffer[2].isprazniHistoricalCollection()
    buffer[3].isprazniHistoricalCollection()
    

def provera_za_slanje(trenutak_pocetka_prijema):
    while True:
        if time.time() > (trenutak_pocetka_prijema + INTERVAL_SLANJA):  #AKO JE PROSLO 90 SEKUNDI POSALJI NIZ OD 4 CD OBJEKTA
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replicatorSenderClient:
                replicatorSenderClient.connect((HOST,PORT2))
                msg = pickle.dumps(buffer)  #KONVERTUJE U NIZ BAJTOVA
                replicatorSenderClient.send(msg)
                Logger("Podaci poslati replicator receiveru!")
                isprazniBuffer()
                Logger("Buffer je ispraznjen!")
                trenutak_pocetka_prijema = time.time()  #POSTAVI NA TRENUTNO VREME

def handle_writer(connection, address):
    while True:
        data = connection.recv(BROJ_BAJTOVA_KOJI_SE_PRIMA).decode("utf-8") #SACUVA SE PRIMLJENI PODATAK
        Logger(f"Podatak primljen od writera sa adrese {address}!")
        rc = konvertuj_u_ReceiverProperty(data)
        if rc == "lose":
            Logger(f"Writer je prekinuo konekciju sa adrese {address}!")
            print(f"Broj konektovanih writer je {threading.active_count() - 2}")
            break
        if ubaci_u_CollectionDescription(rc):
            Logger("Podatak je validan i sacuvan u buffer!")
        else:
            Logger(f"Podatak primljen od writera sa adrese {address} nije validan!")

def start_SenderServer(socket_SenderServer):
    socket_SenderServer.listen(MAX_BROJ_WRITERA)
    print("ReplicatorSender is listening!")
    while True:
        conn, addr = socket_SenderServer.accept()
        Logger(f"Writer se uspeno konektovao sa adrese {addr}!")
        thread = threading.Thread(target=handle_writer, args=(conn, addr)) #    ZA SVAKI WRITER SE KREIRA NOVI NIT
        thread.start()
        print(f"Broj konektovanih writer je {threading.active_count() - 2}")


trenutak_pocetka_prijema_podataka = time.time()

thread_slanja = threading.Thread(target=provera_za_slanje, args=(trenutak_pocetka_prijema_podataka,))   #POSEBNA NIT ZA PROVERU SLANJA
thread_slanja.start()

replicatorSenderServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
replicatorSenderServer.bind((HOST, PORT1))

start_SenderServer(replicatorSenderServer)