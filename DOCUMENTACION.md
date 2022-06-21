# Dokumentacija
- kod je pisan u python programskom jeziku
- koriscena je klient/server arhitektura sa tcp protokolom
- korisceni python paketi su socket, pickle, threading, time
## Replicator sender komponenta
- vise vrajtera istovremeno moze uspotaviti konekciju ka senderu
- na svakih 90 sekundi salje podatke replicator receiveru
- dva soketa se koriste, jedan klijentski i jedan serverski
-  klijentski socket prima podatke od vrajtera, serverski soket salje podatke receiveru

