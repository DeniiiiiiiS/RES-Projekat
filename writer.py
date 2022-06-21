import socket
from time import sleep
from writer_functions import logger
from Reader1_functions import get_last_value_for_code1
from Reader1_functions import read_values_by_code1
from Reader2_functions import get_last_value_for_code2
from Reader2_functions import read_values_by_code2
from Reader3_functions import get_last_value_for_code3
from Reader3_functions import read_values_by_code3
from Reader4_functions import get_last_value_for_code4
from Reader4_functions import read_values_by_code4


HOST = "127.0.0.1"
PORT = 8001
address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(address)
    logger("Uspesno konektovanje na ReplicatorSender server!")

    while True:
        print("---------- MENI ----------")
        print("1. Slanje podataka bazi")
        print("2. Dobavljanje poslednje vrednosti za izabrani kod")
        print("3. Dobavljanje svih vrednosti za izabrani kod")
        print("4. Izlazak iz programa")

        print("Izaberite zeljenu opciju:")
        opcija = input()

        if opcija == "1":
            while True:
                print("WRITER: Please input your data")
                print("To stop sending data, type -1 as Code and END as Value")

                print("Enter desired Code:")
                code = input()
                print("Enter desired Value:")
                value = input()

                if code.isdigit() == False:
                    print("Code must be integer between 1 and 8")
                    logger("Uneta nevalidna vrednost za kod: non-integer")
                    break
                if int(code) == -1 or value == "END":
                    print("Zaustavljanje writera...")
                    logger("Uneta vrednost za zaustavljanje rada writera")
                    break

                if int(code) >= 1 and int(code) <= 8:
                    sleep(2)
                    data = str(code) + ";" + str(value)
                    s.sendall(data.encode('utf-8'))
                    logger("Uspesno poslani podaci na ReplicatorSender server!")
                    print("Writer has sent your data to the next destination")
                else:
                    print("Code must be integer between 1 and 8")
                    logger("Uneta nevalidna vrednost za kod: broj nije izmedju 1 i 8")
        elif opcija == "2":
            print("Unesite zeljeni kod za dobavljanje poslednje vrednosti")
            kod = input()
            if kod == "1" or kod == "2":
                get_last_value_for_code1(int(kod))
            elif kod == "3" or kod == "4":
                get_last_value_for_code2(int(kod))
            elif kod == "5" or kod == "6":
                get_last_value_for_code3(int(kod))
            elif kod == "7" or kod == "8":
                get_last_value_for_code4(int(kod))
            else:
                print("Neispravno unet kod. Kodovi moraju biti u rasponu od 1 do 8")
        elif opcija == "3":
            print("Unesite zeljeni kod za dobavljanje svih vrednosti")
            kod = input()
            if kod == "1" or kod == "2":
                read_values_by_code1(int(kod))
            elif kod == "3" or kod == "4":
                read_values_by_code2(int(kod))
            elif kod == "5" or kod == "6":
                read_values_by_code3(int(kod))
            elif kod == "7" or kod == "8":
                read_values_by_code4(int(kod))
            else:
                print("Neispravno unet kod. Kodovi moraju biti u rasponu od 1 do 8")
        elif opcija == "4":
            print("Program uspesno prekinut")
            break
        else:
            print("Uneta vrednost nije prepoznata. Molimo pokusajte ponovo")
            continue
    # s.close()
logger("Uspesno zatvoren writer klijent")
