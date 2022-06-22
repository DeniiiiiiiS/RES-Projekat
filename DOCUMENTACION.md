# Dokumentacija
- kod je pisan u python programskom jeziku
- koriscena je klient/server arhitektura sa tcp protokolom
- korisceni python paketi su socket, pickle, threading, time
## Replicator sender komponenta
- vise vrajtera istovremeno moze uspotaviti konekciju ka senderu
- na svakih 90 sekundi salje podatke replicator receiveru
- dva soketa se koriste, jedan klijentski i jedan serverski
-  klijentski socket prima podatke od vrajtera, serverski soket salje podatke receiveru
## Reader komponenta
Reader komponenta sluzi da uspostavi konekciju sa Replicator Receiver komponentom, primi od nje podatke i trajno ih sacuva u bazu podataka.
Postoji 4 Reader-a od kojih svaki radi sa svojom tabelom u bazi podataka.
- Reader1
  - Radi sa dataset-om 1 i kodovima CODE_ANALOG[1] i CODE_DIGITAL[2]
- Reader2
  - Radi sa dataset-om 2 i kodovima CODE_CUSTOM[3] i CODE_LIMITSET[4]
- Reader3
  - Radi sa dataset-om 3 i kodovima CODE_SINGLENODE[5] i CODE_MULTIPLENODE[6]
- Reader4
  - Radi sa dataset-om 4 i kodovima CODE_CONSUMER[7] i CODE_SOURCE[8]

U samim Reader komponentama se nalazi uspostavljanje konekcije sa <i>Replicator Receiver</i> komponentom kako bi pridobio podatke i mogao da ih ubaci u proces ubacivanja u bazu podataka.
Za bazu podataka se koristi MySql za koji je potreban mysql-connector package.

Izgled tabele:
| ID | DATASET | CODE | VALUE | DATETIME |
| --- | --- | --- | --- | --- |
| --- | --- | --- | --- | --- |
> Ovako izgleda tabela za svakog od reader-a

Reader komponente koriste funkcije iz fajlova reader_functions koje služe za proveru pristiglih podataka, upis u bazu, i pribavljanje podataka iz baze.
Funkcije koje Reader koristi su:
- mydb_connection(host_name, user_name, user_password)
  - ova funkcija ima povratnu vrednost <i>connection</i> uz pomoc koje ce se dalje kroz program MySql komande.
  - pored toga sluzi i za konekciju sa bazom podataka
- logger(message)
  - služi za beleženje svih aktivnosti koje se dešavaju u svakoj od reader-a.
  - za parametar prima poruku koju će ispisati u .txt fajlu zajedno sa vremenom u koje vreme se neka funkcija izvršavala.
- connect_to_database()
  - sluzi da bi se napravila ako vec ne postoji baza podataka u koju ce se smestati kasnije dobijeni podaci.
- create_table()
  - sluzi za pravljenje tabele za svaku od reader-a, ukoliko vec ne postoji.
- insert_process(id, dataset, code, value)
  - koristi se na dobijenim podacima kako bi izvrsila proveru i validnost podataka
- check_deadband(id, dataset, code, value)
  - sluzi za proveru podataka koji vec postoje u bazi sa unetom vrednoscu, ukoliko postoji vec slicna vrednost sa istim kodom, ona se zanemaruje, u suprotnom se salje na upis.
- insert(id, dataset, code, value) 
  - nakon svih prethodno izvrsenih provera, funkcija insert sluzi za upis podataka (id, dataset, code, value, datetime) u odredjenu tabelu u bazi podataka.
- get_last_value_for_code(code)
  - koristi se kako bi ispisala poslednju unetu vrednost u bazi podataka za uneti kod.
- read_values_by_code(code)
  - funkcija koja dobavlja i ispisuje sve vrednosti iz tabele za odredjeni Reader za uneti kod. 
- get_fetchall(cursor)
  - funkcija koja sluzi za skracivanje koda i lakseg testiranja koda 
