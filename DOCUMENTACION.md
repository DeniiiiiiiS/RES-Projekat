# Dokumentacija
- kod je pisan u python programskom jeziku
- koriscena je klient/server arhitektura sa tcp protokolom
- korisceni python paketi su socket, pickle, threading, time

## Writer komponenta
  Writer odnosno početna komponenta se koristi za uspostavljanje konekcije sa Replicator Sender komponentom. Korisnik može da bira iz menija opcije za rad:
  - 1. Slanje podataka ka bazi podataka
      - Od korisnika se traži da unese kod i vrednost koju želi da upiše u bazu podataka
  - 2. Dobijanje poslednje vrednosti za izabrani kod
      - Od korisnika se traži da unese kod za koji želi da dobije poslednju vrednost iz baze podataka
  - 3. Dobijanje svih vrednosti za izabrani kod
      - Od korisnika se traži da unese kod za koji želi da dobije sve vrednosti iz baze podataka
  - 4. Izlaz iz programa
      - Odabirom ove opcije, program se zatvara 

## Replicator sender komponenta
- vise vrajtera istovremeno moze uspotaviti konekciju ka senderu
- na svakih 90 sekundi salje podatke replicator receiveru
- dva soketa se koriste, jedan klijentski i jedan serverski
-  klijentski socket prima podatke od vrajtera, serverski soket salje podatke receiveru

## Replicator Receiver komponenta
  Replicator Receiver komponenta se koristi za uspostavljanje konekcije sa Replicator Sender komponentom, od koje prima CollectionDescription objekat, i sa Reader komponentama u zavisnosti od ispunjenosti određenog uslova. 

  Nakon što Receiver primi objekat, potrebno je da prođe kroz njegove atribute, i izvuče kod. Na osnovu koda, će se manipulisati sa listama add i update i to tako što će kad prvi put primi neki kod, njega staviti u add listu, a svaki naredni put u update listu.
  Pošto je raspored kodova po datasetovima već određen u prethodnoj komponenti, samo će se nadovezati te CollectionDescription1 (CD1) će se prepakovati u DeltaCD1 (DCD1) i takav poslati Reader1 komponenti. CD2 će biti prepakovan u DCD2 i poslaće se Reader2 komponenti. Na isti način će biti odrađeno za datasetove tri i četiri.

  Funkcije koje Receiver koristi:
  - **check(delt)**
    - kao parametar prima objekat DeltaCD
    - služi za proveru ispunjenosti uslova da je suma brojeva kodova u listama add i update jednaka 10
    - kao povratnu vrednost vraća True ili False
  - **send(i)**
    - kao parametar prima broj od 1 do 4
    - poziva metodu check kojoj prosleđuje jedan od objekata deltaCD zavisno od parametra i
    - uspostavlja konekciju ka Reader[1-4] komponenti i šalje deltaCD[1-4] objekat

## Reader komponenta
Reader komponenta služi da uspostavi konekciju sa Replicator Receiver komponentom, primi od nje podatke i trajno ih sačuva u bazu podataka.
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
| ID | DATASET | CODE | VALUE | DATETIME [PK] |
| --- | --- | --- | --- | --- |
| --- | --- | --- | --- | --- |
> Ovako izgleda tabela za svakog od reader-a

Reader komponente koriste funkcije iz fajlova reader_functions koje služe za proveru pristiglih podataka, upis u bazu, i pribavljanje podataka iz baze.
Funkcije koje Reader koristi su:
- **mydb_connection(host_name, user_name, user_password)**
  - ova funkcija ima povratnu vrednost <i>connection</i> uz pomoć koje će se dalje kroz program MySql komande.
  - pored toga služi i za konekciju sa bazom podataka
- **logger(message)**
  - služi za beleženje svih aktivnosti koje se dešavaju u svakoj od reader-a.
  - za parametar prima poruku koju će ispisati u .txt fajlu zajedno sa vremenom u koje vreme se neka funkcija izvršavala.
- **connect_to_database()**
  - služi da bi se napravila ako već ne postoji baza podataka u koju ce se smeštati kasnije dobijeni podaci.
- **create_table()**
  - služi za pravljenje tabele za svaku od reader-a, ukoliko vec ne postoji.
- **insert_process(id, dataset, code, value)**
  - koristi se na dobijenim podacima kako bi izvrsila proveru i validnost podataka
- **check_deadband(id, dataset, code, value)**
  - služi za proveru podataka koji već postoje u bazi sa unetom vrednošću, ukoliko postoji vec slična vrednost sa istim kodom, ona se zanemaruje, u suprotnom se šalje na upis.
- **insert(id, dataset, code, value)**
  - nakon svih prethodno izvršenih provera, funkcija insert služi za upis podataka (id, dataset, code, value, datetime) u određenu tabelu u bazi podataka.
- **get_last_value_for_code(code)**
  - koristi se kako bi ispisala poslednju unetu vrednost u bazi podataka za uneti kod.
- **read_values_by_code(code)**
  - funkcija koja dobavlja i ispisuje sve vrednosti iz tabele za određeni Reader za uneti kod. 
- **get_fetchall(cursor)**
  - funkcija koja služi za skraćivanje koda i lakšeg testiranja koda 
