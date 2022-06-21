# Reader2-server.py
import pickle
import socket
from Reader2_functions import logger
from Reader2_functions import connect_to_database
from Reader2_functions import create_table
from Reader2_functions import insert_process

HOST_R2 = "127.0.0.1"
PORT_R2 = 8006
NUMBER_OF_BYTES = 1000000

connect_to_database()
logger("Reader2 successfully connected to database.")
create_table()

# povezivanje sa replicator receiver-om
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_R2, PORT_R2))
    while True:
        s.listen()
        print("Reader2: Waiting for connection...")
        logger("Reader2 waiting for connection.")
        conn, addr = s.accept()
        print(f"Reader2: Replicator receiver connected from {addr}")
        logger("ReplicatorReceiver successfully connected to Reader2.")
        inc_data = conn.recv(NUMBER_OF_BYTES)
        data = pickle.loads(inc_data)
        logger("Reader2 successfully received data from replicatorReceiver.")
        add_lista = data.add_list
        update_lista = data.update_list
        # upisivanje vrednosti u tabelu iz add_list-e
        logger("Reader2 started reading data from add_list.")
        for cdx in add_lista:
            id_add = cdx.getId()
            dataset_add = cdx.getDataset()
            hc_add = cdx.getHistoricalCollection().getNiz()
            for cdy in hc_add:
                code_add = cdy.getCode()
                value_add = cdy.getValue()
                insert_process(id_add, dataset_add, code_add, value_add)

        # upisivanje vrednosti u tabelu iz update_list-e
        logger("Reader2 started reading data from update_list.")
        for cdx in update_lista:
            id_update = cdx.getId()
            dataset_update = cdx.getDataset()
            hc_update = cdx.getHistoricalCollection().getNiz()
            for cdy in hc_update:
                code_update = cdy.getCode()
                value_update = cdy.getValue()
                insert_process(id_update, dataset_update, code_update, value_update)
        conn.close()
