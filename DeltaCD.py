# DeltaCD.py

import CollectionDescription


class DeltaCD:
    def __init__(self):
        self.add_list = []   # Lista u kojoj se nalaze objekti CD koji trebaju da se dodaju u bazu
        self.update_list = []    # Lista u kojoj se nalaze objekti CD koji trebaju da se azuriraju u bazi

    def dodajNovi(self, cd):
        self.add_list.append(cd)
    
    def azurirajPostojeci(self, cd):
        self.update_list.append(cd)
